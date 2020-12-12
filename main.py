import os

# os.system("sudo ip link set can0 type can bitrate 50000")
# os.system("sudo ifconfig can0 up")

# os.system("sudo ip link add dev vcan0 type vcan")
# os.system("sudo ip link set up vcan0")
# os.system("sudo ip link set up vcan0")

from module.StatusManager import status_manager
from bluetooth.Manger import defaultManger
import device.SteeringWheel
import module.A2DP
import device.Radio
from device.InstrumentPanel.Screen import screen
from module.DeviceScanner import deviceScanner

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

defaultManger.run_device_manager()

from menu.MainMenuLayer import mainMenuLayer

screen.register_default_menu_layer(mainMenuLayer)

screen.display_text_center("BM Connected", 3)

if not defaultManger.get_device_manager().has_active_device():
    deviceScanner.connect_to_available_device()

deviceScanner.run()

mainloop = GObject.MainLoop()
mainloop.run()
