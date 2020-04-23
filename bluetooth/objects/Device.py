import dbus
from module.EventBus import EventBus
from bluetooth.objects.Player import Player


class Device:
    event_bus: EventBus = EventBus()
    __path: str
    __dbus_obj: dbus.proxies.ProxyObject
    __dbus_iface: dbus.proxies.Interface
    __dbus_props_iface: dbus.proxies.Interface

    __player_path: str = None
    __player: Player = None

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
        self.__find_player()

    def is_connected(self):
        return self.get_prop('Connected')

    def has_a2dp(self):
        uuids = self.get_prop('UUIDs')
        return '0000110d-0000-1000-8000-00805f9b34fb' in uuids

    def has_player(self):
        return self.__player is not None

    def get_player(self):
        if not self.__player:
            raise Exception("Device has'nt player " + self.__path)

        return self.__player

    def __find_player(self):
        if self.__player is not None:
            return
        obj = dbus.SystemBus().get_object('org.bluez', "/")
        mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
        for path, ifaces in mgr.GetManagedObjects().items():
            if str(path).startswith(self.__path):
                adapter = ifaces.get('org.bluez.MediaPlayer1')
                if not adapter:
                    continue
                self.__set_player(path)

    def __on_properties_changed(self, interface, changed: dict, invalidated):
        if changed.get('Connected'):
            self.__on_connected_property_change(changed.get('Connected'))
        if changed.get('Player'):
            self.__on_player_change(changed.get('Player'))

    def __on_connected_property_change(self, value):
        if not value:
            self.event_bus.trigger('disconnected')

    def __on_player_change(self, path):
        self.__set_player(path)

    def __set_player(self, player_path: str):
        self.__player_path = player_path
        if self.__player:
            del self.__player
        self.__player = Player(self.__player_path)
        self.event_bus.trigger('player-changed', {
            'player': self.get_player()
        })

    def get_prop(self, prop_name: str):
        return self.__dbus_props_iface.Get('org.bluez.Device1', prop_name)