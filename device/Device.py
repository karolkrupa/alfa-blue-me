import can
import time
import settings


class Device:
    _can: can.ThreadSafeBus
    _can_filters: [] = None

    def __init__(self):
        self._can = can.ThreadSafeBus(
            channel=settings.CAN_INTERFACE,
            bustype='socketcan_ctypes',
            can_filters=self._can_filters
        )

    def send_frames(self, id, frames: [[]]):
        for frame in frames:
            self._can.send(can.Message(arbitration_id=id, data=frame, extended_id=False))
            time.sleep(0.01)
