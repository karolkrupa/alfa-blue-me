import dbus
from module.EventBus import mainEventBus
from bluetooth.objects.Device import Device


class DeviceManager:
    bus: dbus.SystemBus = None
    devices: [] = []
    active_device: Device = None

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.__find_all_devices()

        mainEventBus.on('bt-agent:device-confirmed', self.__on_new_device)

    def set_active_device(self, device: Device):
        self.active_device = device

        mainEventBus.trigger('bt-device-manager:active-player', {
            'player': device
        })

    def has_active_device(self):
        if not self.active_device:
            return False

        return self.active_device.is_connected()

    def get_active_device(self):
        return self.active_device

    def __on_new_device(self, args: dict):
        device = Device(args['path'])
        self.devices.append(device)
        if device.has_a2dp():
            self.set_active_device(device)

    def __find_all_devices(self):
        obj = self.bus.get_object('org.bluez', "/")
        mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
        for path, ifaces in mgr.GetManagedObjects().items():
            adapter = ifaces.get('org.bluez.Device1')
            if not adapter:
                continue
            device = Device(path)
            self.devices.append(device)
            if device.is_connected():
                self.set_active_device(device)
