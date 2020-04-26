import can
from module.ThreadModuleAbstract import ThreadModuleAbstract
from module.EventBus import mainEventBus
import asyncio


class StatusManager(ThreadModuleAbstract):
    media_player = False
    phone_connected = False
    network_name = None

    def __init__(self, bus):
        super().__init__(bus)

    def execute(self):
        asyncio.set_event_loop(self.loop)
        self.loop.call_soon(self.__send_status)
        self.loop.run_forever()

    # def on_message(self, msg: can.Message):
    #     if msg.arbitration_id == 0x405 and msg.data == bytearray([0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]):
    #         self.media_player = True

    # def __get_status_data(self):
    #     if self.media_player:
    #         return [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x84]
    #     return [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80]

    # @eventBus.on('Radio:open_media_player')
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
        if self.phone_connected: return bytearray([0x0C])
        else: return bytearray([0x00])

    def __get_media_player_byte(self):
        if self.media_player:
            return bytearray([0x84])
        else:
            return bytearray([0x80])
