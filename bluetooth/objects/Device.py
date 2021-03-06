import dbus
from module.EventBus import EventBus, mainEventBus
from bluetooth.objects.Player import Player


class Device:
    event_bus: EventBus
    __path: str
    __dbus_obj: dbus.proxies.ProxyObject
    __dbus_iface: dbus.proxies.Interface
    __dbus_props_iface: dbus.proxies.Interface

    __player_path: str = None
    __player: Player = None

    def __init__(self, path: str):
        self.event_bus = EventBus()
        self.__path = path
        self.__dbus_obj = dbus.SystemBus().get_object('org.bluez', path)
        self.__dbus_obj.connect_to_signal(
            'PropertiesChanged',
            self.__on_properties_changed,
            dbus_interface='org.freedesktop.DBus.Properties'
        )
        self.__dbus_iface = dbus.Interface(self.__dbus_obj, 'org.bluez.Device1')
        self.__dbus_props_iface = dbus.Interface(self.__dbus_obj, 'org.freedesktop.DBus.Properties')
        self.__find_player()

    def __del__(self):
        if self.__player:
            del self.__player
        self.event_bus.off_all()
        del self.event_bus

    def is_connected(self):
        return self.get_prop('Connected')

    def is_paired(self):
        return self.get_prop('Paired')

    def pair(self):
        self.__dbus_iface.Pair()

    def connect(self):
        self.__dbus_iface.Connect()

    def disconnect(self):
        self.__dbus_iface.Disconnect()

    def connect_profile(self, profile):
        self.__dbus_iface.ConnectProfile(profile)

    def has_a2dp(self):
        uuids = self.get_prop('UUIDs')
        return '0000110d-0000-1000-8000-00805f9b34fb' in uuids

    def has_player(self):
        return self.__player is not None

    def get_player(self):
        if not self.__player:
            raise Exception("Device hasn't player " + self.__path)

        return self.__player

    def get_address(self):
        return self.get_prop('Address')

    def get_rssi(self):
        return self.get_prop('RSSI')

    def get_name(self):
        return self.get_prop('Name', 'Unknown')

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
        if 'Connected' in changed:
            self.__on_connected_property_change(changed.get('Connected'))
        if 'Player' in changed:
            self.__on_player_change(changed.get('Player'))
        if 'Paired' in changed:
            self.__on_paired_change(changed.get('Paired'))

    def __on_connected_property_change(self, value):
        if not value:
            self.event_bus.trigger('disconnected')
            mainEventBus.trigger('device:disconnected', {
                'device': self
            })
        else:
            self.event_bus.trigger('connected')
            mainEventBus.trigger('device:connected', {
                'device': self
            })

    def __on_player_change(self, path):
        self.__set_player(path)

    def __on_paired_change(self, value):
        if not value:
            self.event_bus.trigger('unpaired')
            mainEventBus.trigger('device:unpaired', {
                'device': self
            })
        else:
            self.event_bus.trigger('paired')
            mainEventBus.trigger('device:paired', {
                'device': self
            })

    def __set_player(self, player_path: str):
        self.__player_path = player_path
        if self.__player:
            del self.__player
        self.__player = Player(self.__player_path)
        self.__player.event_bus.add_forwarding('active-player', self.event_bus)
        self.event_bus.trigger('player-changed', {
            'player': self.get_player()
        })

    def get_prop(self, prop_name: str, default=None):
        try:
            return self.__dbus_props_iface.Get('org.bluez.Device1', prop_name)
        except Exception:
            return default

    def get_all_props(self):
        return self.__dbus_props_iface.GetAll('org.bluez.Device1')
