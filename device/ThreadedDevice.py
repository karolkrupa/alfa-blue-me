import asyncio
from event_bus import EventBus
from device.Device import Device
from threading import Thread


class ThreadedDevice(Device):
    loop: asyncio.AbstractEventLoop = None
    thread: Thread = None

    def __init__(self, bus):
        super().__init__(bus)
        self.loop = asyncio.new_event_loop()

    def run(self):
        self.thread = Thread(target=self.execute)
        self.thread.start()

    def execute(self):
        pass
