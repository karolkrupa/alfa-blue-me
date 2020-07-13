from module.ThreadModuleAbstract import ThreadModuleAbstract
from bluetooth.Manger import defaultManger


class DeviceScanner(ThreadModuleAbstract):
    def execute(self):
        self.connect_to_available_devices()
        self.loop.run_forever()

    def connect_to_available_devices(self):
        deviceManager = defaultManger.get_device_manager()
        defaultManger.get_adapter().start_discovery()

        for device in deviceManager.get_devices():
            rssi = device.get_rssi()
            if rssi and rssi > -70 and not device.is_connected():
                defaultManger.get_adapter().stop_discovery()
                device.connect()
                return

        self.loop.call_later(3, self.connect_to_available_devices)
