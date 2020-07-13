import can
from module.ThreadModuleAbstract import ThreadModuleAbstract
import asyncio
from module.EventBus import mainEventBus


class StatusManager(ThreadModuleAbstract):
    media_player = False
    phone_connected = True
    menu_mode = False
    network_name = None
    _can_filters = [
        {
            "can_id": 0x545,
            "can_mask": 0x3FF,
            "extended": False
        }
    ]

    def __init__(self):
        super().__init__()

    def execute(self):
        asyncio.set_event_loop(self.loop)
        self.loop.call_soon(self.__send_status)
        self.loop.run_forever()

    def open_media_player(self):
        self.media_player = True

    def __send_status(self):
        self.bus.send(can.Message(arbitration_id=0x3E7, data=self.__create_status_frame(), extended_id=False))
        self.loop.call_later(1, self.__send_status)

    def __create_status_frame(self):
        data = self.__get_network_name_bytes()
        data += self.__get_status_byte()
        data += self.__get_media_player_byte()
        return data

    def __get_network_name_bytes(self):
        # if self.network_name is None:
        return bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        # else:
        #     text = self.network_name[0 + 6]
        #     frames = TextEncoder.encode(text)[0]
        #     for i in range(0, 7):
        #         if not bytes[i]: bytes[i] = 0x00
        #     return bytes

    def __get_status_byte(self):
        status = '0x'
        if self.phone_connected:
            status += 'C'
        else:
            status += '0'

        if self.menu_mode:
            status += '4'
        else:
            status += '0'

        return bytearray([int(status, 16)])

    def __get_media_player_byte(self):
        status = '0x'
        if self.phone_connected:
            status += '0'
        else:
            status += '8'

        if self.media_player:
            status += '4'
        else:
            status += '0'

        return bytearray([int(status, 16)])

    def _on_message(self, msg: can.Message):
        if msg.data == bytearray([0xE0, 0x00, 0x00, 0x00, 0x00, 0x00]):
            if not self.media_player:
                mainEventBus.trigger('status-manager:media-player-enabled', {'enabled': True})
            self.media_player = True
        elif msg.data == bytearray([0x58, 0x04, 0x0c, 0x00, 0x02, 0x00]):
            if self.media_player:
                mainEventBus.trigger('status-manager:media-player-enabled', {'enabled': False})
            self.media_player = False



status_manager = StatusManager()
status_manager.run()
