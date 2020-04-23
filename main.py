# import can
import asyncio
# from threading import Thread
# from module.A2DP import A2DP
# from device.SteeringWheel import SteeringWheel
# from device.InstrumentPanel import InstrumentPanel
from device.Radio import radio
# from module.Proxi import Proxi
# from module.StatusManager import StatusManager
from bluetooth.Manger import defaultManger
# import dbus
from module.EventBus import mainEventBus
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

loop = asyncio.get_event_loop()

# can0 = can.ThreadSafeBus(channel = 'vcan0', bustype = 'socketcan_ctypes')
# can0 = can.ThreadSafeBus(channel = 'vcan', bustype = 'virtual')

defaultManger.register_agent()
defaultManger.register_device_manager()

player = defaultManger.device_manager.get_active_device().get_player()

def test(arg):
    print(player.get_all_props())


player.event_bus.on('properties-changed', test)

player.stop()
# player.play()
# print(player.get_all_props())




mainloop = GObject.MainLoop()
mainloop.run()

# # proxi = Proxi(can0, loop)
# status_manager = StatusManager(can0)
# status_manager.run()
# steering_wheel = SteeringWheel(can0)
# instrument_panel = InstrumentPanel(can0)
# radio = Radio(can0)
# radio.run()
#
# a2dpInstance = A2DP(can0, radio=radio, instrument_panel=instrument_panel, steering_wheel=steering_wheel)
# # try:
# a2dpInstance.run()
# # cat
#
#
#
# can.Notifier(can0, [
#     steering_wheel.on_message
# ], loop=loop)
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     exit(0)

# loop.call_later(2, a2dpInstance.refresh_properties)
# mainThread = Thread(target=loop.run_forever)
# mainThread.start()
# mainProcess.start()
# try:
#     print('Run Glib')
#
#     a2dpInstance.glib_loop.run()
#     print('After Glib Run')
# except KeyboardInterrupt:
#     print('EXIT')
#     mainThread.
#

# dictornay = {
#     '\r': '000000',
#     '0': '000001',
#     '1': '000010',
#     '2': '000011',
#     '3': '000100',
#     '4': '000101',
#     '5': '000110',
#     '6': '000111',
#     '7': '001000',
#     '8': '001001',
#     '9': '001010',
#     '.': '001011',
#     'A': '001100',
#     'B': '001101',
#     'C': '001110',
#     'D': '001111',
#     'E': '010000',
#     'F': '010001',
#     'G': '010010',
#     'H': '010011',
#     'I': '010100',
#     'J': '010101',
#     'K': '010110',
#     'L': '010111',
#     'M': '011000',
#     'N': '011001',
#     'O': '011010',
#     'P': '011011',
#     'Q': '011100',
#     'R': '011101',
#     'S': '011110',
#     'T': '011111',
#     'U': '100000',
#     'V': '100001',
#     'W': '100010',
#     'K': '100011',
#     'Y': '100100',
#     'Z': '100101',
#     'ñ': '100110',
#     'ç': '100111',
#     ' ': '101000',
#     'Ğ': '101001',
#     'i': '101010',
#     'j': '101011',
#     '§': '101100',
#     'À': '101101',
#     'Ä': '101110',
#     'ŭ': '101111',
#     'Ü': '110000',
#     '9': '110001',
#     '_': '110010',
#     '_': '110011',
#     '_': '110100',
#     '?': '110101',
#     '°': '110110',
#     '!': '110111',
#     '+': '111000',
#     '-': '111001',
#     ':': '111010',
#     '/': '111011',
#     '#': '111100',
#     '*': '111101',
#     '_': '111110',
#     '\n': '111111'
# }
#
#
# # def print_message(msg):
# #     msgUp = can.Message(arbitration_id=0x3C4, data=[80, 00], extended_id=False)
# #     print(msg.data == bytearray([0x8000]))
# #
#
# txt = 'S\nelo adsasdaas';
# encoded = ''
#
# for letter in txt:
#     encoded += dictornay[letter.upper()]
# encoded += '000000'
#
# # msg = [0, 0x02]
# msg = []
# encodeIndex = 0
# while encodeIndex < len(encoded):
#     # print(int(encoded[encodeIndex:encodeIndex+8], 2))
#     msg.append(int(encoded[encodeIndex:encodeIndex+8], 2))
#     encodeIndex += 8
#
# frameCount = math.ceil(len(msg)/6)-1
# currentFrame = [int('0x' + str(frameCount) + '0', 16), 0x2A]
# frameStack = [currentFrame]
# for byte in msg:
#     if len(currentFrame) >= 8:
#         currentFrame = [int('0x' + str(frameCount) + str(len(frameStack)), 16), 0x2A]
#         frameStack.append(currentFrame)
#     currentFrame.append(byte)
#
# while(len(currentFrame) < 8):
#     currentFrame.append(0x00)
#
# can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native
#
# for frame in frameStack:
#     msg = can.Message(arbitration_id=0x5E7, data=frame, extended_id=False)
#     # msg.dlc = 8
#     can0.send(msg)
#     print(msg)
#     # print(frame)
#     time.sleep(0.05)
#
# print(encoded)
#
# # can0.send(msg)
#
# # def main():
# #     can0 = can.Bus(channel='can0', bustype='socketcan_ctypes',can_filters=[{"can_id": 0x3C4, "can_mask": 0x7FF, "extended": False}])
# #
# #     listeners = [
# #         print_message  # Callback function
# #     ]
# #     # Create Notifier with an explicit loop to use for scheduling of callbacks
# #     loop = asyncio.get_event_loop()
# #     notifier = can.Notifier(can0, listeners, loop=loop)
# #
# #
# # # Get the default event loop
# # loop = asyncio.get_event_loop()
# # main()
# # # Run until main coroutine finishes
# # loop.run_forever()
