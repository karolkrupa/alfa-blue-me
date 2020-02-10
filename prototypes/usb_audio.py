import can
import asyncio
import time


can0 = can.ThreadSafeBus(channel = 'can0', bustype = 'socketcan_ctypes')

loop = asyncio.get_event_loop()

ready = False
przelaczone = False
def on_message(msg: can.Message):
    global przelaczone
    if(msg.arbitration_id == 0x405 and msg.data == bytearray([0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) and not przelaczone):
        # 747#21 14 00 28 65 70
        # proxiMsg = can.Message(arbitration_id=0x545, data=[0xE0, 0x00, 0x00, 0x00, 0x00, 0x00], extended_id=False)
        # can0.send(proxiMsg)
        title = can.Message(arbitration_id=0x5E7, data=[0x00, 0x2A, 0x30, 0xdf, 0xce, 0x3c, 0x00, 0x00], extended_id=False)
        can0.send(title)
        global ready
        ready = True
        print('przelacza')
        przelaczone = True

counter = 0;
def send_status():
    global ready
    global counter
    if not ready:
        # statusMsg = can.Message(arbitration_id=0x545, data=[0x58, 0x04, 0x0C, 0x00, 0x02, 0x00], extended_id=False)
        trackMsg = can.Message(arbitration_id=0x427, data=[0x00, 0x00, 0xC8, 0x78, 0x00, 0x00, 0x00, 0x00], extended_id=False)
        statusMsg2 = can.Message(arbitration_id=0x3E7, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80],
                                 extended_id=False)
    else:
        statusMsg = can.Message(arbitration_id=0x545, data=[0x58, 0x04, 0x0C, 0x00, 0x02, 0x00], extended_id=False)
        can0.send(statusMsg)
        # statusMsg = can.Message(arbitration_id=0x545, data=[0xE0, 0x00, 0x00, 0x00, 0x02, 0x00], extended_id=False)
        trackMsg = can.Message(arbitration_id=0x427, data=[0x00, int('0x0' + str(counter), 16), 0x40, 0x78, 0x00, 0x00, 0x00, 0x00], extended_id=False)
        statusMsg2 = can.Message(arbitration_id=0x3E7, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x84],
                                 extended_id=False)
        counter += 1
    # can0.send(statusMsg)


    can0.send(statusMsg2)
    can0.send(trackMsg)

    loop.call_later(0.95, send_status)

can.Notifier(can0, [
    on_message
], loop=loop)

loop.call_soon(send_status)
loop.run_forever()

