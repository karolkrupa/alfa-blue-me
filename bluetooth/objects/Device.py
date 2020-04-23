import dbus
from module.EventBus import EventBus
from bluetooth.objects.Player import Player


class Device:
    event_bus: EventBus = EventBus()
    __path: str
    __dbus_obj: dbus.proxies.ProxyObject
    __dbus_iface: dbus.proxies.Interface
    __dbus_props_iface: dbus.proxies.Interface

    def __init__(self, path: str):
        self.__path = path
        self.__dbus_obj = dbus.SystemBus().get_object('org.bluez', path)
        self.__dbus_obj.connect_to_signal(
            'PropertiesChanged',
            self.__on_properties_changed,
            dbus_interface='org.freedesktop.DBus.Properties'
        )
        self.__dbus_iface = dbus.Interface('org.bluez.Device1', self.__dbus_obj)
        self.__dbus_props_iface = dbus.Interface(self.__dbus_obj, 'org.freedesktop.DBus.Properties')

    def is_connected(self):
        return self.__get_prop('Connected')

    def has_a2dp(self):
        uuids = self.__get_prop('UUIDs')
        return '0000110d-0000-1000-8000-00805f9b34fb' in uuids

    def get_player(self):
        if not self.is_connected():
            raise 'Device ' + self.__path + " is'nt connected (get_player)"
        return Player(self.__path + '/MediaPlayer1')

    def __on_properties_changed(self, interface, changed: dict, invalidated):
        if changed.get('Connected'):
            self.__on_connected_property_change(changed.get('Connected'))

    def __on_connected_property_change(self, value):
        if not value:
            self.event_bus.trigger('disconnected')

    def __get_prop(self, prop_name: str):
        return self.__dbus_props_iface.Get('org.bluez.Device1', prop_name)