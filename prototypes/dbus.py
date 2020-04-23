import dbus

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

bus = dbus.SystemBus();


def on_dbus_property_changed(self, interface, changed, invalidated):
    print(interface)


obj = bus.get_object('org.bluez', "/")
mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
for path, ifaces in mgr.GetManagedObjects().items():
    print(path)
    adapter = ifaces.get('org.bluez.MediaPlayer1')
    if not adapter:
        continue
bus.add_signal_receiver(
    on_dbus_property_changed,
    bus_name='org.bluez',
    signal_name='PropertiesChanged',
    dbus_interface='org.freedesktop.DBus.Properties'
)
