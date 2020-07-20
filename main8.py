from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QLabel
import sys
import interface
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
import json
import can
import time
import os
import http.client, urllib.request


BITRATE = 500000
CHANNEL = "can0"

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "mqtt/subscribe"
DBtime = 30                         #waktu kirim data -> database (seconds)
CanTime = 2                         #waktu kirim data can (seconds)


class MainClass(QDialog, interface.Ui_MainWindow):
    
    loadData = [0, 0, 0, 0, 0, 0, 0, 0]
    
    BAT_1_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_1_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_1_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_1_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_1_CURRENT = QtCore.pyqtSignal(str)
    BAT_1_SOC = QtCore.pyqtSignal(str)
    BAT_1_TEMP = QtCore.pyqtSignal(str)
    BAT_1_CAPACITY = QtCore.pyqtSignal(str)
    BAT_1_SOH = QtCore.pyqtSignal(str)
    BAT_1_CYCLE = QtCore.pyqtSignal(str)

    BAT_2_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_2_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_2_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_2_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_2_CURRENT = QtCore.pyqtSignal(str)
    BAT_2_SOC = QtCore.pyqtSignal(str)
    BAT_2_TEMP = QtCore.pyqtSignal(str)
    BAT_2_CAPACITY = QtCore.pyqtSignal(str)
    BAT_2_SOH = QtCore.pyqtSignal(str)
    BAT_2_CYCLE = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.flagDB = 0
        self.flagDB2 = 0
        self.flagCAN = 0
        self.bat_1_flagServ = 0
        self.bat_2_flagServ = 0
        self.val = 1
        
        self.setupUi(self)
        self.bat_1_handshaking_status = 0
        self.bat_1_ChargeFLAG = 0
        self.BAT_1_HOLE_ID.connect(self.bat_1_hole_id_handle)
        self.BAT_1_FAULT_CODE.connect(self.bat_1_fault_code_handle)
        self.BAT_1_HANDSHAKING.connect(self.bat_1_handshaking_handle)
        self.BAT_1_VOLTAGE.connect(self.bat_1_voltage_handle)
        self.BAT_1_CURRENT.connect(self.bat_1_current_handle)
        self.BAT_1_SOC.connect(self.bat_1_soc_handle)
        self.BAT_1_TEMP.connect(self.bat_1_temp_handle)
        self.BAT_1_CAPACITY.connect(self.bat_1_capacity_handle)
        self.BAT_1_SOH.connect(self.bat_1_soh_handle)
        self.BAT_1_CYCLE.connect(self.bat_1_cycle_handle)

        self.bat_2_handshaking_status = 0
        self.bat_2_ChargeFLAG = 0
        self.BAT_2_HOLE_ID.connect(self.bat_2_hole_id_handle)
        self.BAT_2_FAULT_CODE.connect(self.bat_2_fault_code_handle)
        self.BAT_2_HANDSHAKING.connect(self.bat_2_handshaking_handle)
        self.BAT_2_VOLTAGE.connect(self.bat_2_voltage_handle)
        self.BAT_2_CURRENT.connect(self.bat_2_current_handle)
        self.BAT_2_SOC.connect(self.bat_2_soc_handle)
        self.BAT_2_TEMP.connect(self.bat_2_temp_handle)
        self.BAT_2_CAPACITY.connect(self.bat_2_capacity_handle)
        self.BAT_2_SOH.connect(self.bat_2_soh_handle)
        self.BAT_2_CYCLE.connect(self.bat_2_cycle_handle)

        #MAIN BUTTON
        self.button_connect.clicked.connect(self.canConnect)
        self.button_disconnect.clicked.connect(self.button_disconnect_handle)
        self.bat_swap.clicked.connect(self.bat_swap_handle)

        #BUTTON START STOP
        self.bat_1_button_start.clicked.connect(self.bat_1_button_start_handle)
        self.bat_1_button_stop.clicked.connect(self.bat_1_button_stop_handle)
        self.bat_2_button_start.clicked.connect(self.bat_2_button_start_handle)
        self.bat_2_button_stop.clicked.connect(self.bat_2_button_stop_handle)

        #BUTTON BACK
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
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
        
        self.progressBar.setMaximum(99)
        self.progressBar_2.setMaximum(99)
        self.progressBar_3.setMaximum(99)
        self.progressBar_4.setMaximum(99)
        self.progressBar_5.setMaximum(99)
        self.progressBar_6.setMaximum(99)
        self.progressBar_7.setMaximum(99)
        self.progressBar_8.setMaximum(99)

        self.l = QtGui.QPalette(self.palette())
        self.brush = QtGui.QBrush(QtGui.QColor(255,0,0))
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.l.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, self.brush)
        self.c = QtGui.QPalette(self.palette())
        self.brush = QtGui.QBrush(QtGui.QColor(243,243,0))
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.c.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, self.brush)
        #self.c.setColor(QtGui.QPalette.Highlight, QtGui.QColor(QtCore.Qt.yellow))
        self.p = QtGui.QPalette()
        self.brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, self.brush)
       
    
    ## every handle method below affected by every single canbus signal transmit
    #BATT 1 VARIABLE
    def bat_1_hole_id_handle(self, value):
        self.hole_1_msg_1 = 0xB0 << 20 | value
        self.hole_1_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_1_id.setText(str(value))
        self.bat_1_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()  
    def bat_1_fault_code_handle(self, value):
        if value != 0:
            self.flagServ = self.flagServ + 1
            if self.flagServ == 1:
                print(senddb(self.add))
                
            if value == 7:
                self.err_code_1.setText("Over Charge")
                self.bat_1_batt_over_charge.setText("1")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")
            
            elif value == 8:
                self.err_code_1.setText("Batt Over Temp")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("1")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")
                
            elif value == 9:
                self.err_code_1.setText("Bat Under Temp")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("1")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_1.setText("Bat Over Current")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("1")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")
            
            elif value == 11:
                self.err_code_1.setText("Bat Over Volt")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("1")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_1.setText("Bat Short Circuit")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("1")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_1.setText("Bat Sistem Failure")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("1")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_1.setText("Charge Out Under Volt")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("1")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_1.setText("Charge Out Over Volt")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("1")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_1.setText("Charge Over Temp")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("1")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_1.setText("Charge Under Temp")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("1")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_1.setText("Charge Short Circuit")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("1")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_1.setText("Charge Over Current")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("1")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_1.setText("In Over Volt")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("1")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_1.setText("In Under Volt")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("1")
                self.bat_1_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_1.setText("Lost Communication")
                self.bat_1_batt_over_charge.setText("0")
                self.bat_1_batt_over_temp.setText("0")
                self.bat_1_batt_under_temp.setText("0")
                self.bat_1_batt_over_current.setText("0")
                self.bat_1_batt_over_voltage.setText("0")
                self.bat_1_batt_short_circuit.setText("0")
                self.bat_1_batt_system_failure.setText("0")
                self.bat_1_charge_out_under_voltage.setText("0")
                self.bat_1_charge_out_over_voltage.setText("0")
                self.bat_1_charge_over_temp.setText("0")
                self.bat_1_charge_under_temp.setText("0")
                self.bat_1_charge_short_circuit.setText("0")
                self.bat_1_charge_over_current.setText("0")
                self.bat_1_charge_in_over_voltage.setText("0")
                self.bat_1_charge_in_under_voltage.setText("0")
                self.bat_1_charge_lost_com.setText("1")
        
        else:
            self.flagServ = 0
            self.err_code_1.setText("0")
            self.bat_1_batt_over_charge.setText("0")
            self.bat_1_batt_over_temp.setText("0")
            self.bat_1_batt_under_temp.setText("0")
            self.bat_1_batt_over_current.setText("0")
            self.bat_1_batt_over_voltage.setText("0")
            self.bat_1_batt_short_circuit.setText("0")
            self.bat_1_batt_system_failure.setText("0")
            self.bat_1_charge_out_under_voltage.setText("0")
            self.bat_1_charge_out_over_voltage.setText("0")
            self.bat_1_charge_over_temp.setText("0")
            self.bat_1_charge_under_temp.setText("0")
            self.bat_1_charge_short_circuit.setText("0")
            self.bat_1_charge_over_current.setText("0")
            self.bat_1_charge_in_over_voltage.setText("0")
            self.bat_1_charge_in_under_voltage.setText("0")
            self.bat_1_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents() 
    def bat_1_handshaking_handle(self, value):
        self.bat_1_handshaking_status = value        
        QtWidgets.QApplication.processEvents()
    def bat_1_voltage_handle(self, value): 
        self.bat_1_voltage.setText(value)   
        self.voltage_1.setText(value)
        #print("".format(value))      
        QtWidgets.QApplication.processEvents()
    def bat_1_current_handle(self, value):
        self.bat_1_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_soc_handle(self, value):
        self.bat_1_soc.setText(value)
        self.soc_1.setText(value)
        self.progressBar.setValue(int(value))
        if self.bat_1_ChargeFLAG == 0:
            if self.bat_1_handshaking_status == 1:
                self.bat_1_button_start.setEnabled(True)
            self.progressBar.setPalette(self.l) if self.progressBar.value() <= 20 else self.progressBar.setPalette(self.p)
        else:
            self.bat_1_button_start.setEnabled(False)
            self.progressBar.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_1_temp_handle(self, value):
        self.bat_1_temp.setText(value)
        self.temp_1.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_capacity_handle(self, value):
        self.bat_1_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_soh_handle(self, value):
        self.bat_1_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_cycle_handle(self, value):
        self.bat_1_cycle.setText(value)
        QtWidgets.QApplication.processEvents()
    
    #BAT 2 VARIABLE
    def bat_2_hole_id_handle(self, value):
        self.hole_2_msg_1 = 0xB0 << 20 | value
        self.hole_2_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_2_id.setText(str(value))
        self.bat_2_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_2_fault_code_handle(self, value):
        if value != 0:
            self.flagServ = self.flagServ + 1
            if self.flagServ == 1:
                print(senddb(self.add2))
            if value == 7:
                self.err_code_2.setText("Over Charge")
                self.bat_2_batt_over_charge.setText("1")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")
        
            elif value == 8:
                self.err_code_2.setText("Batt Over Temp")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("1")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_2.setText("Bat Under Temp")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("1")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_2.setText("Bat Over Current")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("1")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_2.setText("Bat Over Volt")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("1")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_2.setText("Bat Short Circuit")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("1")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_2.setText("Bat Sistem Failure")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("1")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_2.setText("Charge Out Under Volt")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("1")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_2.setText("Charge Out Over Volt")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("1")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_2.setText("Charge Over Temp")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("1")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_2.setText("Charge Under Temp")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("1")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_2.setText("Charge Short Circuit")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("1")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_2.setText("Charge Over Current")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("1")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_.setText("In Over Volt")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("1")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_2.setText("In Under Volt")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("1")
                self.bat_2_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_2.setText("Lost Communication")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("1")
    
            else:
                self.flagServ = 0
                self.err_code_2.setText("0")
                self.bat_2_batt_over_charge.setText("0")
                self.bat_2_batt_over_temp.setText("0")
                self.bat_2_batt_under_temp.setText("0")
                self.bat_2_batt_over_current.setText("0")
                self.bat_2_batt_over_voltage.setText("0")
                self.bat_2_batt_short_circuit.setText("0")
                self.bat_2_batt_system_failure.setText("0")
                self.bat_2_charge_out_under_voltage.setText("0")
                self.bat_2_charge_out_over_voltage.setText("0")
                self.bat_2_charge_over_temp.setText("0")
                self.bat_2_charge_under_temp.setText("0")
                self.bat_2_charge_short_circuit.setText("0")
                self.bat_2_charge_over_current.setText("0")
                self.bat_2_charge_in_over_voltage.setText("0")
                self.bat_2_charge_in_under_voltage.setText("0")
                self.bat_2_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_2_handshaking_handle(self, value):
        self.bat_2_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_2_voltage_handle(self, value):       
        self.bat_2_voltage.setText(value)   
        self.voltage_2.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_2_current_handle(self, value):
        self.bat_2_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_soc_handle(self, value):
        self.bat_2_soc.setText(value)
        self.soc_2.setText(value)
        self.progressBar_2.setValue(int(value))
        if self.bat_2_ChargeFLAG == 0:
            if self.bat_2_handshaking_status == 1:
                self.bat_2_button_start.setEnabled(True)
            self.progressBar_2.setPalette(self.l) if self.progressBar_2.value() <= 20 else self.progressBar_2.setPalette(self.p)
        else:
            self.bat_2_button_start.setEnabled(False)
            self.progressBar_2.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_2_temp_handle(self, value):
        self.bat_2_temp.setText(value)
        self.temp_2.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_capacity_handle(self, value):
        self.bat_2_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_soh_handle(self, value):
        self.bat_2_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_cycle_handle(self, value):
        self.bat_2_cycle.setText(value)
        QtWidgets.QApplication.processEvents()

    #START STOP FUNCTION   
    def bat_1_button_start_handle(self):        
        try:
            self.loadData.pop(0)
            self.loadData.insert(0,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
            self.bus.send(self.sendmsg)
            self.bat_1_ChargeFLAG = 1
        except:
            self.bat_1_ChargeFLAG = 0

    def bat_1_button_stop_handle(self):
        try:
            self.bat_1_button_stop.setEnabled(False)
            self.loadData.pop(0)
            self.loadData.insert(0,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
            self.bus.send(self.sendmsg)
            self.status_1.setPalette(self.l)
            self.bat_1_ChargeFLAG = 0
        except:
            self.bat_1_ChargeFLAG = 1

    def bat_2_button_start_handle(self):
        try:
            self.loadData.pop(1)
            self.loadData.insert(1,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
            self.bus.send(self.sendmsg)
            self.bat_2_ChargeFLAG = 1
            #self.bat_2_button_stop.setEnabled(True)  
        except:
            self.bat_2_ChargeFLAG = 0
            #self.bat_2_button_stop.setEnabled(False) 
        
    def bat_2_button_stop_handle(self):
        try:
            self.bat_2_button_stop.setEnabled(False)
            self.loadData.pop(1)
            self.loadData.insert(1,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
            self.bus.send(self.sendmsg)
            self.status_2.setPalette(self.l)
            self.bat_2_ChargeFLAG = 0
            #self.bat_2_button_stop.setEnabled(False)
        except:
            self.bat_2_ChargeFLAG = 1
            #self.bat_2_button_stop.setEnabled(True)

    ##SWAP FUNCTION
    def bat_swap_handle(self):
        j = 0
        soc = [float(self.bat_1_soc.text()), float(self.bat_2_soc.text()), float(self.bat_3_soc.text())] 
        for i in range(0, (len(soc) - 1)):
            if soc[j] < soc[i+1]:
                j = i + 1

        #self.bat_swap.setText("hole {} ready".format(j+1))
        if j == 0:
            self.bat_1_button_stop.setEnabled(True)
        if j == 1:
            self.bat_2_button_stop.setEnabled(True)
        if j == 2:
            self.bat_3_button_stop.setEnabled(True)
        if j == 3:
            self.bat_4_button_stop.setEnabled(True)
        if j == 4:
            self.bat_5_button_stop.setEnabled(True)
        if j == 5:
            self.bat_6_button_stop.setEnabled(True)
        if j == 6:
            self.bat_7_button_stop.setEnabled(True)
        if j == 7:
            self.bat_8_button_stop.setEnabled(True)

    ##BUTTON CONNECTION  
    def button_disconnect_handle(self):
        try: 
            os.system("sudo ip link set {} down".format(CHANNEL))    
            #self.flagconn = 0
            self.button_connect.setEnabled(True)
            self.button_disconnect.setEnabled(False)
            self.loadData = [0, 0, 0, 0, 0, 0, 0, 0]
            self.bat_1_button_start.setEnabled(False)
            self.bat_2_button_start.setEnabled(False)
            
            self.status_1.setEnabled(False)
            self.status_2.setEnabled(False)
            self.status_3.setEnabled(False)
            self.status_4.setEnabled(False)
            self.status_5.setEnabled(False)
            self.status_6.setEnabled(False)
            self.status_7.setEnabled(False)
            self.status_8.setEnabled(False)
            print("fdsa")

        except:
            self.status_connect.setText("Canbus disconnecting failed")

    def canConnect(self):           ##try to parse data
        try:
            os.system("sudo ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))
            #self.flagconn = 1
            self.bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')
            self.button_connect.setEnabled(False)
            self.button_disconnect.setEnabled(True)
            self.status_connect.setText("Canbus initiating success")

            tic = time.perf_counter()
                
            self.status_1.setEnabled(True)
            self.status_2.setEnabled(True)
            self.status_3.setEnabled(True)
            self.status_4.setEnabled(True)
            self.status_5.setEnabled(True)
            self.status_6.setEnabled(True)
            self.status_7.setEnabled(True)
            self.status_8.setEnabled(True)
            self.msg = self.bus.recv()

            while True:
                self.msg = self.bus.recv()
                toc = time.perf_counter()
                timm = toc - tic
                
                #print("iso")
                SendCanTime = "".join("{:0.2f}".format(timm % CanTime))
                SendDbTime = "".join("{:0.2f}".format(timm % DBtime))
                self.add = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_1_id.text() , self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_batt_over_charge.text(), self.bat_1_batt_over_temp.text(), self.bat_1_batt_under_temp.text(), self.bat_1_batt_over_current.text(), self.bat_1_batt_over_voltage.text(), self.bat_1_batt_short_circuit.text(), self.bat_1_batt_system_failure.text(), self.bat_1_charge_out_under_voltage.text(), self.bat_1_charge_out_over_voltage.text(), self.bat_1_charge_over_temp.text(), self.bat_1_charge_under_temp.text(), self.bat_1_charge_short_circuit.text(), self.bat_1_charge_over_current.text(), self.bat_1_charge_in_over_voltage.text(), self.bat_1_charge_in_under_voltage.text(), self.bat_1_charge_lost_com.text())
                self.add2 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_2_id.text() , self.bat_2_voltage.text(), self.bat_2_current.text(), self.bat_2_soc.text(), self.bat_2_temp.text(), self.bat_2_capacity.text(), self.bat_2_soh.text(), self.bat_2_cycle.text(), self.bat_2_batt_over_charge.text(), self.bat_2_batt_over_temp.text(), self.bat_2_batt_under_temp.text(), self.bat_2_batt_over_current.text(), self.bat_2_batt_over_voltage.text(), self.bat_2_batt_short_circuit.text(), self.bat_2_batt_system_failure.text(), self.bat_2_charge_out_under_voltage.text(), self.bat_2_charge_out_over_voltage.text(), self.bat_2_charge_over_temp.text(), self.bat_2_charge_under_temp.text(), self.bat_2_charge_short_circuit.text(), self.bat_2_charge_over_current.text(), self.bat_2_charge_in_over_voltage.text(), self.bat_2_charge_in_under_voltage.text(), self.bat_2_charge_lost_com.text()) 
                ## THE ARBITRATION_ID MAY CHANGE WHEN TRYING ON REAL BMS
                #HOLE 1
                
                if self.msg.arbitration_id == 0x0C1:
                    self.BAT_1_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_1_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_1_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                
                if self.bat_1_handshaking_status == 1:
                    self.status_1.setPalette(self.p)
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB = self.flagDB + 1
                        if self.flagDB == 1:
                            print(senddb(self.add))
                    else:
                        self.flagDB = 0
                    
                    if self.msg.arbitration_id == self.hole_1_msg_1:
                        self.BAT_1_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_1_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_1_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_1_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                       
                    if self.msg.arbitration_id == self.hole_1_msg_2:
                        self.BAT_1_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_1_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_1_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                elif self.bat_1_handshaking_status == 0:
                    self.status_1.setPalette(self.l)
                    self.BAT_1_VOLTAGE.emit("0")
                    self.BAT_1_CURRENT.emit("0")
                    self.BAT_1_SOC.emit("0")
                    self.BAT_1_TEMP.emit("0")
                    self.BAT_1_CAPACITY.emit("0")
                    self.BAT_1_SOH.emit("0")
                    self.BAT_1_CYCLE.emit("0")
                    self.BAT_1_FAULT_CODE.emit(0)
                
                #HOLE 2
                if self.msg.arbitration_id == 0x0C2:
                    self.BAT_2_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_2_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_2_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_2_handshaking_status == 1:
                    self.status_2.setPalette(self.p)
                    
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB2 = self.flagDB2 + 1
                        if self.flagDB2 == 1:
                            print(senddb(self.add2))
                    else:
                        self.flagDB2 = 0 
                    
                    if self.msg.arbitration_id == self.hole_2_msg_1:
                        self.BAT_2_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_2_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_2_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_2_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_2_msg_2:
                        self.BAT_2_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_2_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_2_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_2.setPalette(self.l)
                    self.BAT_2_VOLTAGE.emit("0")
                    self.BAT_2_CURRENT.emit("0")
                    self.BAT_2_SOC.emit("0")
                    self.BAT_2_TEMP.emit("0")
                    self.BAT_2_CAPACITY.emit("0")
                    self.BAT_2_SOH.emit("0")
                    self.BAT_2_CYCLE.emit("0")
                    self.BAT_2_FAULT_CODE.emit(0)
                
                if (float(SendCanTime) > 0.0) & (float(SendCanTime) < 1.0):
                    self.flagCAN = self.flagCAN + 1
                    if self.flagCAN == 1:
                        self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
                        self.bus.send(self.sendmsg) 
                else:
                    self.flagCAN = 0
             
        except:
            #self.flagconn = 0
            self.status_1.setEnabled(False)
            self.status_2.setEnabled(False)
            self.status_3.setEnabled(False)
            self.status_4.setEnabled(False)
            self.status_5.setEnabled(False)
            self.status_6.setEnabled(False)
            self.status_7.setEnabled(False)
            self.status_8.setEnabled(False)

            self.status_connect.setText("Canbus disconnected")
            self.button_connect.setEnabled(True)
            self.button_disconnect.setEnabled(False)

            self.BAT_1_VOLTAGE.emit("0")
            self.BAT_1_CURRENT.emit("0")
            self.BAT_1_SOC.emit("0")
            self.BAT_1_TEMP.emit("0")
            self.BAT_1_CAPACITY.emit("0")
            self.BAT_1_SOH.emit("0")
            self.BAT_1_CYCLE.emit("0")
            self.bat_1_id_1.setText("")
            self.bat_1_id.setText("")
            self.err_code_1.setText("0")
            self.BAT_1_FAULT_CODE.emit(0)
            
            self.BAT_2_VOLTAGE.emit("0")
            self.BAT_2_CURRENT.emit("0")
            self.BAT_2_SOC.emit("0")
            self.BAT_2_TEMP.emit("0")
            self.BAT_2_CAPACITY.emit("0")
            self.BAT_2_SOH.emit("0")
            self.BAT_2_CYCLE.emit("0")
            self.bat_2_id_1.setText("")
            self.bat_2_id.setText("")
            self.err_code_2.setText("0")
            self.BAT_2_FAULT_CODE.emit(0)


def senddb(data):
    encript = ""
    for x in data:   
        i = ord(x) + 2
        encript = encript + chr(i)
    url = ("http://charging.genmotorcycles.com/index.php?x=")
    url = url + encript
    #webUrl = urllib.request.urlopen(url)
    #print("result code " + str(webUrl.getcode()))
    return url
    
## another parse method
def frameparse(frame, type):
    hexformat = "{:x}"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    bolformat = "{:08b}"
    floatformat = "{:4.2f}"

    if type == "bat_id":
        x = "".join(hexformat.format(frame.data[i])for i in range (3))
        formatted_data = int(x, 16)
        return formatted_data

    if type == "fault_code":
        x = "".join(hexformat.format(frame.data[3]))
        formatted_data = int(x, 16)
        return formatted_data

    if type == "handshaking":
        x = "".join(hexformat.format(frame.data[4]))
        formatted_data = int(x, 16)
        return formatted_data

    if type == "bat_voltage":
        x = "".join(hexformat.format(frame.data[1]))
        x = "".join(x + hexformat.format(frame.data[0]))

        formatted_data = int(x, 16)
        return formatted_data / 100 

    elif type == "bat_current":
        x = "".join(hexformat.format(frame.data[3]))
        x = "".join(x + hexformat.format(frame.data[2]))

        formatted_data = int(x, 16) 
        formatted_data = formatted_data / 100 - 50
        return floatformat.format(formatted_data)

    elif type == "bat_soc":
        x = "".join(hexformat.format(frame.data[5]))
        x = "".join(x + hexformat.format(frame.data[4]))
        formatted_data = int(x, 16) / 100 
        return "{:4.0f}".format(formatted_data)

    elif type == "bat_temp":
        x = "".join(hexformat.format(frame.data[7]))
        x = "".join(x + hexformat.format(frame.data[6]))
        formatted_data = int(x, 16) 
        formatted_data = formatted_data / 10 - 40
        return floatformat.format(formatted_data)

    elif type == "bat_capacity":
        x = "".join(hexformat.format(frame.data[1]))
        x = "".join(x + hexformat.format(frame.data[0]))
        formatted_data = int(x, 16)
        return formatted_data / 100

    elif type == "bat_soh":
        x = "".join(hexformat.format(frame.data[3]))
        x = "".join(x + hexformat.format(frame.data[2]))
        formatted_data = int(x, 16)
        return formatted_data

    elif type == "bat_cycle":
        x = "".join(hexformat.format(frame.data[5]))
        x = "".join(x + hexformat.format(frame.data[4]))
        formatted_data = int(x, 16)
        return formatted_data

    elif type == "status":
        formatted_data = "".join(bolformat.format(frame.data[i])for i in range (6, 8))
        return formatted_data

if __name__ == "__main__":
    window = QApplication(sys.argv)
    ui = MainClass()
    ui.showFullScreen()
    window.exec_()

    '''
    V1. enkripsi data
    V2. Algoritma Button swap
    V3. Handshaking new design
    4. multithreading
    '''
