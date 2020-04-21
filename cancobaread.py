import can
import time
import os

BITRATE = 500000
CHANNEL = 'can0'

try:
    os.system("sudo ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))
    bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')

    time.sleep(1)

except:
    print("Canbus initiating failed")
    SystemExit()


def frameparse(frame, type):
    hexformat = "{:x}"
    bolformat = "{:08b}"

    if type == "bat_voltage":
        x = "".join(hexformat.format(frame.data[i])for i in range (2))
        formatted_data = int(x, 16)
        return formatted_data / 100

    elif type == "bat_current":
        x = "".join(hexformat.format(frame.data[i])for i in range (2,4))
        formatted_data = int(x, 16) 
        return formatted_data / 100 - 50

    elif type == "bat_soc":
        x = "".join(hexformat.format(frame.data[i])for i in range (4,6)) 
        formatted_data = int(x, 16) 
        return formatted_data

    elif type == "bat_temp":
        x = "".join(hexformat.format(frame.data[i])for i in range (6,8))
        formatted_data = int(x, 16)
        return formatted_data

    elif type == "bat_capacity":
        x = "".join(hexformat.format(frame.data[i])for i in range (2))
        formatted_data = int(x, 16)
        return formatted_data / 100

    elif type == "bat_soh":
        x = "".join(hexformat.format(frame.data[i])for i in range (2, 4))
        formatted_data = int(x, 16)
        return formatted_data

    elif type == "bat_cycle":
        x = "".join(hexformat.format(frame.data[i])for i in range (4, 6))
        formatted_data = int(x, 16)
        return formatted_data

    elif type == "status":
        formatted_data = "".join(bolformat.format(frame.data[i])for i in range (6, 8))
        return formatted_data

i = 0
while True: 
    try:      
        msg = bus.recv()
        if msg.arbitration_id == 0xB0FFFFF:
            bat_voltage = frameparse(msg, "bat_voltage")
            bat_current = frameparse(msg, "bat_current")
            bat_soc = frameparse(msg, "bat_soc")
            bat_temp = frameparse(msg, "bat_temp")
            
        if msg.arbitration_id == 0xB1FFFFF:
            bat_capacity = frameparse(msg, "bat_capacity")
            bat_soh = frameparse(msg, "bat_soh")
            bat_cycle = frameparse(msg, "bat_cycle")
            status = frameparse(msg, "status")
            Discharge_Over_Current = frameparse(msg, "status")[0]
            Charge_Over_Current = frameparse(msg, "status")[1]
            Short_Circuit = frameparse(msg, "status")[2]
            Discharge_Over_Temperature = frameparse(msg, "status")[3]
            Discharge_Under_Temperature = frameparse(msg, "status")[4]
            Charge_Over_Temperature = frameparse(msg, "status")[5]
            Charge_Under_Temperature = frameparse(msg, "status")[6]
            Under_Voltage = frameparse(msg, "status")[7]
            Over_Voltage = frameparse(msg, "status")[8]
            Over_Discharge_Capacity = frameparse(msg, "status")[9]
            Unbalance = frameparse(msg, "status")[10]
            System_Failure = frameparse(msg, "status")[11]
            Charge_State = frameparse(msg, "status")[12]
            Discharge_State = frameparse(msg, "status")[13]
            Sleep_State = frameparse(msg, "status")[14]

        if i == 1: print(bat_capacity)

        i += 1       
        if i > 5 : i = 0

    except KeyboardInterrupt:
        print ('keyboard received, program exit')
        SystemExit()
