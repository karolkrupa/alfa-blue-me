import can

can0 = can.ThreadSafeBus(channel = 'vcan0', bustype = 'socketcan_ctypes')

while(True):
    val = input('Button: ')
    msg = can.Message(arbitration_id=0x3C4, data=[], is_extended_id=False)
    if val == 'vol-up':
        msg = can.Message(arbitration_id=0x3C4, data=[0x80, 0x00], is_extended_id=False)
    elif val == 'vol-down':
        msg = can.Message(arbitration_id=0x3C4, data=[0x40, 0x00], is_extended_id=False)
    elif val == 'right':
        msg = can.Message(arbitration_id=0x3C4, data=[0x10, 0x00], is_extended_id=False)
    elif val == 'left':
        msg = can.Message(arbitration_id=0x3C4, data=[0x08, 0x00], is_extended_id=False)
    elif val == 'down':
        msg = can.Message(arbitration_id=0x3C4, data=[0x00, 0x01], is_extended_id=False)
    elif val == 'up':
        msg = can.Message(arbitration_id=0x3C4, data=[0x00, 0x02], is_extended_id=False)
    elif val == 'src':
        msg = can.Message(arbitration_id=0x3C4, data=[0x04, 0x00], is_extended_id=False)
    elif val == 'win':
        msg = can.Message(arbitration_id=0x3C4, data=[0x00, 0x40], is_extended_id=False)
    elif val == 'mute':
        msg = can.Message(arbitration_id=0x3C4, data=[0x20, 0x00], is_extended_id=False)
    elif val == 'menu':
        msg = can.Message(arbitration_id=0x3C4, data=[0x00, 0x80], is_extended_id=False)
    else:
        print('Unknown button')
        continue

    can0.send(msg)