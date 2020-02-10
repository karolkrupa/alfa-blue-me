import dbus, dbus.mainloop.glib, sys
from device.SteeringWheel import SteeringWheel
from device.InstrumentPanel import InstrumentPanel
from device.Radio import Radio, DisplayMode
from gi.repository import GLib
from module.ThreadModuleAbstract import ThreadModuleAbstract
import can
from utils.EventBus import eventBus
from threading import Thread
import asyncio
import time


class A2DP(ThreadModuleAbstract):
    player_connected = False
    glib_thread = None
    loop = None
    playing = False
    player_props = None
    player = None

    def __init__(self, bus: can.ThreadSafeBus,
                 steering_wheel: SteeringWheel,
                 instrument_panel: InstrumentPanel,
                 radio: Radio
                 ):
        super().__init__(bus)
        self.steering_wheel = steering_wheel
        self.instrument_panel = instrument_panel
        self.radio = radio

    @eventBus.on('test')
    def test(self):
        print('elo')

    def execute(self):
        asyncio.set_event_loop(self.loop)
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.register_dbus_listeners()
        self.find_media_player()
        self.find_media_player()
        self.loop.run_forever()

    def register_dbus_listeners(self):
        bus = dbus.SystemBus()
        bus.add_signal_receiver(
            self.on_dbus_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties'
        )
        self.__run_glib_loop(GLib.MainLoop())

    def __run_glib_loop(self, loop):
        self.glib_thread = Thread(target=loop.run)
        self.glib_thread.start()

    def on_dbus_property_changed(self, interface, changed, invalidated):
        if interface == 'org.bluez.MediaPlayer1':
            self.loop.call_soon_threadsafe(self.on_media_player_property_change, changed)
        elif interface == 'org.bluez.Device1':
            print('Device prop', changed.get('Connected'))
            if changed.get('Connected'):
                self.loop.call_soon_threadsafe(self.loop.call_later, 0.5, self.find_media_player)
            else:
                self.player_connected = False

    def find_media_player(self):
        print('FIND MEDIA PLAYER')
        bus = dbus.SystemBus()
        obj = bus.get_object('org.bluez', "/")
        mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
        for path, ifaces in mgr.GetManagedObjects().items():
            adapter = ifaces.get('org.bluez.MediaPlayer1')
            if not adapter:
                continue
            player = bus.get_object('org.bluez', path)
            self.player_connected = True
            self.player = dbus.Interface(player, dbus_interface='org.bluez.MediaPlayer1')
            self.player_props = dbus.Interface(player, "org.freedesktop.DBus.Properties")
            self.refresh_properties()
            # GLib.MainLoop().run()
            print('Player found')
            break
        if not adapter:
            print('Player not found')
            self.player_connected = False

    def refresh_properties(self):

        if self.player_connected:
            print('refresh')
            self.display_position(self.player_props.Get("org.bluez.MediaPlayer1", 'Position'))
        self.loop.call_later(1, self.refresh_properties)

    def display_position(self, position):
        minutes = position / 1000 / 60
        minutes_from_start = int(minutes)
        seconds_from_start = int((minutes - minutes_from_start) * 60)
        if minutes_from_start < 10:
            minutes_from_start = '0' + str(minutes_from_start)
        if seconds_from_start < 10:
            seconds_from_start = '0' + str(seconds_from_start)
        self.radio.time_minutes = minutes_from_start
        self.radio.time_seconds = seconds_from_start

    def on_media_player_property_change(self, changed):
        for prop, value in changed.items():
            if prop == 'Status':
                if value == 'playing':
                    self.playing = True
            elif prop == 'Track':
                if value.get('Title', ''):
                    self.display_track_name(value.get('Artist', ''), value.get('Title', ''))

    def display_track_name(self, artist, title, folder_name=''):
        if artist:
            self.radio.set_display_mode(DisplayMode.artists)
        else:
            self.radio.set_display_mode(DisplayMode.text)

        self.radio.set_first_field(artist)
        self.radio.set_second_filed(title)
        self.radio.display()

    @eventBus.on('SteeringWheel:next')
    def next(self):
        if not self.player_connected: return
        print('next')
        self.player.Next()

    @eventBus.on('SteeringWheel:prev')
    def prev(self):
        if not self.player_connected: return
        print('prev')
        self.player.Previous()

    def play(self):
        if not self.player_connected: return
        print('play')
        self.player.Play()

    def pause(self):
        if not self.player_connected: return
        print('pause')
        self.player.Pause()

    @eventBus.on('SteeringWheel:mute')
    def __play_pause(self):
        if not self.player_connected: return
        if not self.playing:
            self.play()
            print('play')
        else:
            self.pause()
            print('mute')
