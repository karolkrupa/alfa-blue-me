from threading import Thread
import can
from event_bus import EventBus
import asyncio


class ThreadModuleAbstract:
    thread = None
    bus: can.ThreadSafeBus = None

    def __init__(self, bus: can.ThreadSafeBus):
        self.bus = bus
        self.loop = asyncio.new_event_loop()

    def run(self):
        self.thread = Thread(target=self.execute)
        self.thread.start()

    def execute(self):
        pass
