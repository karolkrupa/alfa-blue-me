import asyncio
import time
from threading import Thread
import can
from device.Device import Device


class ThreadedDevice(Device):
    _loop: asyncio.AbstractEventLoop = None
    _thread: Thread = None
    _notifier: can.Notifier

    def __init__(self):
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self.__register_notifier()

    def run(self):
        self._thread = Thread(target=self._execute)
        # self._thread.daemon = True
        self._thread.start()

    def _execute(self):
        self._loop.run_forever()

    def _on_message(self, msg: can.Message):
        pass

    def __register_notifier(self):
        self._notifier = can.Notifier(self._can, [
            self._on_message
        ], loop=self._loop)
