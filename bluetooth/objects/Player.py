from module.EventBus import EventBus
import dbus


class Player:
    __path: str
    __player_object = None
    __player_iface = None
    __props_iface = None
    event_bus: EventBus

    def __init__(self, player_path: str):
        self.event_bus = EventBus()
        self.__path = player_path
        self.__player_object = dbus.SystemBus().get_object('org.bluez', player_path)
        self.__player_object.connect_to_signal(
            'PropertiesChanged',
            self.__properties_changed_callback,
            dbus_interface='org.freedesktop.DBus.Properties'
        )
        self.__player_iface = dbus.Interface(self.__player_object, 'org.bluez.MediaPlayer1')
        self.__props_iface = dbus.Interface(self.__player_object, 'org.freedesktop.DBus.Properties')

    def __del__(self):
        self.event_bus.off_all()
        del self.event_bus

    def play(self):
        self.__player_iface.Play()

    def pause(self):
        self.__player_iface.Pause()

    def stop(self):
        self.__player_iface.Stop()

    def next(self):
        self.__player_iface.Next()

    def previous(self):
        self.__player_iface.Previous()

    def fastForward(self):
        self.__player_iface.FastForward()

    def rewind(self):
        self.__player_iface.Rewind()

    def is_playing(self):
        status = self.get_prop('Status')
        return status == 'playing'

    def get_prop(self, name: str):
        try:
            return self.__props_iface.Get('org.bluez.MediaPlayer1', name)
        except dbus.exceptions.DBusException:
            return None

    def get_all_props(self):
        return self.__props_iface.GetAll('org.bluez.MediaPlayer1')

    def __properties_changed_callback(self, interface, changed: dict, invalidated):
        self.event_bus.trigger('properties-changed', {
            'changed': changed
        })
