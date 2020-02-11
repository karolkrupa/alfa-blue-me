from device.Device import Device
from enum import Enum
from utils.EventBus import eventBus


# 3C4 80 00 - VOL UP
# 3C4 40 00 - VOL DOWN
# 3C4 10 00 - Prawo
# 3C4 08 00 - Lewo
# 3C4 10 01 - Dół
# 3C4 08 02 - Góra
# 3C4 04 00 - SRC
# 3C4 00 40 - Windows
# 3C4 20 00 - Mute
# 3C4 00 80 - Menu

class Button(Enum):
    vol_up = 'vol_up'
    vol_down = 'vol_down'
    next = 'next'
    prev = 'prev'
    up = 'up'
    down = 'down'
    src = 'src'
    win = 'win'
    mute = 'mute'
    menu = 'menu'
    none = 'none'


buttons_binding = {
    bytearray([0x00, 0x00]).hex(): Button.none,
    bytearray([0x80, 0x00]).hex(): Button.vol_up,
    bytearray([0x40, 0x00]).hex(): Button.vol_down,
    bytearray([0x10, 0x00]).hex(): Button.next,
    bytearray([0x08, 0x00]).hex(): Button.prev,
    bytearray([0x08, 0x02]).hex(): Button.up,
    bytearray([0x10, 0x01]).hex(): Button.down,
    bytearray([0x04, 0x00]).hex(): Button.src,
    bytearray([0x00, 0x40]).hex(): Button.win,
    bytearray([0x20, 0x00]).hex(): Button.mute,
    bytearray([0x00, 0x80]).hex(): Button.menu
}


class SteeringWheel(Device):
    arbitration_ids = [0x3C4]

    def __received_message(self, msg):
        self.__on_button_click(buttons_binding[msg.data.hex()])

    def on_message(self, msg):
        if msg.arbitration_id in self.arbitration_ids:
            self.__received_message(msg)

    def __on_button_click(self, button):
        if button is Button.none:
            return None
        eventBus.emit('SteeringWheel:' + button)