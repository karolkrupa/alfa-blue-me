import utils.TextEncoder as TextEncoder
from module.EventBus import mainEventBus
from enum import Enum
from menu.AbstractMenuLayer import AbstractMenuLayer


class MenuType(Enum):
    full = 0x04
    top = 0x08
    bottom = 0x1C


class Menu:
    _elements: dict
    _elements_array: []
    _active_element_index: int = None
    _menu_type: MenuType = MenuType.full

    _menu_layer: AbstractMenuLayer = None

    _top_text: str = ''
    _bottom_text: str = ''

    is_active = False

    __event_pointers: []

    _screen = None

    _history: []

    def __init__(self, screen):
        self._history = []
        self._screen = screen
        self._active_element_index = None
        self._elements = {}
        self.__event_pointers = []
        self.__event_pointers.append(
            mainEventBus.on('steering-wheel:down', self._scroll_down_callback)
        )
        self.__event_pointers.append(
            mainEventBus.on('steering-wheel:up', self._scroll_up_callback)
        )
        self.__event_pointers.append(
            mainEventBus.on('steering-wheel:menu', self._select_callback)
        )
        self.__event_pointers.append(
            mainEventBus.on('steering-wheel:win', self._back_callback)
        )

    def __del__(self):
        for pointer in self.__event_pointers:
            pointer.off()

    def set_menu_type(self, menu_type: MenuType):
        self._menu_type = menu_type

    def set_menu_layer(self, layer):
        self._menu_layer = layer

    def show(self):
        self._menu_layer.on_show()
        self.set_elements(self._menu_layer.get_elements())
        self._render()

    def _render(self):
        self._screen.display_menu()

    def hide(self):
        self._history = []
        self.set_is_active(False)
        self._screen.clear()

    def set_elements(self, elements: dict):
        self._elements = elements
        self._elements_array = list(elements.values())
        self._active_element_index = 0

    def add_element(self, key, name):
        self._elements[key] = name

    def get_elements(self):
        return self._elements

    def get_frames(self):
        if self._menu_type == MenuType.full:
            text = self.__get_text_full_menu()
        elif self._menu_type == MenuType.bottom:
            text = self.__get_text_bottom_menu()
        else:
            text = self.__get_text_top_menu()

        return TextEncoder.encode(text, self._menu_type.value)

    def __get_text_full_menu(self):
        first_element = self._elements_array[self._active_element_index]
        text = ''
        if first_element.count('\n') < 1:
            text = ' \n' + first_element + '\n'
        else:
            text = first_element + '\n'

        return text + self._get_next_element()

    def __get_text_bottom_menu(self):
        text = ''
        if self._top_text.count('\n') < 1:
            text += '\n' + self._top_text + '\n'
        else:
            text += self._top_text + '\n'

        return text + self._elements_array[self._active_element_index]

    def __get_text_top_menu(self):
        text = ''
        element_text = self._elements_array[self._active_element_index]
        if element_text.count('\n') < 1:
            text += '\n' + element_text + '\n'
        else:
            text += element_text + '\n'

        return text + self._bottom_text

    def set_is_active(self, active=False):
        self.is_active = active

    def _get_next_element(self, position = 1):
        given_index = self._active_element_index + position
        max_index = len(self._elements_array)-1
        if max_index >= given_index:
            return self._elements_array[given_index]
        return ''

    def scroll_down(self):
        if not self.is_active:
            return
        max_index = len(self._elements_array) - 1
        given_index = self._active_element_index + 1
        if max_index >= given_index and self._active_element_index != given_index:
            self._active_element_index = given_index
            self._render()

    def scroll_up(self):
        if self._active_element_index > 0:
            self._active_element_index -= 1
            self._render()

    def _scroll_up_callback(self, args):
        if self.is_active:
            self.scroll_up()

    def _scroll_down_callback(self, args):
        if self.is_active:
            self.scroll_down()

    def _select_callback(self, args):
        if self.is_active:
            newLayer = self._menu_layer.on_select(self.__get_active_element_key())
            if isinstance(newLayer, AbstractMenuLayer):
                self._history.append(self._menu_layer)
                self.set_menu_layer(newLayer)
                self.show()
            elif isinstance(newLayer, str):
                self._screen.display(newLayer, 4)

    def __get_active_element_key(self):
        return list(self._elements.keys())[self._active_element_index]

    def _back_callback(self, args):
        try:
            newLayer = self._history.pop()
            self.set_menu_layer(newLayer)
            self.show()
        except IndexError:
            self.hide()
