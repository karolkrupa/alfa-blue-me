from device.Device import Device
import utils.TextEncoder as TextEncoder
from module.StatusManager import status_manager
from device.InstrumentPanel.Menu import Menu
from module.EventBus import mainEventBus
import time


class Screen(Device):
    _menu = None
    _default_menu_layer = None

    def __init__(self):
        super().__init__()
        self._menu = Menu(self)
        mainEventBus.on('steering-wheel:menu', self._show_menu_callback)

    def get_menu(self):
        return self._menu

    def register_default_menu_layer(self, layer):
        self._default_menu_layer = layer
        self.get_menu().set_menu_layer(layer)

    def _show_menu_callback(self, args):
        if not self._menu.is_active:
            self._menu.set_menu_layer(self._default_menu_layer)
            self._menu.show()

    def display(self, text, sleep):
        frames = TextEncoder.encode(text, 0x02)
        self.send_frames(0x5E7, frames)
        if sleep:
            time.sleep(sleep)
            self.__back_to_last_state()

    def display_text_center(self, text, sleep=None):
        self.display(' \n' + text, sleep)

    def __back_to_last_state(self):
        if self._menu.is_active:
            self.display_menu()
        else:
            self.clear()

    def display_menu(self):
        self._menu.set_is_active(True)
        frames = self._menu.get_frames()
        status_manager.menu_mode = True
        self.send_frames(0x5E7, frames)

    def clear(self):
        self.send_frames(0x5E7, [[0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]])


screen = Screen()
