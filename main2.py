from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QLabel
import sys
import interface
from PyQt5.QtCore import QTimer
import can
import time
import os

BITRATE = 500000
CHANNEL = "can0"

'''
try:
   os.system("sudo ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))
   bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')
   msg = bus.recv()
   time.sleep(1)
   print(msg)
except:
   print("Canbus initiating failed")
   SystemExit()
'''

class MainClass(QDialog, interface.Ui_MainWindow):
   valupdate = QtCore.pyqtSignal(int)
   def __init__(self):
      super().__init__()
      
      self.val = 1
      self.setupUi(self)
      self.pushButton_2.clicked.connect(self.updateValue)
      self.valupdate.connect(self.handlevalue)
      self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
      self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
      self.pushButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
      self.pushButton_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
      self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
      self.pushButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
      self.pushButton_9.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

      self.toolButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
      self.toolButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
      self.toolButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
      self.toolButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
      self.toolButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
      self.toolButton_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
      self.toolButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
      self.toolButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(8))

        #self.pushButton.clicked.connect(self.btnClickedEvent)
        #self.temp_1 = QLabel()
        #self.temp_1.linkActivated.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        #self.QLabel.temp_1 = self.do_something

      self.timer = QTimer()
        #self.timer.timeout.connect(self.handleTimer)
      self.timer.start(100)
        
      self.progressBar.setMaximum(99)
      self.progressBar_2.setMaximum(99)
      self.progressBar_3.setMaximum(99)
      self.progressBar_4.setMaximum(99)
      self.progressBar_5.setMaximum(99)
      self.progressBar_6.setMaximum(99)
      self.progressBar_7.setMaximum(99)
      self.progressBar_8.setMaximum(99)

      self.l = QtGui.QPalette(self.palette())
      self.l.setColor(QtGui.QPalette.Highlight, QtGui.QColor(QtCore.Qt.red))
      self.dial.valueChanged.connect(self.dialValue)
      self.p = QtGui.QPalette()
      self.brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
      self.brush.setStyle(QtCore.Qt.SolidPattern)
      self.p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, self.brush)
      self.brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
      self.brush.setStyle(QtCore.Qt.SolidPattern)
      self.p.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, self.brush)
      self.brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
      self.brush.setStyle(QtCore.Qt.SolidPattern)
      self.p.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, self.brush)

    #def do_something(self):
    #    print("clickable")

   def dialValue(self):
            
      self.progressBar.setValue(self.dial.value())
      a = self.progressBar.value()
      self.progressBar_2.setValue(a)
      self.progressBar.setPalette(self.l) if a <= 20 else self.progressBar.setPalette(self.p)
      self.progressBar_2.setPalette(self.l) if a <= 20 else self.progressBar_2.setPalette(self.p)
        
      self.bat_1_voltage.setText(str(self.dial.value()))
      self.bat_1_temp.setText(str(self.dial.value()))
      self.bat_1_current.setText(str(self.dial.value()))
      self.voltage_1.setText(str(self.dial.value()))
      self.temp_1.setText(str(self.dial.value()))
   
   def updateValue(self):
      
      for i in range (10):    
         self.valupdate.emit(i)
         time.sleep(0.5)

   def handlevalue(self,value):
      self.bat_1_temp.setText(str(value))
      QtWidgets.QApplication.processEvents()

   def canConnect(self):
      
      try:
         '''
         if msg.arbitration_id == 0xB0FFFFF:
            bat_voltage = frameparse(msg, "bat_voltage")
            bat_current = frameparse(msg, "bat_current")
            bat_soc = frameparse(msg, "bat_soc")
            bat_temp = frameparse(msg, "bat_temp")
         '''
         #self.bat_1_voltage.setText(str(bat_voltage))
         #self.bat_1_current.setText(str(bat_current))
         #self.bat_1_soc.setText(str(bat_soc))
         self.val = self.val
         self.bat_1_temp.setText(str(self.val))
         
         '''
         elif msg.arbitration_id == 0xB0FFFFF:
            self.bat_1_voltage.setText("2") 
         else:
            print(msg.arbitration_id)
            self.bat_1_voltage.setText("3")  
           
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
         '''
      except:
         #print("{:x}".format(msg.arbitration_id))
         self.bat_1_voltage.setText("none")
         #self.bat_1_current.setText(str(bat_voltage))
'''
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
'''

if __name__ == "__main__":
    window = QApplication(sys.argv)
    ui = MainClass()
    ui.showFullScreen()
    window.exec_()