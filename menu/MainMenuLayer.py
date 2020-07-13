from menu.AbstractMenuLayer import AbstractMenuLayer
from menu.Bluetooth.SettingsLayer import settingsLayer


class MainMenuLayer(AbstractMenuLayer):
    _elements = {
        'bt-settings': 'BT Settings',
        'media-settings': 'Media\nSettings'
    }

    __menu_layers = {

    }

    def on_show(self):
        pass

    def on_select(self, element) -> AbstractMenuLayer:
        if element == 'bt-settings':
            return settingsLayer


mainMenuLayer = MainMenuLayer()
