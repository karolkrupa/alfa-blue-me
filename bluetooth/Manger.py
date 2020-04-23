import bluetooth
from bluetooth.Agent import Agent
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

    def register_agent(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        self.agent = Agent(bus, AGENT_PATH)
        obj = bus.get_object("org.bluez", "/org/bluez");
        manager = dbus.Interface(obj, "org.bluez.AgentManager1")
        manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")
        manager.RequestDefaultAgent(AGENT_PATH)

    def register_device_manager(self):
        self.device_manager = DeviceManager()