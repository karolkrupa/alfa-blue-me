from menu.AbstractMenuLayer import AbstractMenuLayer
from bluetooth.Manger import defaultManger
from menu.Bluetooth.DeviceLayer import deviceLayer


class DevicesLayer(AbstractMenuLayer):
    _elements = {}

    __devices = {}

    def on_show(self):
        self._load_devices()

    def on_select(self, element) -> AbstractMenuLayer:
        deviceLayer.set_device(self.__devices[element])
        return deviceLayer

    def _load_devices(self):
        device_manager = defaultManger.get_device_manager()
        for device in device_manager.get_devices():
            self._elements[device.get_address()] = device.get_name()
            self.__devices[device.get_address()] = device


devicesLayer = DevicesLayer()
