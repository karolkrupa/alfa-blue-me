from module.EventBus import EventBus
import dbus


class Player:
    __path: str
    __player_object = None
    __player_iface = None
    __props_iface = None
    event_bus: EventBus = EventBus()

    def __init__(self, player_path):
        self.__path = player_path
        self.__player_object = dbus.SystemBus().get_object('org.bluez', player_path)
        self.__player_object.connect_to_signal(
            'PropertiesChanged',
            self.__properties_changed_callback,
            dbus_interface='org.freedesktop.DBus.Properties'
        )
        self.__player_iface = dbus.Interface(self.__player_object, 'org.bluez.MediaControl1')
        self.__props_iface = dbus.Interface(self.__player_object, 'org.freedesktop.DBus.Properties')

    def play(self):
        self.__player_iface.Play()

    def pause(self):
        self.__player_iface.Pause()

    def stop(self):
        self.__player_iface.Stop()

    def next(self):
        self.__player_iface.next()

    def previous(self):
        self.__player_iface.Previous()

    def fastForward(self):
        self.__player_iface.FastForward()

    def rewind(self):
        self.__player_iface.Rewind()

    def __properties_changed_callback(self, interface, changed: dict, invalidated):
        self.event_bus.trigger('properties-changed', changed)