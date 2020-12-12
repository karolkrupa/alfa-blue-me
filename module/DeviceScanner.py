from module.ThreadModuleAbstract import ThreadModuleAbstract
from bluetooth.Manger import defaultManger
from dbus.exceptions import DBusException


class DeviceScanner(ThreadModuleAbstract):
    def execute(self):
        self.loop.run_forever()

    def connect_to_available_device(self):
        if self._has_active_device():
            if defaultManger.get_adapter().is_discovering():
                defaultManger.get_adapter().stop_discovery()
            return

        deviceManager = defaultManger.get_device_manager()
        if not defaultManger.get_adapter().is_discovering():
            defaultManger.get_adapter().start_discovery()

        for device in deviceManager.get_devices():
            rssi = device.get_rssi()
            # print('DEVICES')
            # print(device.get_address())
            # print(device.is_paired())
            # print(rssi)
            # print('----------')
            if rssi and rssi > -70 and not device.is_connected() and device.is_paired():
                if defaultManger.get_adapter().is_discovering():
                    defaultManger.get_adapter().stop_discovery()
                device.connect()
                return

            if device.is_paired():
                try:
                    device.connect()
                except DBusException:
                    pass

        self.loop.call_later(3, self.connect_to_available_device)

    def _has_active_device(self):
        return defaultManger.get_device_manager().has_active_device()


deviceScanner = DeviceScanner()
