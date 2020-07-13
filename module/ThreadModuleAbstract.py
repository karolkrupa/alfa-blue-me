import can
from threading import Thread
import asyncio
import settings


class ThreadModuleAbstract:
    thread = None
    bus: can.ThreadSafeBus = None
    loop: asyncio.AbstractEventLoop = None
    _can_filters: [] = None

    def __init__(self):
        self.bus = self._can = can.ThreadSafeBus(
            channel=settings.CAN_INTERFACE,
            bustype='socketcan_ctypes',
            can_filters=self._can_filters
        )
        self.__register_notifier()
        self.loop = asyncio.new_event_loop()

    def run(self):
        self.thread = Thread(target=self.execute)
        self.thread.daemon = True
        self.thread.start()

    def execute(self):
        pass

    def _on_message(self, msg: can.Message):
        pass

    def __register_notifier(self):
        self._notifier = can.Notifier(self.bus, [
            self._on_message
        ], loop=self.loop)
