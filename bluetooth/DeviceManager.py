import dbus
from module.EventBus import mainEventBus
from module.EventBus import EventBus
from bluetooth.objects.Device import Device


class DeviceManager:
    bus: dbus.SystemBus = None
    event_bus: EventBus
    devices: [] = []
    active_device: Device = None

    def __init__(self):
        self.event_bus = EventBus()
        self.bus = dbus.SystemBus()

        self.bus.add_signal_receiver(
            self.on_dbus_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties',
            path_keyword="path"
        )

        mainEventBus.on('device:connected', self.__on_device_connected)
        mainEventBus.on('device:disconnected', self.__on_device_disconnected)

    def on_dbus_property_changed(self, interface, changed, invalidated, path=None):
        if interface == 'org.bluez.Device1':
            if 'Paired' in changed:
                self.__on_new_device(path)

    def set_active_device(self, new_device):
        if self.active_device:
            self.active_device.event_bus.remove_forwarding('bt-device-manager:active-device')
            if self.active_device.is_connected():
                self.active_device.disconnect()

        self.active_device = new_device

        if new_device:
            self.active_device.event_bus.add_forwarding('bt-device-manager:active-device', self.event_bus)
            mainEventBus.trigger('bt-device-manager:active-device', {
                'device': new_device
            })

    def has_active_device(self):
        if not self.active_device:
            return False

        return self.active_device.is_connected()

    def get_active_device(self):
        return self.active_device

    def get_devices(self):
        return self.devices

    def get_device_by_address(self, address):
        for device in self.devices:
            if device.get_address() == address:
                return device
        return None

    def __on_new_device(self, path):
        device = Device(path)
        if self.get_device_by_address(device.get_address()):
            del device
            return
        self.devices.append(device)
        if device.has_a2dp():
            self.set_active_device(device)

    def __on_device_connected(self, args: dict):
        device = args['device']
        if not self.has_active_device():
            self.set_active_device(device)

    def __on_device_disconnected(self, args: dict):
        device = args['device']
        if self.active_device == device:
            next_device = self.__get_first_available_device()
            if next_device:
                self.set_active_device(next_device)
            else:
                self.set_active_device(None)

    def __get_first_available_device(self):
        for device in self.get_devices():
            if device.is_connected() and device.has_a2dp():
                return device
        return None

    def find_all_devices(self):
        obj = self.bus.get_object('org.bluez', "/")
        mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
        for path, ifaces in mgr.GetManagedObjects().items():
            adapter = ifaces.get('org.bluez.Device1')
            if not adapter:
                continue
            device = Device(path)
            self.devices.append(device)
            if device.is_connected() and not self.has_active_device():
                self.set_active_device(device)
