import can
import asyncio
import time


can0 = can.ThreadSafeBus(channel = 'can0', bustype = 'socketcan_ctypes')

loop = asyncio.get_event_loop()

ready = False

def on_message(msg: can.Message):
    if(msg.arbitration_id == 0x740):
        # 747#21 14 00 28 65 70
        proxiMsg = can.Message(arbitration_id=0x747, data=[0x21, 0x14, 0x00, 0x28, 0x65, 0x70], extended_id=False)
        can0.send(proxiMsg)
        global ready
        ready = True


def send_status():
    global ready
    if not ready:
        statusMsg = can.Message(arbitration_id=0x707, data=[0x00, 0x1A], extended_id=False)
    else:
        statusMsg = can.Message(arbitration_id=0x707, data=[0x00, 0x1E], extended_id=False)
    can0.send(statusMsg)
    loop.call_later(0.95, send_status)

can.Notifier(can0, [
    on_message
], loop=loop)

loop.call_soon(send_status)
loop.run_forever()

