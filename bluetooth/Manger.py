from bluetooth.Agent import Agent
from bluetooth.Adapter import Adapter
from bluetooth.DeviceManager import DeviceManager

import dbus
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

AGENT_PATH = "/blueandme/agent"

class Manager:
    agent: Agent = None
    device_manager: DeviceManager = None
    adapter: Adapter = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.device_manager = DeviceManager()

    def register_agent(self):
        bus = dbus.SystemBus()
        self.agent = Agent(bus, AGENT_PATH)
        obj = bus.get_object("org.bluez", "/org/bluez");
        manager = dbus.Interface(obj, "org.bluez.AgentManager1")
        manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")
        manager.RequestDefaultAgent(AGENT_PATH)

    def run_device_manager(self):
        self.device_manager.find_all_devices()

    def get_device_manager(self):
        return self.device_manager

    def get_adapter(self) -> Adapter:
        return self.adapter

    def find_adapter(self):
        obj = dbus.SystemBus().get_object('org.bluez', "/")
        mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
        for path, ifaces in mgr.GetManagedObjects().items():
            adapter = ifaces.get('org.bluez.Adapter1')
            if not adapter:
                continue
            self.adapter = Adapter(path)
            return


defaultManger = Manager()
defaultManger.register_agent()
defaultManger.find_adapter()
# defaultManger.register_device_manager()

deviceManager = defaultManger.get_device_manager()
