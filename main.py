import module.A2DP
import device.SteeringWheel
import device.Radio
from bluetooth.Manger import defaultManger
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

defaultManger.run_device_manager()

mainloop = GObject.MainLoop()
mainloop.run()
