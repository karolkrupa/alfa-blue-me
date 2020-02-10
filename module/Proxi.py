import can
import asyncio

class Proxi:
    runing = True

    def __init__(self, bus: can.ThreadSafeBus, loop: asyncio.AbstractEventLoop):
        self.bus = bus
        self.loop = loop
        self.send_status_message()

    def on_message(self, msg: can.Message):
        if(msg.arbitration_id == 0x740):
            self.__send_proxi_message()

    def send_status_message(self):
        if self.runing:
            status_byte = 0x1F
        else:
            status_byte = 0x1A

        self.bus.send(can.Message(arbitration_id=0x707, data=[0x00, status_byte], extended_id=False))
        self.loop.call_later(1, self.send_status_message)

    def __send_proxi_message(self):
        self.bus.send(can.Message(arbitration_id=0x747, data=[0x21, 0x14, 0x00, 0x28, 0x65, 0x70], extended_id=False))
        self.runing = True
