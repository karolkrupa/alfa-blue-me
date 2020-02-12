import can
import time


class Device:
    arbitration_ids = []

    def __init__(self, bus):
        self.bus = bus

    def send_frames(self, id, frames: [[]]):
        for frame in frames:
            self.bus.send(can.Message(arbitration_id=id, data=frame, extended_id=False))
            time.sleep(0.01)

    def on_message(self, msg: can.Message):
        if msg.arbitration_id in self.arbitration_ids:
            self.__received_message(msg)

    def __received_message(self, msg):
        pass
