import can
import asyncio
from bitstring import BitArray
from bitstring import Bits
import utils.TextDecoder as TextDecoder
import curses

can0 = can.ThreadSafeBus(channel = 'vcan0', bustype = 'socketcan_ctypes')

can0.set_filters([
    {
        'can_id': 0x5E7,
        'can_mask': 0x7FF,
        'extended': False
    }
])

txt = ''

screen = curses.initscr()

curses.noecho()
curses.cbreak()

screen.keypad(True)


instrumentPanelWindow = curses.newwin(6, 20, 0, 0)
instrumentPanelWindow.border()

screen.refresh()
instrumentPanelWindow.refresh()

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
        instrumentPanelWindow.clear()
        text = TextDecoder.decode(txt)
        fragments = text.split("\n")
        # print(fragments)

        row = 1
        for fragment in fragments:
            instrumentPanelWindow.addstr(row, 1, ' ' + fragment)
            # print(fragment)
            # print(row)
            row += 1
        instrumentPanelWindow.border()
        instrumentPanelWindow.refresh()
        # print(TextDecoder.decode(txt))
        txt = ''


loop = asyncio.get_event_loop()
try:
    notifier = can.Notifier(can0, [print_message], loop=loop)
    loop.run_forever()
except:
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    raise

