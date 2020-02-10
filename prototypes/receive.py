import os
import can

# os.system('sudo ip link set can0 type can bitrate 100000')
# os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native

#msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], extended_id=False)
msg = can0.recv(10.0)
print(msg)
if msg is None:
    print('Timeout occurred, no message.')

# os.system('sudo ifconfig can0 down')