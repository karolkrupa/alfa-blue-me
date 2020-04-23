import can
import asyncio
from bitstring import BitArray
from bitstring import Bits
import utils.TextDecoder as TextDecoder
import keyboard

can0 = can.ThreadSafeBus(channel = 'vcan0', bustype = 'socketcan_ctypes')

can0.set_filters([
    {
        'can_id': 0x5E7,
        'can_mask': 0x7FF,
        'extended': False
    }
])

txt = ''

def print_message(msg: can.Message):
    global txt
    frameId = msg.data[0]
    frameCount = Bits(int=int(frameId), length=8).hex[0]
    frameNumber = Bits(int=int(frameId), length=8).hex[1]

    frame = BitArray()
    for x in range(6):
        x = x + 2
        frame.append(Bits(uint=int(msg.data[x]), length=8))

    txt = txt + frame.bin

    if frameNumber == frameCount:
        print(TextDecoder.decode(txt))
        txt = ''

loop = asyncio.get_event_loop()
notifier = can.Notifier(can0, [print_message], loop=loop)

loop.run