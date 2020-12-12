from module.EventBus import EventBus
import dbus
import ctypes


class Adapter:
    __path: str
    __adapter_object = None
    __adapter_iface = None
    __props_iface = None
    event_bus: EventBus

    def __init__(self, adapter_path: str):
        self.event_bus = EventBus()
        self.__path = adapter_path
        self.__adapter_object = dbus.SystemBus().get_object('org.bluez', adapter_path)
        self.__adapter_object.connect_to_signal(
            'PropertiesChanged',
            self.__properties_changed_callback,
            dbus_interface='org.freedesktop.DBus.Properties'
        )
        self.__adapter_iface = dbus.Interface(self.__adapter_object, 'org.bluez.Adapter1')
        self.__props_iface = dbus.Interface(self.__adapter_object, 'org.freedesktop.DBus.Properties')

    def __del__(self):
        self.event_bus.off_all()
        del self.event_bus

    def get_prop(self, name: str):
        try:
            return self.__props_iface.Get('org.bluez.Adapter1', name)
        except dbus.exceptions.DBusException:
            return None

    def set_discoverable(self, discoverable):
        self.__props_iface.Set('org.bluez.Adapter1', 'Discoverable', discoverable)

    def set_discoverable_timeout(self, timeout):
        self.__props_iface.Set('org.bluez.Adapter1', 'DiscoverableTimeout', int(timeout))

    def get_all_props(self):
        return self.__props_iface.GetAll('org.bluez.Adapter1')

    def start_discovery(self):
        if self.get_prop('Discovering'):
            return
        try:
            self.__adapter_iface.StartDiscovery()
        except dbus.exceptions.DBusException as e:
            if e.get_dbus_name() == 'org.bluez.Error.InProgress':
                return

    def stop_discovery(self):
        self.__adapter_iface.StopDiscovery()

    def is_discovering(self):
        return self.get_prop('Discovering')

    def __properties_changed_callback(self, interface, changed: dict, invalidated):
        self.event_bus.trigger('properties-changed', {
            'changed': changed
        })
