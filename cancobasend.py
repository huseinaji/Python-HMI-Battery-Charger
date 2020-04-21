import can 
import time

bustype = 'socketcan'
channel = 'vcan0'

def producer(id):

    bus = can.interface.Bus(channel=channel, bustype=bustype)
    
    #for i in range(10):
    msg = can.Message(arbitration_id=0xDAAA, data = [id, 0, 1, 3, 1, 4, 1], is_extended_id = False)
    bus.send(msg)
    
    print('ID : {:x}'.format(msg.is_extended_id))
    print("data 1: {:x}, data 2: {:x}, data 3: {:x}".format(msg.data[0], msg.data[1], msg.data[2]))
    
    time.sleep(2)

producer(0x10)