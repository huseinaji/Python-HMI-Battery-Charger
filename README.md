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
### CANbus Host Configuration
Follow This instruction for installing PCAN Driver :
* https://github.com/SICKAG/sick_line_guidance/blob/master/doc/pcan-linux-installation.md

Use this tools for send/receive CAN data :
* sudo apt-get install can-utils
* https://github.com/linux-can/can-utils
* https://python-can.readthedocs.io/en/master/installation.html
* http://skpang.co.uk/blog/archives/1220
