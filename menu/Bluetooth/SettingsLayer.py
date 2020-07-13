from menu.AbstractMenuLayer import AbstractMenuLayer
from menu.Bluetooth.DevicesLayer import devicesLayer
from bluetooth.Manger import defaultManger


class SettingsLayer(AbstractMenuLayer):
    _elements = {
        'devices': 'Devices',
        'discoverable': 'Discoverable'
    }

    def on_show(self):
        pass

    def on_select(self, element) -> AbstractMenuLayer:
        if element == 'devices':
            return devicesLayer
        if element == 'discoverable':
            return self._make_discoverable()

    def _make_discoverable(self):
        adapter = defaultManger.get_adapter()

        adapter.set_discoverable(True)

        return "Discoverable\nfor 3min"


settingsLayer = SettingsLayer()
