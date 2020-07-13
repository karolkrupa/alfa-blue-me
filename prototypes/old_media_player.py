import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import asyncio
import math
from multiprocessing import Process


def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        # print(prop)
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':

            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))
        elif prop == 'Position':
            print(BT_Media_props.Get("org.bluez.MediaPlayer1", 'Position'))

def get_props():
    # secondsFromStart = BT_Media_props.Get("org.bluez.MediaPlayer1", 'Position')/1000
    minutes = BT_Media_props.Get("org.bluez.MediaPlayer1", 'Position')/1000/60
    minutesFromStart = int(minutes)
    secondsFromStart = int((minutes - minutesFromStart) * 60)
    print('{}:{}'.format(minutesFromStart, secondsFromStart))
    loop.call_later(1, get_props)

def on_playback_control(fd, condition):
    str = fd.readline()
    if str.startswith('play'):
        player_iface.Play()
    elif str.startswith('pause'):
        player_iface.Pause()
    elif str.startswith('next'):
        player_iface.Next()
    elif str.startswith('prev'):
        player_iface.Previous()
    return True


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    bus.add_signal_receiver(
        on_property_changed,
        bus_name='org.bluez',
        signal_name='PropertiesChanged',
        dbus_interface='org.freedesktop.DBus.Properties')
    GLib.MainLoop().run()
    obj = bus.get_object('org.bluez', "/")
    mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
    for path, ifaces in mgr.GetManagedObjects().items():
        adapter = ifaces.get('org.bluez.MediaPlayer1')
        if not adapter: continue
        player = bus.get_object('org.bluez', path)
        player_iface = dbus.Interface(
            player,
            dbus_interface='org.bluez.MediaPlayer1')
        BT_Media_props = dbus.Interface(player, "org.freedesktop.DBus.Properties")
        break
    if not adapter:
        sys.exit('Error: Media Player not found.')

    # bus.add_signal_receiver(
    #     on_property_changed,
    #     bus_name='org.bluez',
    #     signal_name='PropertiesChanged',
    #     dbus_interface='org.freedesktop.DBus.Properties')
    GLib.io_add_watch(sys.stdin, GLib.IO_IN, on_playback_control)
    print('before')
    loop = asyncio.get_event_loop()

    # GLib.MainLoop().run()

    print('after')

    loop.call_soon(get_props)
    print('run forever')

    loop.run_forever()

    print('exit')