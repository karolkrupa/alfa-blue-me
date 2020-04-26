from device.ThreadedDevice import ThreadedDevice
import utils.TextEncoder as TextEncoder
from enum import Enum
from module.EventBus import mainEventBus


class DisplayMode(Enum):
    folder = 0x48
    artists = 0x50
    text = 0x40
    genres = 0x58
    albums = 0x60
    playlists = 0x68


class Radio(ThreadedDevice):
    first_field = ''
    second_field = ''
    time_minutes = None
    time_seconds = None
    display_mode = DisplayMode.text
    _can_filters = [
        {
            "can_id": 0x405,
            "can_mask": 0x3FF,
            "extended": False
        }
    ]

    def _execute(self):
        self.display_time()
        super()._execute()

    def set_display_mode(self, display_mode: DisplayMode):
        self.display_mode = display_mode

    def set_first_field(self, folder_name):
        self.first_field = folder_name[:8]

    def set_second_filed(self, title_text):
        self.second_field = title_text

    def _on_message(self, msg):
        if msg.data == bytearray([0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]):
            mainEventBus.trigger('radio:open-media-player')

    def display(self):
        if self.display_mode is DisplayMode.folder:
            text = "{}\n{}".format(self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.artists:
            if len(self.first_field + self.first_field + self.second_field) > 53:
                self.second_field = self.second_field[:(53 - len(self.first_field) * 2)]
            text = "{}\n{}\n{}".format(self.first_field, self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.genres:
            text = "{}\n{}".format(self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.albums:
            text = "{}\n{}".format(self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.playlists:
            text = "{}\n{}".format(self.first_field, self.second_field)
        else:
            text = (self.first_field + self.second_field)[:26]
            text = "\n{}\n{}".format(text, text)

        frames = TextEncoder.encode(text, 0x2A)
        self.send_frames(0x5E7, [[0x00, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]])
        self.send_frames(0x5E7, frames)

    def display_time(self):
        if self.time_minutes is None or self.time_seconds is None:
            self.send_frames(0x427, [[0x00, 0x00, 0xC8, 0x78, 0x00, 0x00, 0x00, 0x00]])
        else:
            self.send_frames(0x427, [[int('0x' + str(self.time_minutes), 16), int('0x' + str(self.time_seconds), 16), self.display_mode.value, 0x78, 0x00, 0x00, 0x00, 0x00]])
        self._loop.call_later(1, self.display_time)

# 48 - Folders Nazwa folderu<field spearator>Tytul
# 50 - Artists Artysta <field separator> Artysta <field separator> Tytul Na artyscie miesci sie 13 znakow i 14 uciety
# 40 - nic - Zaczyna sie o field separatora (Działa bez?), Tekst<field separator>Tekst
# 58 - Generes Gatunek<field separator>Tekst
# 60 - Albums Album<field separator>Tekst
# 68 - Playlists
# 70 nic


radio = Radio()
radio.run()
