# Python-HMI-Battery-Charger
## Raspberry Pi Preparation
### Headless Raspberry Configuration
Follow this instruction for wifi connection setting
* https://raspberrypi.stackexchange.com/questions/10251/prepare-sd-card-for-wifi-on-headless-pi

Download VNC viewer and install it
* https://www.realvnc.com/en/connect/download/viewer/linux/

### Standard Procedure and Debugging
Run Program on Raspberry Pi:

(if the color didn't change on Raspbian, use "sudo")
```
Python3 main.py
```

inserting image to QT
* https://stackoverflow.com/questions/28536306/inserting-an-image-in-gui-using-qt-designer

Convert Qt5 Designer output from .ui (QTCreator output) to .py

write on command line:
```
apt-get install pyqt5-dev-tools

pyuic5 -x "name".ui -o "output name".py
```
for .qrc file:
```
pyrcc5 "name".qrc -o "output name".py
```

### Install python3 program dependencies:
```
sudo apt-get install python3-pyqt5
sudo apt-get install python3-pip
sudo apt-get install DateTime
sudo apt-get install RPi.GPIO
sudo apt-get install python-can
```
## CANbus Configuration
### PCan Installation
Follow This instruction for installing PCAN Driver (PC) :
* https://github.com/SICKAG/sick_line_guidance/blob/master/doc/pcan-linux-installation.md

For Raspberry Pi:
* https://forum.peak-system.com/viewtopic.php?t=3381

### MCP Raspberry Pi Configuration
Follow below instruction :
* https://vimtut0r.com/2017/01/17/can-bus-with-raspberry-pi-howtoquickstart-mcp2515-kernel-4-4-x/

edit /boot/config.txt to:
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
dtoverlay=spi1-1cs
```
then install the dependency
```
sudo apt-get install can-utils
```
overall, including wiring are okay

## Error and Debugging
### CANbus Error and Debugging
if there is some error occure while trying mcp2515 canbus module:
```
cannot find device can0
```
follow this instruction
* https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=155651&p=1023355#p1023355

on the "/boot/config.txt" just remove "-overlays"

#### MCP2515 modul cannot send or receive any message

* the oscillator must set to be 8000000, not 16000000 (same as the crystal module) --> and this happened to me :((

* interrupt pin need to set as GPIO pin

* the mcp2515 chip need 3.3v but TJA1050 need 5V supply. Cut and devide the wire to get 5V source (follow below instruction)

* https://vimtut0r.com/2017/01/17/can-bus-with-raspberry-pi-howtoquickstart-mcp2515-kernel-4-4-x/

## MQTT configuration
### Installation
clone paho-mqtt from github:
* sudo git clone https://github.com/eclipse/paho.mqtt.python

get in to the directory paho-mqtt then,
* python3 setup.py install

if there is some error occured, try this
* pip3 install paho-mqtt python-etcd
