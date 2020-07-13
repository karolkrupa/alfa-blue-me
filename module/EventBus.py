import uuid


class EventBus:
    callbacks: dict
    forwards: dict

    def __init__(self):
        self.callbacks = {}
        self.forwards = {}

    def __del__(self):
        self.off_all()

    def on(self, event_name: str, callback):
        print('ON')
        print(event_name)
        callback_id = str(uuid.uuid1())
        if event_name not in self.callbacks:
            self.callbacks[event_name] = {
                callback_id: callback
            }
        else:
            self.callbacks[event_name][callback_id] = callback

        return EventPointer(self, event_name, callback_id)

    def off(self, event_name: str, callback_id: str, event_pointer=None):
        if event_pointer:
            event_name = event_pointer.event_name
            callback_id = event_pointer.callback_id

        if event_name not in self.callbacks:
            return

        if callback_id not in self.callbacks[event_name]:
            return

        del self.callbacks[event_name][callback_id]

    def off_all(self):
        self.callbacks = {}
        self.forwards = {}

    def trigger(self, event_name: str, args: dict = {}):
        print(event_name)
        print(event_name in self.callbacks)
        if event_name in self.callbacks:
            for callback in self.callbacks[event_name].values():
                callback(args)

        for prefix, bus in self.forwards.items():
            bus.trigger(prefix + ':' + event_name, args)

    def add_forwarding(self, prefix: str, bus):
        self.forwards[prefix] = bus

    def remove_forwarding(self, prefix: str):
        if prefix in self.forwards:
            del self.forwards[prefix]


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
