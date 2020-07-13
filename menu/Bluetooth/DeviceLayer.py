from menu.AbstractMenuLayer import AbstractMenuLayer
from device.InstrumentPanel.Screen import screen
from bluetooth.objects.Device import Device
from bluetooth.Manger import defaultManger


class DeviceLayer(AbstractMenuLayer):
    _elements = {
        'activate': 'Activate'
    }

    __device: Device

    def set_device(self, device):
        self.__device = device

    def on_show(self):
        pass

    def on_select(self, element):
        if element == 'activate':
            return self._activate_device()

        return None

    def _activate_device(self):
        if not self.__device.is_connected():
            return 'Device\ndisconnected'

        deviceManager = defaultManger.get_device_manager()

        if deviceManager.get_active_device() == self.__device:
            return "Device\nis\nactive"

        defaultManger.get_device_manager().set_active_device(self.__device)

        return "Activated"


deviceLayer = DeviceLayer()
