import uuid


class EventBus:
    callbacks: dict = {}

    def on(self, event_name: str, callback):
        callback_id = str(uuid.uuid1())
        if event_name not in self.callbacks:
            self.callbacks[event_name] = {
                callback_id: callback
            }
        else:
            self.callbacks[event_name][callback_id] = callback

        return EventPointer(self, event_name, callback_id)

    def off(self, event_name: str, callback_id: str, event_pointer = None):
        if event_pointer:
            event_name = event_pointer.event_name
            callback_id = event_pointer.callback_id

        if event_name not in self.callbacks:
            return

        if callback_id not in self.callbacks[event_name]:
            return

        del self.callbacks[event_name][callback_id]

    def trigger(self, event_name: str, args: dict = {}):
        if event_name not in self.callbacks:
            return

        for callback in self.callbacks[event_name].values():
            callback(args)


class EventPointer:
    bus: EventBus
    event_name: str
    callback_id: str

    def __init__(self, bus: EventBus, event_name: str, callback_id: str):
        self.bus = bus
        self.event_name = event_name
        self.callback_id = callback_id

    def off(self):
        self.bus.off(event_pointer=self)


mainEventBus = EventBus()
