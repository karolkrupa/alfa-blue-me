from device.ThreadedDevice import ThreadedDevice
import utils.TextEncoder as TextEncoder
from enum import Enum
from utils.EventBus import eventBus
import asyncio


class DisplayMode(Enum):
    folder = 0x48
    artists = 0x50
    text = 0x40
    genres = 0x58
    albums = 0x60
    playlists = 0x68


class Radio(ThreadedDevice):
    arbitration_ids = [0x405]
    first_field = ''
    second_field = ''
    time_minutes = None
    time_seconds = None
    display_mode = DisplayMode.text

    def execute(self):
        asyncio.set_event_loop(self.loop)
        self.display_time()
        self.loop.run_forever()

    def set_display_mode(self, display_mode: DisplayMode):
        self.display_mode = display_mode

    def set_first_field(self, folder_name):
        self.first_field = folder_name

    def set_second_filed(self, title_text):
        self.second_field = title_text

    def __received_message(self, msg):
        if msg.data == bytearray([0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]):
            eventBus.emit('Radio:open_media_player')

    def display(self):
        if self.display_mode is DisplayMode.folder:
            text = "{}\n{}".format(self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.artists:
            text = "{}\n{}\n{}".format(self.first_field, self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.genres:
            text = "{}\n{}".format(self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.albums:
            text = "{}\n{}".format(self.first_field, self.second_field)
        elif self.display_mode is DisplayMode.playlists:
            text = "{}\n{}".format(self.first_field, self.second_field)
        else:
            text = "{}\n{}".format(self.second_field, self.second_field)

        frames = TextEncoder.encode(text, 0x2A)
        self.send_frames(0x5E7, frames)

    def display_time(self):
        if self.time_minutes is None or self.time_seconds is None:
            self.send_frames(0x427, [[0x00, 0x00, 0xC8, 0x78, 0x00, 0x00, 0x00, 0x00]])
        else:
            self.send_frames(0x427, [[int('0x' + str(self.time_minutes), 16), int('0x' + str(self.time_seconds), 16), 0x50, 0x78, 0x00, 0x00, 0x00, 0x00]])
        self.loop.call_later(1, self.display_time)


# 48 - Folders Nazwa folderu<field spearator>Tytul
# 50 - Artists Artysta <field separator> Artysta <field separator> Tytul Na artyscie miesci sie 13 znakow i 14 uciety
# 40 - nic - Zaczyna sie o field separatora (Działa bez?), Tekst<field separator>Tekst
# 58 - Generes Gatunek<field separator>Tekst
# 60 - Albums Album<field separator>Tekst
# 68 - Playlists
# 70 nic