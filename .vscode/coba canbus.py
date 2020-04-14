import time
import os
import subprocess
import logging
import threading
import can 
import RPi.GPIO as GPIO
from datetime import datetime

# global variables
DEBUG = not False
SECONDS_DILATION_MAX = 60
GPIO_LCD_POWER = 44
GPIO_LCD_BACKLIGHT = 42
CAN_ID_SUBMODULE = 0x000
CAN_ID_RTC = 0x001 
CHANNEL = "can0"
BITRATE = 500000
RUN_THREADS = True
SHUTDOWN_REQUEST = False

# main function
def threadRxCan():
    global SHUTDOWN_REQUEST
    # receive messages
    while RUN_THREADS:
        # get received message (blocking)
        try:
            frame = bus.recv()
        except: 
            logging.warning("Receiving failed.")
        else:
            # debugging
            logging.debug("RX {}".format(canFormatFrame(frame)))

            # set Backlight Control from Submodule.Daylight frame
            if(frame.arbitration_id == CAN_ID_SUBMODULE):
                SHUTDOWN_REQUEST = canRxSubModule(frame.data)

            # set Datetime from RTC frame
            elif(frame.arbitration_id == CAN_ID_RTC):
                canRxRTC(frame.data)

def threadUsbMonitor():
    msg = can.Message(arbitration_id=0x7D0, data=[0])
    toggle_indicator = False

    # check & send usb-plugged status
    while RUN_THREADS:
        msg.data[0] = 0

        # check usb-plugged status
        try:
            device_count = len(shell("lsusb").splitlines())
        except: 
            logging.error("Executing command 'lsusb' failed")
        else:
            # count usb device (default 1: HUB)
            if device_count > 1:
                msg.data[0] = int(device_count > 1)
                # indicator
                GPIO.output(GPIO_LCD_POWER, (GPIO.HIGH, GPIO.LOW)[toggle_indicator])
                toggle_indicator = not toggle_indicator
            else:
                GPIO.output(GPIO_LCD_POWER, GPIO.HIGH)

        # send usb-plugged status to can
        try:
            bus.send(msg)
        except:
            logging.warning("Sending failed.")
        else:
            logging.debug("TX {}".format(canFormatFrame(msg)))
        
        time.sleep(0.5)

# can related functions
def canFormatFrame(frame, conversion = "hex"):
    if frame.is_remote_frame:
        formatted_data = "RTR"
    else:
        formatter = "0x{:02X} "
        if conversion == "bin":
            formatter = "{:08b} "
        elif conversion == "decimal":
            formatter = "{:>3d} "
        formatted_data = "".join(formatter.format(i) for i in frame.data)

    return "0x{:03X}[{:d}]: {}".format(frame.arbitration_id, frame.dlc, formatted_data)

def canRxSubModule(data):
    try:
        backlight_state = (data[0] >> 7) & 1
        shutdown_state = (data[1] >> 2) & 1
    except: 
        logging.warning("SubModule Frame is corrupted, parsing failed.")
    else:
        GPIO.output(GPIO_LCD_BACKLIGHT, backlight_state)

    return shutdown_state

def canRxRTC(data):
    try:
        rtc = datetime(data[5], data[4], data[3], data[2], data[1], data[0], 0)
    except:
        logging.warning("RTC Frame is corrupted, parsing failed.")
    else:
        now = datetime.now()
        delta_seconds = abs(rtc - now).total_seconds()

        # check time dilation
        if delta_seconds > SECONDS_DILATION_MAX:
            # set system datetime
            os.system("sudo timedatectl set-time '{}-{}-{} {}:{}:{}'".format(
                rtc.year, rtc.month, rtc.day, rtc.hour, rtc.minute, rtc.second
            ))       
            time.sleep(0.1)

def shell(command):
    output = subprocess.check_output(
        command,
        shell=True, 
        universal_newlines=True)
    return output

# define start point
if __name__ == '__main__':   
    # configure logging
    logging.basicConfig(
        format="%(asctime)s-%(levelname)s-%(message)s", datefmt="%H:%M:%S",
        level=(logging.INFO, logging.DEBUG)[DEBUG]
    )
    logging.getLogger("can").setLevel(logging.WARNING)

    # GPIO initialization
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_LCD_POWER, GPIO.OUT) 
    GPIO.setup(GPIO_LCD_BACKLIGHT, GPIO.OUT) 

    # activate the CAN driver
    logging.info("Enabling {} driver...".format(CHANNEL))
    os.system("sudo /sbin/ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))
    time.sleep(0.1)

    # create bus instance
    try:
        bus = can.ThreadSafeBus(
            bustype='socketcan_native', channel=CHANNEL, bitrate=BITRATE, 
        )
    except OSError:
        logging.error("Bus {} is error.".format(CHANNEL))
        exit()
    else: 
        logging.info("Bus {} is ready.".format(CHANNEL))
        # disable ntp sync
        os.system("sudo timedatectl set-ntp no") 
        time.sleep(0.1)
    
    # make RTOS
    thRxCan = threading.Thread(target=threadRxCan)
    thUsbMonitor = threading.Thread(target=threadUsbMonitor)

    # start RTOS
    thRxCan.start()   
    thUsbMonitor.start()    

    # main thread
    try:
        while not SHUTDOWN_REQUEST:
            time.sleep(0.1)
    except:
        logging.info("Opps, something is wrong.")
    finally:
        logging.info("Program is terminatting...")
        # stop the thread
        RUN_THREADS = False
        thRxCan.join()
        thUsbMonitor.join()
        # stop CAN-BUS
        bus.shutdown()
        logging.info("Program is terminated.")
        # shutdown request
        if SHUTDOWN_REQUEST:
            os.system("sudo shutdown -h now")