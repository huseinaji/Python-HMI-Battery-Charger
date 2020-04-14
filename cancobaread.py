
import can
import time

can_interface = 'vcan0'
bus = can.interface.Bus(can_interface, bustype = 'socketcan')

while 1:
    message = bus.recv()
    string = "nama:husein"
    print(message)
    print('parsed line =')
    step_0 = string.split(":")
    print('step 1: ', step_0[0])
    print('step 2: ', step_0[1])