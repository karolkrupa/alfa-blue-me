import dbus.mainloop.glib, sys
from gi.repository import GLib
import can
from prototypes import text_encoder
import time

def sendToNav(text):
    frames = text_encoder.encode(text, 0x2A)
    for frame in frames:
        can0.send(can.Message(arbitration_id=0x5E7, data=frame, extended_id=False))
        time.sleep(0.05)

def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':
            if value.get('Title', ''):
                sendToNav('a\n{}: {}'.format(value.get('Artist', ''), value.get('Title', '')))


def on_playback_control(msg):
    if msg.data == bytearray([0x20,0x00]):
        player_iface.Play()
    elif msg.data == bytearray([0x20,0x00]):
        player_iface.Pause()
    elif msg.data == bytearray([0x10,0x00]):
        player_iface.Next()
    elif msg.data == bytearray([0x08,0x00]):
        player_iface.Previous()
    return True

can0 = can.Bus(channel='can0', bustype='socketcan_ctypes')

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    obj = bus.get_object('org.bluez', "/")
    mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
    for path, ifaces in mgr.GetManagedObjects().items():
        adapter = ifaces.get('org.bluez.MediaPlayer1')
        if not adapter:
            continue
        player = bus.get_object('org.bluez', path)
        player_iface = dbus.Interface(player, dbus_interface='org.bluez.MediaPlayer1')
        break
    if not adapter:
        sendToNav('AB\nCDD')
        sys.exit('Error: Media Player not found.')


    bus.add_signal_receiver(
        on_property_changed,
        bus_name='org.bluez',
        signal_name='PropertiesChanged',
        dbus_interface='org.freedesktop.DBus.Properties')

    # listeners = [
    #     on_playback_control  # Callback function
    # ]
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    # loop = asyncio.get_event_loop()
    # notifier = can.Notifier(can0, listeners, loop=loop)
    # loop.run_forever()

    # GLib.io_add_watch(sys.stdin, GLib.IO_IN, on_playback_control)
    GLib.MainLoop().run()