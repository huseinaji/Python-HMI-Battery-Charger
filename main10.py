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

flagConnect = 0
loadData = [0, 0, 0, 0, 0, 0, 0, 0]
bus = 0
class MainClass(QDialog, interface.Ui_MainWindow):
    
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

    BAT_3_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_3_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_3_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_3_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_3_CURRENT = QtCore.pyqtSignal(str)
    BAT_3_SOC = QtCore.pyqtSignal(str)
    BAT_3_TEMP = QtCore.pyqtSignal(str)
    BAT_3_CAPACITY = QtCore.pyqtSignal(str)
    BAT_3_SOH = QtCore.pyqtSignal(str)
    BAT_3_CYCLE = QtCore.pyqtSignal(str)

    BAT_4_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_4_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_4_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_4_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_4_CURRENT = QtCore.pyqtSignal(str)
    BAT_4_SOC = QtCore.pyqtSignal(str)
    BAT_4_TEMP = QtCore.pyqtSignal(str)
    BAT_4_CAPACITY = QtCore.pyqtSignal(str)
    BAT_4_SOH = QtCore.pyqtSignal(str)
    BAT_4_CYCLE = QtCore.pyqtSignal(str)

    BAT_5_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_5_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_5_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_5_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_5_CURRENT = QtCore.pyqtSignal(str)
    BAT_5_SOC = QtCore.pyqtSignal(str)
    BAT_5_TEMP = QtCore.pyqtSignal(str)
    BAT_5_CAPACITY = QtCore.pyqtSignal(str)
    BAT_5_SOH = QtCore.pyqtSignal(str)
    BAT_5_CYCLE = QtCore.pyqtSignal(str)

    BAT_6_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_6_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_6_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_6_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_6_CURRENT = QtCore.pyqtSignal(str)
    BAT_6_SOC = QtCore.pyqtSignal(str)
    BAT_6_TEMP = QtCore.pyqtSignal(str)
    BAT_6_CAPACITY = QtCore.pyqtSignal(str)
    BAT_6_SOH = QtCore.pyqtSignal(str)
    BAT_6_CYCLE = QtCore.pyqtSignal(str)

    BAT_7_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_7_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_7_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_7_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_7_CURRENT = QtCore.pyqtSignal(str)
    BAT_7_SOC = QtCore.pyqtSignal(str)
    BAT_7_TEMP = QtCore.pyqtSignal(str)
    BAT_7_CAPACITY = QtCore.pyqtSignal(str)
    BAT_7_SOH = QtCore.pyqtSignal(str)
    BAT_7_CYCLE = QtCore.pyqtSignal(str)

    BAT_8_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_8_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_8_HANDSHAKING = QtCore.pyqtSignal(int)
    BAT_8_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_8_CURRENT = QtCore.pyqtSignal(str)
    BAT_8_SOC = QtCore.pyqtSignal(str)
    BAT_8_TEMP = QtCore.pyqtSignal(str)
    BAT_8_CAPACITY = QtCore.pyqtSignal(str)
    BAT_8_SOH = QtCore.pyqtSignal(str)
    BAT_8_CYCLE = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.flagDB1 = 0
        self.flagDB2 = 0
        self.flagDB3 = 0
        self.flagDB4 = 0
        self.flagDB5 = 0
        self.flagDB6 = 0
        self.flagDB7 = 0
        self.flagDB8 = 0

        self.bat_1_flagServ = 0
        self.bat_2_flagServ = 0
        self.bat_3_flagServ = 0
        self.bat_4_flagServ = 0
        self.bat_5_flagServ = 0
        self.bat_6_flagServ = 0
        self.bat_7_flagServ = 0
        self.bat_8_flagServ = 0
        
        self.bat_1_swap = 0
        self.bat_2_swap = 0
        self.bat_3_swap = 0
        self.bat_4_swap = 0
        self.bat_5_swap = 0
        self.bat_6_swap = 0
        self.bat_7_swap = 0
        self.bat_8_swap = 0

        #thread Initial
        self.cansend = CanSend()       
        
        #battery Initial
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

        self.bat_3_handshaking_status = 0
        self.bat_3_ChargeFLAG = 0
        self.BAT_3_HOLE_ID.connect(self.bat_3_hole_id_handle)
        self.BAT_3_FAULT_CODE.connect(self.bat_3_fault_code_handle)
        self.BAT_3_HANDSHAKING.connect(self.bat_3_handshaking_handle)
        self.BAT_3_VOLTAGE.connect(self.bat_3_voltage_handle)
        self.BAT_3_CURRENT.connect(self.bat_3_current_handle)
        self.BAT_3_SOC.connect(self.bat_3_soc_handle)
        self.BAT_3_TEMP.connect(self.bat_3_temp_handle)
        self.BAT_3_CAPACITY.connect(self.bat_3_capacity_handle)
        self.BAT_3_SOH.connect(self.bat_3_soh_handle)
        self.BAT_3_CYCLE.connect(self.bat_3_cycle_handle)

        self.bat_4_handshaking_status = 0
        self.bat_4_ChargeFLAG = 0
        self.BAT_4_HOLE_ID.connect(self.bat_4_hole_id_handle)
        self.BAT_4_FAULT_CODE.connect(self.bat_4_fault_code_handle)
        self.BAT_4_HANDSHAKING.connect(self.bat_4_handshaking_handle)
        self.BAT_4_VOLTAGE.connect(self.bat_4_voltage_handle)
        self.BAT_4_CURRENT.connect(self.bat_4_current_handle)
        self.BAT_4_SOC.connect(self.bat_4_soc_handle)
        self.BAT_4_TEMP.connect(self.bat_4_temp_handle)
        self.BAT_4_CAPACITY.connect(self.bat_4_capacity_handle)
        self.BAT_4_SOH.connect(self.bat_4_soh_handle)
        self.BAT_4_CYCLE.connect(self.bat_4_cycle_handle)

        self.bat_5_handshaking_status = 0
        self.bat_5_ChargeFLAG = 0
        self.BAT_5_HOLE_ID.connect(self.bat_5_hole_id_handle)
        self.BAT_5_FAULT_CODE.connect(self.bat_5_fault_code_handle)
        self.BAT_5_HANDSHAKING.connect(self.bat_5_handshaking_handle)
        self.BAT_5_VOLTAGE.connect(self.bat_5_voltage_handle)
        self.BAT_5_CURRENT.connect(self.bat_5_current_handle)
        self.BAT_5_SOC.connect(self.bat_5_soc_handle)
        self.BAT_5_TEMP.connect(self.bat_5_temp_handle)
        self.BAT_5_CAPACITY.connect(self.bat_5_capacity_handle)
        self.BAT_5_SOH.connect(self.bat_5_soh_handle)
        self.BAT_5_CYCLE.connect(self.bat_5_cycle_handle)

        self.bat_6_handshaking_status = 0
        self.bat_6_ChargeFLAG = 0
        self.BAT_6_HOLE_ID.connect(self.bat_6_hole_id_handle)
        self.BAT_6_FAULT_CODE.connect(self.bat_6_fault_code_handle)
        self.BAT_6_HANDSHAKING.connect(self.bat_6_handshaking_handle)
        self.BAT_6_VOLTAGE.connect(self.bat_6_voltage_handle)
        self.BAT_6_CURRENT.connect(self.bat_6_current_handle)
        self.BAT_6_SOC.connect(self.bat_6_soc_handle)
        self.BAT_6_TEMP.connect(self.bat_6_temp_handle)
        self.BAT_6_CAPACITY.connect(self.bat_6_capacity_handle)
        self.BAT_6_SOH.connect(self.bat_6_soh_handle)
        self.BAT_6_CYCLE.connect(self.bat_6_cycle_handle)

        self.bat_7_handshaking_status = 0
        self.bat_7_ChargeFLAG = 0
        self.BAT_7_HOLE_ID.connect(self.bat_7_hole_id_handle)
        self.BAT_7_FAULT_CODE.connect(self.bat_7_fault_code_handle)
        self.BAT_7_HANDSHAKING.connect(self.bat_7_handshaking_handle)
        self.BAT_7_VOLTAGE.connect(self.bat_7_voltage_handle)
        self.BAT_7_CURRENT.connect(self.bat_7_current_handle)
        self.BAT_7_SOC.connect(self.bat_7_soc_handle)
        self.BAT_7_TEMP.connect(self.bat_7_temp_handle)
        self.BAT_7_CAPACITY.connect(self.bat_7_capacity_handle)
        self.BAT_7_SOH.connect(self.bat_7_soh_handle)
        self.BAT_7_CYCLE.connect(self.bat_7_cycle_handle)

        self.bat_8_handshaking_status = 0
        self.bat_8_ChargeFLAG = 0
        self.BAT_8_HOLE_ID.connect(self.bat_8_hole_id_handle)
        self.BAT_8_FAULT_CODE.connect(self.bat_8_fault_code_handle)
        self.BAT_8_HANDSHAKING.connect(self.bat_8_handshaking_handle)
        self.BAT_8_VOLTAGE.connect(self.bat_8_voltage_handle)
        self.BAT_8_CURRENT.connect(self.bat_8_current_handle)
        self.BAT_8_SOC.connect(self.bat_8_soc_handle)
        self.BAT_8_TEMP.connect(self.bat_8_temp_handle)
        self.BAT_8_CAPACITY.connect(self.bat_8_capacity_handle)
        self.BAT_8_SOH.connect(self.bat_8_soh_handle)
        self.BAT_8_CYCLE.connect(self.bat_8_cycle_handle)

        #MAIN BUTTON
        self.button_connect.clicked.connect(self.canConnect)
        self.button_disconnect.clicked.connect(self.button_disconnect_handle)
        self.bat_swap.clicked.connect(self.bat_swap_handle)

        #BUTTON START STOP
        self.bat_1_button_start.clicked.connect(self.bat_1_button_start_handle)
        self.bat_1_button_stop.clicked.connect(self.bat_1_button_stop_handle)
        self.bat_2_button_start.clicked.connect(self.bat_2_button_start_handle)
        self.bat_2_button_stop.clicked.connect(self.bat_2_button_stop_handle)
        self.bat_3_button_start.clicked.connect(self.bat_3_button_start_handle)
        self.bat_3_button_stop.clicked.connect(self.bat_3_button_stop_handle)
        self.bat_4_button_start.clicked.connect(self.bat_4_button_start_handle)
        self.bat_4_button_stop.clicked.connect(self.bat_4_button_stop_handle)
        self.bat_5_button_start.clicked.connect(self.bat_5_button_start_handle)
        self.bat_5_button_stop.clicked.connect(self.bat_5_button_stop_handle)
        self.bat_6_button_start.clicked.connect(self.bat_6_button_start_handle)
        self.bat_6_button_stop.clicked.connect(self.bat_6_button_stop_handle)
        self.bat_7_button_start.clicked.connect(self.bat_7_button_start_handle)
        self.bat_7_button_stop.clicked.connect(self.bat_7_button_stop_handle)
        self.bat_8_button_start.clicked.connect(self.bat_8_button_start_handle)
        self.bat_8_button_stop.clicked.connect(self.bat_8_button_stop_handle)

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
            self.bat_1_button_stop.setEnabled(True)
            self.bat_1_flagServ = self.bat_1_flagServ + 1
            if self.bat_1_flagServ == 1:
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
            if self.bat_1_swap == 0:
                self.bat_1_button_stop.setEnabled(False)

            self.bat_1_flagServ = 0
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
            self.bat_2_button_stop.setEnabled(True)
            self.bat_2_flagServ = self.bat_2_flagServ + 1
            if self.bat_2_flagServ == 1:
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
            if self.bat_2_swap == 0:
                self.bat_2_button_stop.setEnabled(False)

            self.bat_2_flagServ = 0
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

    #BAT 3 VARIABLE
    def bat_3_hole_id_handle(self, value):
        self.hole_3_msg_1 = 0xB0 << 20 | value
        self.hole_3_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_3_id.setText(str(value))
        self.bat_3_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_3_fault_code_handle(self, value):
        if value != 0:
            self.bat_3_button_stop.setEnabled(True)
            self.bat_3_flagServ = self.bat_3_flagServ + 1
            if self.bat_3_flagServ == 1:
                print(senddb(self.add3))

            if value == 7:
                self.err_code_3.setText("Over Charge")
                self.bat_3_batt_over_charge.setText("1")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")
        
            elif value == 8:
                self.err_code_3.setText("Batt Over Temp")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("1")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_3.setText("Bat Under Temp")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("1")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_3.setText("Bat Over Current")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("1")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_3.setText("Bat Over Volt")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("1")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_3.setText("Bat Short Circuit")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("1")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_3.setText("Bat Sistem Failure")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("1")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_3.setText("Charge Out Under Volt")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("1")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_3.setText("Charge Out Over Volt")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("1")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_3.setText("Charge Over Temp")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("1")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_3.setText("Charge Under Temp")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("1")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_3.setText("Charge Short Circuit")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("1")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_3.setText("Charge Over Current")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("1")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_3.setText("In Over Volt")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("1")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_3.setText("In Under Volt")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("1")
                self.bat_3_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_3.setText("Lost Communication")
                self.bat_3_batt_over_charge.setText("0")
                self.bat_3_batt_over_temp.setText("0")
                self.bat_3_batt_under_temp.setText("0")
                self.bat_3_batt_over_current.setText("0")
                self.bat_3_batt_over_voltage.setText("0")
                self.bat_3_batt_short_circuit.setText("0")
                self.bat_3_batt_system_failure.setText("0")
                self.bat_3_charge_out_under_voltage.setText("0")
                self.bat_3_charge_out_over_voltage.setText("0")
                self.bat_3_charge_over_temp.setText("0")
                self.bat_3_charge_under_temp.setText("0")
                self.bat_3_charge_short_circuit.setText("0")
                self.bat_3_charge_over_current.setText("0")
                self.bat_3_charge_in_over_voltage.setText("0")
                self.bat_3_charge_in_under_voltage.setText("0")
                self.bat_3_charge_lost_com.setText("1")
    
        else:
            if self.bat_3_swap == 0:
                self.bat_3_button_stop.setEnabled(False)

            self.bat_3_flagServ = 0
            self.err_code_3.setText("0")
            self.bat_3_batt_over_charge.setText("0")
            self.bat_3_batt_over_temp.setText("0")
            self.bat_3_batt_under_temp.setText("0")
            self.bat_3_batt_over_current.setText("0")
            self.bat_3_batt_over_voltage.setText("0")
            self.bat_3_batt_short_circuit.setText("0")
            self.bat_3_batt_system_failure.setText("0")
            self.bat_3_charge_out_under_voltage.setText("0")
            self.bat_3_charge_out_over_voltage.setText("0")
            self.bat_3_charge_over_temp.setText("0")
            self.bat_3_charge_under_temp.setText("0")
            self.bat_3_charge_short_circuit.setText("0")
            self.bat_3_charge_over_current.setText("0")
            self.bat_3_charge_in_over_voltage.setText("0")
            self.bat_3_charge_in_under_voltage.setText("0")
            self.bat_3_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_3_handshaking_handle(self, value):
        self.bat_3_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_3_voltage_handle(self, value):       
        self.bat_3_voltage.setText(value)   
        self.voltage_3.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_3_current_handle(self, value):
        self.bat_3_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_soc_handle(self, value):
        self.bat_3_soc.setText(value)
        self.soc_3.setText(value)
        self.progressBar_3.setValue(int(value))
        if self.bat_3_ChargeFLAG == 0:
            if self.bat_3_handshaking_status == 1:
                self.bat_3_button_start.setEnabled(True)
            self.progressBar_3.setPalette(self.l) if self.progressBar_3.value() <= 20 else self.progressBar_3.setPalette(self.p)
        else:
            self.bat_3_button_start.setEnabled(False)
            self.progressBar_3.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_3_temp_handle(self, value):
        self.bat_3_temp.setText(value)
        self.temp_3.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_capacity_handle(self, value):
        self.bat_3_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_soh_handle(self, value):
        self.bat_3_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_cycle_handle(self, value):
        self.bat_3_cycle.setText(value)
        QtWidgets.QApplication.processEvents()
    
    #BAT 4 VARIABLE
    def bat_4_hole_id_handle(self, value):
        self.hole_4_msg_1 = 0xB0 << 20 | value
        self.hole_4_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_4_id.setText(str(value))
        self.bat_4_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_4_fault_code_handle(self, value):
        if value != 0:
            self.bat_4_button_stop.setEnabled(True)
            self.bat_4_flagServ = self.bat_4_flagServ + 1
            if self.bat_4_flagServ == 1:
                print(senddb(self.add4))

            if value == 7:
                self.err_code_4.setText("Over Charge")
                self.bat_4_batt_over_charge.setText("1")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")
        
            elif value == 8:
                self.err_code_4.setText("Batt Over Temp")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("1")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_4.setText("Bat Under Temp")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("1")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_4.setText("Bat Over Current")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("1")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_4.setText("Bat Over Volt")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("1")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_4.setText("Bat Short Circuit")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("1")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_4.setText("Bat Sistem Failure")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("1")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_4.setText("Charge Out Under Volt")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("1")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_4.setText("Charge Out Over Volt")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("1")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_4.setText("Charge Over Temp")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("1")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_4.setText("Charge Under Temp")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("1")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_4.setText("Charge Short Circuit")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("1")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_4.setText("Charge Over Current")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("1")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_4.setText("In Over Volt")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("1")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_4.setText("In Under Volt")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("1")
                self.bat_4_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_4.setText("Lost Communication")
                self.bat_4_batt_over_charge.setText("0")
                self.bat_4_batt_over_temp.setText("0")
                self.bat_4_batt_under_temp.setText("0")
                self.bat_4_batt_over_current.setText("0")
                self.bat_4_batt_over_voltage.setText("0")
                self.bat_4_batt_short_circuit.setText("0")
                self.bat_4_batt_system_failure.setText("0")
                self.bat_4_charge_out_under_voltage.setText("0")
                self.bat_4_charge_out_over_voltage.setText("0")
                self.bat_4_charge_over_temp.setText("0")
                self.bat_4_charge_under_temp.setText("0")
                self.bat_4_charge_short_circuit.setText("0")
                self.bat_4_charge_over_current.setText("0")
                self.bat_4_charge_in_over_voltage.setText("0")
                self.bat_4_charge_in_under_voltage.setText("0")
                self.bat_4_charge_lost_com.setText("1")
    
        else:
            if self.bat_4_swap == 0:
                self.bat_4_button_stop.setEnabled(False)

            self.bat_4_flagServ = 0
            self.err_code_4.setText("0")
            self.bat_4_batt_over_charge.setText("0")
            self.bat_4_batt_over_temp.setText("0")
            self.bat_4_batt_under_temp.setText("0")
            self.bat_4_batt_over_current.setText("0")
            self.bat_4_batt_over_voltage.setText("0")
            self.bat_4_batt_short_circuit.setText("0")
            self.bat_4_batt_system_failure.setText("0")
            self.bat_4_charge_out_under_voltage.setText("0")
            self.bat_4_charge_out_over_voltage.setText("0")
            self.bat_4_charge_over_temp.setText("0")
            self.bat_4_charge_under_temp.setText("0")
            self.bat_4_charge_short_circuit.setText("0")
            self.bat_4_charge_over_current.setText("0")
            self.bat_4_charge_in_over_voltage.setText("0")
            self.bat_4_charge_in_under_voltage.setText("0")
            self.bat_4_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_4_handshaking_handle(self, value):
        self.bat_4_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_4_voltage_handle(self, value):       
        self.bat_4_voltage.setText(value)   
        self.voltage_4.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_4_current_handle(self, value):
        self.bat_4_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_soc_handle(self, value):
        self.bat_4_soc.setText(value)
        self.soc_4.setText(value)
        self.progressBar_4.setValue(int(value))
        if self.bat_4_ChargeFLAG == 0:
            if self.bat_4_handshaking_status == 1:
                self.bat_4_button_start.setEnabled(True)
            self.progressBar_4.setPalette(self.l) if self.progressBar_4.value() <= 20 else self.progressBar_4.setPalette(self.p)
        else:
            self.bat_4_button_start.setEnabled(False)
            self.progressBar_4.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_4_temp_handle(self, value):
        self.bat_4_temp.setText(value)
        self.temp_4.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_capacity_handle(self, value):
        self.bat_4_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_soh_handle(self, value):
        self.bat_4_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_cycle_handle(self, value):
        self.bat_4_cycle.setText(value)
        QtWidgets.QApplication.processEvents()

    #BAT 5 VARIABLE
    def bat_5_hole_id_handle(self, value):
        self.hole_5_msg_1 = 0xB0 << 20 | value
        self.hole_5_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_5_id.setText(str(value))
        self.bat_5_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_5_fault_code_handle(self, value):
        if value != 0:
            self.bat_5_button_stop.setEnabled(True)
            self.bat_5_flagServ = self.bat_5_flagServ + 1
            if self.bat_5_flagServ == 1:
                print(senddb(self.add5))

            if value == 7:
                self.err_code_5.setText("Over Charge")
                self.bat_5_batt_over_charge.setText("1")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")
        
            elif value == 8:
                self.err_code_5.setText("Batt Over Temp")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("1")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_5.setText("Bat Under Temp")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("1")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_5.setText("Bat Over Current")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("1")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_5.setText("Bat Over Volt")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("1")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_5.setText("Bat Short Circuit")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("1")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_5.setText("Bat Sistem Failure")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("1")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_5.setText("Charge Out Under Volt")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("1")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_5.setText("Charge Out Over Volt")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("1")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_5.setText("Charge Over Temp")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("1")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_5.setText("Charge Under Temp")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("1")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_5.setText("Charge Short Circuit")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("1")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_5.setText("Charge Over Current")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("1")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_5.setText("In Over Volt")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("1")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_5.setText("In Under Volt")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("1")
                self.bat_5_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_5.setText("Lost Communication")
                self.bat_5_batt_over_charge.setText("0")
                self.bat_5_batt_over_temp.setText("0")
                self.bat_5_batt_under_temp.setText("0")
                self.bat_5_batt_over_current.setText("0")
                self.bat_5_batt_over_voltage.setText("0")
                self.bat_5_batt_short_circuit.setText("0")
                self.bat_5_batt_system_failure.setText("0")
                self.bat_5_charge_out_under_voltage.setText("0")
                self.bat_5_charge_out_over_voltage.setText("0")
                self.bat_5_charge_over_temp.setText("0")
                self.bat_5_charge_under_temp.setText("0")
                self.bat_5_charge_short_circuit.setText("0")
                self.bat_5_charge_over_current.setText("0")
                self.bat_5_charge_in_over_voltage.setText("0")
                self.bat_5_charge_in_under_voltage.setText("0")
                self.bat_5_charge_lost_com.setText("1")
    
        else:
            if self.bat_5_swap == 0:
                self.bat_5_button_stop.setEnabled(False)

            self.bat_5_flagServ = 0
            self.err_code_5.setText("0")
            self.bat_5_batt_over_charge.setText("0")
            self.bat_5_batt_over_temp.setText("0")
            self.bat_5_batt_under_temp.setText("0")
            self.bat_5_batt_over_current.setText("0")
            self.bat_5_batt_over_voltage.setText("0")
            self.bat_5_batt_short_circuit.setText("0")
            self.bat_5_batt_system_failure.setText("0")
            self.bat_5_charge_out_under_voltage.setText("0")
            self.bat_5_charge_out_over_voltage.setText("0")
            self.bat_5_charge_over_temp.setText("0")
            self.bat_5_charge_under_temp.setText("0")
            self.bat_5_charge_short_circuit.setText("0")
            self.bat_5_charge_over_current.setText("0")
            self.bat_5_charge_in_over_voltage.setText("0")
            self.bat_5_charge_in_under_voltage.setText("0")
            self.bat_5_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_5_handshaking_handle(self, value):
        self.bat_5_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_5_voltage_handle(self, value):       
        self.bat_5_voltage.setText(value)   
        self.voltage_5.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_5_current_handle(self, value):
        self.bat_5_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_soc_handle(self, value):
        self.bat_5_soc.setText(value)
        self.soc_5.setText(value)
        self.progressBar_5.setValue(int(value))
        if self.bat_5_ChargeFLAG == 0:
            if self.bat_5_handshaking_status == 1:
                self.bat_5_button_start.setEnabled(True)
            self.progressBar_5.setPalette(self.l) if self.progressBar_5.value() <= 20 else self.progressBar_5.setPalette(self.p)
        else:
            self.bat_5_button_start.setEnabled(False)
            self.progressBar_5.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_5_temp_handle(self, value):
        self.bat_5_temp.setText(value)
        self.temp_5.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_capacity_handle(self, value):
        self.bat_5_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_soh_handle(self, value):
        self.bat_5_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_cycle_handle(self, value):
        self.bat_5_cycle.setText(value)
        QtWidgets.QApplication.processEvents()

    #BAT 6 VARIABLE
    def bat_6_hole_id_handle(self, value):
        self.hole_6_msg_1 = 0xB0 << 20 | value
        self.hole_6_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_6_id.setText(str(value))
        self.bat_6_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_6_fault_code_handle(self, value):
        if value != 0:
            self.bat_6_button_stop.setEnabled(True)
            self.bat_6_flagServ = self.bat_6_flagServ + 1
            if self.bat_6_flagServ == 1:
                print(senddb(self.add6))

            if value == 7:
                self.err_code_6.setText("Over Charge")
                self.bat_6_batt_over_charge.setText("1")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")
    
            elif value == 8:
                self.err_code_6.setText("Batt Over Temp")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("1")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_6.setText("Bat Under Temp")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("1")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_6.setText("Bat Over Current")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("1")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_6.setText("Bat Over Volt")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("1")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_6.setText("Bat Short Circuit")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("1")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_6.setText("Bat Sistem Failure")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("1")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_6.setText("Charge Out Under Volt")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("1")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_6.setText("Charge Out Over Volt")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("1")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_6.setText("Charge Over Temp")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("1")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_6.setText("Charge Under Temp")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("1")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_6.setText("Charge Short Circuit")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("1")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_6.setText("Charge Over Current")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("1")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_6.setText("In Over Volt")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("1")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_6.setText("In Under Volt")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("1")
                self.bat_6_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_6.setText("Lost Communication")
                self.bat_6_batt_over_charge.setText("0")
                self.bat_6_batt_over_temp.setText("0")
                self.bat_6_batt_under_temp.setText("0")
                self.bat_6_batt_over_current.setText("0")
                self.bat_6_batt_over_voltage.setText("0")
                self.bat_6_batt_short_circuit.setText("0")
                self.bat_6_batt_system_failure.setText("0")
                self.bat_6_charge_out_under_voltage.setText("0")
                self.bat_6_charge_out_over_voltage.setText("0")
                self.bat_6_charge_over_temp.setText("0")
                self.bat_6_charge_under_temp.setText("0")
                self.bat_6_charge_short_circuit.setText("0")
                self.bat_6_charge_over_current.setText("0")
                self.bat_6_charge_in_over_voltage.setText("0")
                self.bat_6_charge_in_under_voltage.setText("0")
                self.bat_6_charge_lost_com.setText("1")
    
        else:
            if self.bat_6_swap == 0:
                self.bat_6_button_stop.setEnabled(False)

            self.bat_6_flagServ = 0
            self.err_code_6.setText("0")
            self.bat_6_batt_over_charge.setText("0")
            self.bat_6_batt_over_temp.setText("0")
            self.bat_6_batt_under_temp.setText("0")
            self.bat_6_batt_over_current.setText("0")
            self.bat_6_batt_over_voltage.setText("0")
            self.bat_6_batt_short_circuit.setText("0")
            self.bat_6_batt_system_failure.setText("0")
            self.bat_6_charge_out_under_voltage.setText("0")
            self.bat_6_charge_out_over_voltage.setText("0")
            self.bat_6_charge_over_temp.setText("0")
            self.bat_6_charge_under_temp.setText("0")
            self.bat_6_charge_short_circuit.setText("0")
            self.bat_6_charge_over_current.setText("0")
            self.bat_6_charge_in_over_voltage.setText("0")
            self.bat_6_charge_in_under_voltage.setText("0")
            self.bat_6_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_6_handshaking_handle(self, value):
        self.bat_6_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_6_voltage_handle(self, value):       
        self.bat_6_voltage.setText(value)   
        self.voltage_6.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_6_current_handle(self, value):
        self.bat_6_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_soc_handle(self, value):
        self.bat_6_soc.setText(value)
        self.soc_6.setText(value)
        self.progressBar_6.setValue(int(value))
        if self.bat_6_ChargeFLAG == 0:
            if self.bat_6_handshaking_status == 1:
                self.bat_6_button_start.setEnabled(True)
            self.progressBar_6.setPalette(self.l) if self.progressBar_6.value() <= 20 else self.progressBar_6.setPalette(self.p)
        else:
            self.bat_6_button_start.setEnabled(False)
            self.progressBar_6.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_6_temp_handle(self, value):
        self.bat_6_temp.setText(value)
        self.temp_6.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_capacity_handle(self, value):
        self.bat_6_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_soh_handle(self, value):
        self.bat_6_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_cycle_handle(self, value):
        self.bat_6_cycle.setText(value)
        QtWidgets.QApplication.processEvents()

    #BAT 7 VARIABLE
    def bat_7_hole_id_handle(self, value):
        self.hole_7_msg_1 = 0xB0 << 20 | value
        self.hole_7_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_7_id.setText(str(value))
        self.bat_7_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_7_fault_code_handle(self, value):
        if value != 0:
            self.bat_7_button_stop.setEnabled(True)
            self.bat_7_flagServ = self.bat_7_flagServ + 1
            if self.bat_7_flagServ == 1:
                print(senddb(self.add7))

            if value == 7:
                self.err_code_7.setText("Over Charge")
                self.bat_7_batt_over_charge.setText("1")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")
        
            elif value == 8:
                self.err_code_7.setText("Batt Over Temp")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("1")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_7.setText("Bat Under Temp")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("1")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_7.setText("Bat Over Current")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("1")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_7.setText("Bat Over Volt")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("1")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_7.setText("Bat Short Circuit")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("1")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_7.setText("Bat Sistem Failure")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("1")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_7.setText("Charge Out Under Volt")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("1")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_7.setText("Charge Out Over Volt")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("1")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_7.setText("Charge Over Temp")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("1")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_7.setText("Charge Under Temp")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("1")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_7.setText("Charge Short Circuit")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("1")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_7.setText("Charge Over Current")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("1")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_7.setText("In Over Volt")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("1")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_7.setText("In Under Volt")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("1")
                self.bat_7_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_7.setText("Lost Communication")
                self.bat_7_batt_over_charge.setText("0")
                self.bat_7_batt_over_temp.setText("0")
                self.bat_7_batt_under_temp.setText("0")
                self.bat_7_batt_over_current.setText("0")
                self.bat_7_batt_over_voltage.setText("0")
                self.bat_7_batt_short_circuit.setText("0")
                self.bat_7_batt_system_failure.setText("0")
                self.bat_7_charge_out_under_voltage.setText("0")
                self.bat_7_charge_out_over_voltage.setText("0")
                self.bat_7_charge_over_temp.setText("0")
                self.bat_7_charge_under_temp.setText("0")
                self.bat_7_charge_short_circuit.setText("0")
                self.bat_7_charge_over_current.setText("0")
                self.bat_7_charge_in_over_voltage.setText("0")
                self.bat_7_charge_in_under_voltage.setText("0")
                self.bat_7_charge_lost_com.setText("1")
    
        else:
            if self.bat_7_swap == 0:
                self.bat_7_button_stop.setEnabled(False)

            self.bat_7_flagServ = 0
            self.err_code_7.setText("0")
            self.bat_7_batt_over_charge.setText("0")
            self.bat_7_batt_over_temp.setText("0")
            self.bat_7_batt_under_temp.setText("0")
            self.bat_7_batt_over_current.setText("0")
            self.bat_7_batt_over_voltage.setText("0")
            self.bat_7_batt_short_circuit.setText("0")
            self.bat_7_batt_system_failure.setText("0")
            self.bat_7_charge_out_under_voltage.setText("0")
            self.bat_7_charge_out_over_voltage.setText("0")
            self.bat_7_charge_over_temp.setText("0")
            self.bat_7_charge_under_temp.setText("0")
            self.bat_7_charge_short_circuit.setText("0")
            self.bat_7_charge_over_current.setText("0")
            self.bat_7_charge_in_over_voltage.setText("0")
            self.bat_7_charge_in_under_voltage.setText("0")
            self.bat_7_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_7_handshaking_handle(self, value):
        self.bat_7_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_7_voltage_handle(self, value):       
        self.bat_7_voltage.setText(value)   
        self.voltage_7.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_7_current_handle(self, value):
        self.bat_7_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_soc_handle(self, value):
        self.bat_7_soc.setText(value)
        self.soc_7.setText(value)
        self.progressBar_7.setValue(int(value))
        if self.bat_7_ChargeFLAG == 0:
            if self.bat_7_handshaking_status == 1:
                self.bat_7_button_start.setEnabled(True)
            self.progressBar_7.setPalette(self.l) if self.progressBar_7.value() <= 20 else self.progressBar_7.setPalette(self.p)
        else:
            self.bat_7_button_start.setEnabled(False)
            self.progressBar_7.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_7_temp_handle(self, value):
        self.bat_7_temp.setText(value)
        self.temp_7.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_capacity_handle(self, value):
        self.bat_7_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_soh_handle(self, value):
        self.bat_7_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_cycle_handle(self, value):
        self.bat_7_cycle.setText(value)
        QtWidgets.QApplication.processEvents()

    #BAT 8 VARIABLE
    def bat_8_hole_id_handle(self, value):
        self.hole_8_msg_1 = 0xB0 << 20 | value
        self.hole_8_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_8_id.setText(str(value))
        self.bat_8_id_1.setText(str(value))
        QtWidgets.QApplication.processEvents()
    def bat_8_fault_code_handle(self, value):
        if value != 0:
            self.bat_8_button_stop.setEnabled(True)
            self.bat_8_flagServ = self.bat_8_flagServ + 1
            if self.bat_8_flagServ == 1:
                print(senddb(self.add2))

            if value == 7:
                self.err_code_8.setText("Over Charge")
                self.bat_8_batt_over_charge.setText("1")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")
        
            elif value == 8:
                self.err_code_8.setText("Batt Over Temp")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("1")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")
            
            elif value == 9:
                self.err_code_8.setText("Bat Under Temp")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("1")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")

            elif value == 10:
                self.err_code_8.setText("Bat Over Current")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("1")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")
        
            elif value == 11:
                self.err_code_8.setText("Bat Over Volt")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("1")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")

            elif value == 12:
                self.err_code_8.setText("Bat Short Circuit")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("1")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")

            elif value == 13:
                self.err_code_8.setText("Bat Sistem Failure")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("1")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")

            elif value == 14:
                self.err_code_8.setText("Charge Out Under Volt")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("1")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")           

            elif value == 15:
                self.err_code_8.setText("Charge Out Over Volt")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("1")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")          

            elif value == 16:
                self.err_code_8.setText("Charge Over Temp")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("1")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0") 

            elif value == 17:
                self.err_code_8.setText("Charge Under Temp")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("1")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")        

            elif value == 18:
                self.err_code_8.setText("Charge Short Circuit")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("1")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")           

            elif value == 19:
                self.err_code_8.setText("Charge Over Current")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("1")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")      

            elif value == 20:
                self.err_code_8.setText("In Over Volt")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("1")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("0")         

            elif value == 21:
                self.err_code_8.setText("In Under Volt")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("1")
                self.bat_8_charge_lost_com.setText("0")           

            elif value == 22:
                self.err_code_8.setText("Lost Communication")
                self.bat_8_batt_over_charge.setText("0")
                self.bat_8_batt_over_temp.setText("0")
                self.bat_8_batt_under_temp.setText("0")
                self.bat_8_batt_over_current.setText("0")
                self.bat_8_batt_over_voltage.setText("0")
                self.bat_8_batt_short_circuit.setText("0")
                self.bat_8_batt_system_failure.setText("0")
                self.bat_8_charge_out_under_voltage.setText("0")
                self.bat_8_charge_out_over_voltage.setText("0")
                self.bat_8_charge_over_temp.setText("0")
                self.bat_8_charge_under_temp.setText("0")
                self.bat_8_charge_short_circuit.setText("0")
                self.bat_8_charge_over_current.setText("0")
                self.bat_8_charge_in_over_voltage.setText("0")
                self.bat_8_charge_in_under_voltage.setText("0")
                self.bat_8_charge_lost_com.setText("1")
    
        else:
            if self.bat_8_swap == 0:
                self.bat_8_button_stop.setEnabled(False)

            self.bat_8_flagServ = 0
            self.err_code_8.setText("0")
            self.bat_8_batt_over_charge.setText("0")
            self.bat_8_batt_over_temp.setText("0")
            self.bat_8_batt_under_temp.setText("0")
            self.bat_8_batt_over_current.setText("0")
            self.bat_8_batt_over_voltage.setText("0")
            self.bat_8_batt_short_circuit.setText("0")
            self.bat_8_batt_system_failure.setText("0")
            self.bat_8_charge_out_under_voltage.setText("0")
            self.bat_8_charge_out_over_voltage.setText("0")
            self.bat_8_charge_over_temp.setText("0")
            self.bat_8_charge_under_temp.setText("0")
            self.bat_8_charge_short_circuit.setText("0")
            self.bat_8_charge_over_current.setText("0")
            self.bat_8_charge_in_over_voltage.setText("0")
            self.bat_8_charge_in_under_voltage.setText("0")
            self.bat_8_charge_lost_com.setText("0")              

        QtWidgets.QApplication.processEvents()    
    def bat_8_handshaking_handle(self, value):
        self.bat_8_handshaking_status = value
        QtWidgets.QApplication.processEvents()
    def bat_8_voltage_handle(self, value):       
        self.bat_8_voltage.setText(value)   
        self.voltage_8.setText(value)       
        QtWidgets.QApplication.processEvents()
    def bat_8_current_handle(self, value):
        self.bat_8_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_soc_handle(self, value):
        self.bat_8_soc.setText(value)
        self.soc_8.setText(value)
        self.progressBar_8.setValue(int(value))
        if self.bat_8_ChargeFLAG == 0:
            if self.bat_8_handshaking_status == 1:
                self.bat_8_button_start.setEnabled(True)
            self.progressBar_8.setPalette(self.l) if self.progressBar_8.value() <= 20 else self.progressBar_8.setPalette(self.p)
        else:
            self.bat_8_button_start.setEnabled(False)
            self.progressBar_8.setPalette(self.c)
        QtWidgets.QApplication.processEvents()
    def bat_8_temp_handle(self, value):
        self.bat_8_temp.setText(value)
        self.temp_8.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_capacity_handle(self, value):
        self.bat_8_capacity.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_soh_handle(self, value):
        self.bat_8_soh.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_cycle_handle(self, value):
        self.bat_8_cycle.setText(value)
        QtWidgets.QApplication.processEvents()

    #START STOP FUNCTION   
    def bat_1_button_start_handle(self):        
        try:
            global loadData
            loadData.pop(0)
            loadData.insert(0,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_1_ChargeFLAG = 1
        except:
            self.bat_1_ChargeFLAG = 0

    def bat_1_button_stop_handle(self):
        try:
            global loadData
            self.bat_1_button_stop.setEnabled(False)
            loadData.pop(0)
            loadData.insert(0,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_1.setPalette(self.l)
            self.bat_1_button_stop.setEnabled(False)
            self.bat_1_swap = 0
            self.bat_1_ChargeFLAG = 0
        except:
            self.bat_1_ChargeFLAG = 1

    def bat_2_button_start_handle(self):
        try:
            global loadData
            loadData.pop(1)
            loadData.insert(1,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_2_ChargeFLAG = 1 
        except:
            self.bat_2_ChargeFLAG = 0
        
    def bat_2_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(1)
            loadData.insert(1,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_2.setPalette(self.l)
            self.bat_2_button_stop.setEnabled(False)
            self.bat_2_swap = 0
            self.bat_2_ChargeFLAG = 0
            
        except:
            self.bat_2_ChargeFLAG = 1

    def bat_3_button_start_handle(self):
        try:
            global loadData
            loadData.pop(2)
            loadData.insert(2,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_3_ChargeFLAG = 1 
        except:
            self.bat_3_ChargeFLAG = 0
        
    def bat_3_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(2)
            loadData.insert(2,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_3.setPalette(self.l)
            self.bat_3_button_stop.setEnabled(False)
            self.bat_3_swap = 0
            self.bat_3_ChargeFLAG = 0
            
        except:
            self.bat_3_ChargeFLAG = 1

    def bat_4_button_start_handle(self):
        try:
            global loadData
            loadData.pop(3)
            loadData.insert(3,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_4_ChargeFLAG = 1 
        except:
            self.bat_4_ChargeFLAG = 0
        
    def bat_4_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(3)
            loadData.insert(3,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_4.setPalette(self.l)
            self.bat_4_button_stop.setEnabled(False)
            self.bat_4_swap = 0
            self.bat_4_ChargeFLAG = 0
            
        except:
            self.bat_4_ChargeFLAG = 1

    def bat_5_button_start_handle(self):
        try:
            global loadData
            loadData.pop(4)
            loadData.insert(4,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_5_ChargeFLAG = 1 
        except:
            self.bat_5_ChargeFLAG = 0
        
    def bat_5_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(4)
            loadData.insert(4,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_5.setPalette(self.l)
            self.bat_5_button_stop.setEnabled(False)
            self.bat_5_swap = 0
            self.bat_5_ChargeFLAG = 0
            
        except:
            self.bat_5_ChargeFLAG = 1

    def bat_6_button_start_handle(self):
        try:
            global loadData
            loadData.pop(5)
            loadData.insert(5,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_6_ChargeFLAG = 1 
        except:
            self.bat_6_ChargeFLAG = 0
        
    def bat_6_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(5)
            loadData.insert(5,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_6.setPalette(self.l)
            self.bat_6_button_stop.setEnabled(False)
            self.bat_6_swap = 0
            self.bat_6_ChargeFLAG = 0
            
        except:
            self.bat_6_ChargeFLAG = 1

    def bat_7_button_start_handle(self):
        try:
            global loadData
            loadData.pop(6)
            loadData.insert(6,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_7_ChargeFLAG = 1 
        except:
            self.bat_7_ChargeFLAG = 0
        
    def bat_7_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(6)
            loadData.insert(6,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_7.setPalette(self.l)
            self.bat_7_button_stop.setEnabled(False)
            self.bat_7_swap = 0
            self.bat_7_ChargeFLAG = 0
            
        except:
            self.bat_7_ChargeFLAG = 1

    def bat_8_button_start_handle(self):
        try:
            global loadData
            loadData.pop(7)
            loadData.insert(7,1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.bat_8_ChargeFLAG = 1 
        except:
            self.bat_8_ChargeFLAG = 0
        
    def bat_8_button_stop_handle(self):
        try:
            global loadData
            loadData.pop(7)
            loadData.insert(7,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            bus.send(self.sendmsg)
            self.status_8.setPalette(self.l)
            self.bat_8_button_stop.setEnabled(False)
            self.bat_8_swap = 0
            self.bat_8_ChargeFLAG = 0
            
        except:
            self.bat_8_ChargeFLAG = 1

    ##SWAP FUNCTION
    def bat_swap_handle(self):
        j = 0
        soc = [float(self.bat_1_soc.text()), float(self.bat_2_soc.text()), float(self.bat_3_soc.text()), float(self.bat_4_soc.text()), float(self.bat_5_soc.text()), float(self.bat_6_soc.text()), float(self.bat_7_soc.text()), float(self.bat_8_soc.text())] 
        for i in range(0, (len(soc) - 1)):
            if soc[j] < soc[i+1]:
                j = i + 1

        #self.bat_swap.setText("hole {} ready".format(j+1))
        if j == 0:
            self.bat_1_button_stop.setEnabled(True)
            self.bat_1_swap = 1
        if j == 1:
            self.bat_2_button_stop.setEnabled(True)
            self.bat_2_swap = 1
        if j == 2:
            self.bat_3_button_stop.setEnabled(True)
            self.bat_3_swap = 1
        if j == 3:
            self.bat_4_button_stop.setEnabled(True)
            self.bat_4_swap = 1
        if j == 4:
            self.bat_5_button_stop.setEnabled(True)
            self.bat_5_swap = 1
        if j == 5:
            self.bat_6_button_stop.setEnabled(True)
            self.bat_6_swap = 1
        if j == 6:
            self.bat_7_button_stop.setEnabled(True)
            self.bat_7_swap = 1
        if j == 7:
            self.bat_8_button_stop.setEnabled(True)
            self.bat_8_swap = 1

    ##BUTTON CONNECTION  
    def button_disconnect_handle(self):
        try: 
            global flagConnect
            global loadData

            flagConnect = 0
            os.system("sudo ip link set {} down".format(CHANNEL))    
            self.button_connect.setEnabled(True)
            self.button_disconnect.setEnabled(False)
            loadData = [0, 0, 0, 0, 0, 0, 0, 0]
            self.bat_1_button_start.setEnabled(False)
            self.bat_2_button_start.setEnabled(False)
            self.bat_3_button_start.setEnabled(False)
            self.bat_4_button_start.setEnabled(False)
            self.bat_5_button_start.setEnabled(False)
            self.bat_6_button_start.setEnabled(False)
            self.bat_7_button_start.setEnabled(False)
            self.bat_8_button_start.setEnabled(False)

            self.status_1.setEnabled(False)
            self.status_2.setEnabled(False)
            self.status_3.setEnabled(False)
            self.status_4.setEnabled(False)
            self.status_5.setEnabled(False)
            self.status_6.setEnabled(False)
            self.status_7.setEnabled(False)
            self.status_8.setEnabled(False)

        except:
            self.status_connect.setText("Canbus disconnecting failed")

    def canConnect(self):           ##try to parse data
        try:
            global flagConnect
            global loadData
            global bus

            flagConnect = 1

            os.system("sudo ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))

            self.cansend.start()
            bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')
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

            while True:
                self.msg = bus.recv()
                toc = time.perf_counter()
                timm = toc - tic
                
                #SendCanTime = "".join("{:0.2f}".format(timm % CanTime))
                SendDbTime = "".join("{:0.2f}".format(timm % DBtime))
                self.add = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_1_id.text() , self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_batt_over_charge.text(), self.bat_1_batt_over_temp.text(), self.bat_1_batt_under_temp.text(), self.bat_1_batt_over_current.text(), self.bat_1_batt_over_voltage.text(), self.bat_1_batt_short_circuit.text(), self.bat_1_batt_system_failure.text(), self.bat_1_charge_out_under_voltage.text(), self.bat_1_charge_out_over_voltage.text(), self.bat_1_charge_over_temp.text(), self.bat_1_charge_under_temp.text(), self.bat_1_charge_short_circuit.text(), self.bat_1_charge_over_current.text(), self.bat_1_charge_in_over_voltage.text(), self.bat_1_charge_in_under_voltage.text(), self.bat_1_charge_lost_com.text())
                self.add2 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_2_id.text() , self.bat_2_voltage.text(), self.bat_2_current.text(), self.bat_2_soc.text(), self.bat_2_temp.text(), self.bat_2_capacity.text(), self.bat_2_soh.text(), self.bat_2_cycle.text(), self.bat_2_batt_over_charge.text(), self.bat_2_batt_over_temp.text(), self.bat_2_batt_under_temp.text(), self.bat_2_batt_over_current.text(), self.bat_2_batt_over_voltage.text(), self.bat_2_batt_short_circuit.text(), self.bat_2_batt_system_failure.text(), self.bat_2_charge_out_under_voltage.text(), self.bat_2_charge_out_over_voltage.text(), self.bat_2_charge_over_temp.text(), self.bat_2_charge_under_temp.text(), self.bat_2_charge_short_circuit.text(), self.bat_2_charge_over_current.text(), self.bat_2_charge_in_over_voltage.text(), self.bat_2_charge_in_under_voltage.text(), self.bat_2_charge_lost_com.text()) 
                self.add3 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_3_id.text() , self.bat_3_voltage.text(), self.bat_3_current.text(), self.bat_3_soc.text(), self.bat_3_temp.text(), self.bat_3_capacity.text(), self.bat_3_soh.text(), self.bat_3_cycle.text(), self.bat_3_batt_over_charge.text(), self.bat_3_batt_over_temp.text(), self.bat_3_batt_under_temp.text(), self.bat_3_batt_over_current.text(), self.bat_3_batt_over_voltage.text(), self.bat_3_batt_short_circuit.text(), self.bat_3_batt_system_failure.text(), self.bat_3_charge_out_under_voltage.text(), self.bat_3_charge_out_over_voltage.text(), self.bat_3_charge_over_temp.text(), self.bat_3_charge_under_temp.text(), self.bat_3_charge_short_circuit.text(), self.bat_3_charge_over_current.text(), self.bat_3_charge_in_over_voltage.text(), self.bat_3_charge_in_under_voltage.text(), self.bat_3_charge_lost_com.text())
                self.add4 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_4_id.text() , self.bat_4_voltage.text(), self.bat_4_current.text(), self.bat_4_soc.text(), self.bat_4_temp.text(), self.bat_4_capacity.text(), self.bat_4_soh.text(), self.bat_4_cycle.text(), self.bat_4_batt_over_charge.text(), self.bat_4_batt_over_temp.text(), self.bat_4_batt_under_temp.text(), self.bat_4_batt_over_current.text(), self.bat_4_batt_over_voltage.text(), self.bat_4_batt_short_circuit.text(), self.bat_4_batt_system_failure.text(), self.bat_4_charge_out_under_voltage.text(), self.bat_4_charge_out_over_voltage.text(), self.bat_4_charge_over_temp.text(), self.bat_4_charge_under_temp.text(), self.bat_4_charge_short_circuit.text(), self.bat_4_charge_over_current.text(), self.bat_4_charge_in_over_voltage.text(), self.bat_4_charge_in_under_voltage.text(), self.bat_4_charge_lost_com.text())
                self.add5 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_5_id.text() , self.bat_5_voltage.text(), self.bat_5_current.text(), self.bat_5_soc.text(), self.bat_5_temp.text(), self.bat_5_capacity.text(), self.bat_5_soh.text(), self.bat_5_cycle.text(), self.bat_5_batt_over_charge.text(), self.bat_5_batt_over_temp.text(), self.bat_5_batt_under_temp.text(), self.bat_5_batt_over_current.text(), self.bat_5_batt_over_voltage.text(), self.bat_5_batt_short_circuit.text(), self.bat_5_batt_system_failure.text(), self.bat_5_charge_out_under_voltage.text(), self.bat_5_charge_out_over_voltage.text(), self.bat_5_charge_over_temp.text(), self.bat_5_charge_under_temp.text(), self.bat_5_charge_short_circuit.text(), self.bat_5_charge_over_current.text(), self.bat_5_charge_in_over_voltage.text(), self.bat_5_charge_in_under_voltage.text(), self.bat_5_charge_lost_com.text())
                self.add6 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_6_id.text() , self.bat_6_voltage.text(), self.bat_6_current.text(), self.bat_6_soc.text(), self.bat_6_temp.text(), self.bat_6_capacity.text(), self.bat_6_soh.text(), self.bat_6_cycle.text(), self.bat_6_batt_over_charge.text(), self.bat_6_batt_over_temp.text(), self.bat_6_batt_under_temp.text(), self.bat_6_batt_over_current.text(), self.bat_6_batt_over_voltage.text(), self.bat_6_batt_short_circuit.text(), self.bat_6_batt_system_failure.text(), self.bat_6_charge_out_under_voltage.text(), self.bat_6_charge_out_over_voltage.text(), self.bat_6_charge_over_temp.text(), self.bat_6_charge_under_temp.text(), self.bat_6_charge_short_circuit.text(), self.bat_6_charge_over_current.text(), self.bat_6_charge_in_over_voltage.text(), self.bat_6_charge_in_under_voltage.text(), self.bat_6_charge_lost_com.text())
                self.add7 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_7_id.text() , self.bat_7_voltage.text(), self.bat_7_current.text(), self.bat_7_soc.text(), self.bat_7_temp.text(), self.bat_7_capacity.text(), self.bat_7_soh.text(), self.bat_7_cycle.text(), self.bat_7_batt_over_charge.text(), self.bat_7_batt_over_temp.text(), self.bat_7_batt_under_temp.text(), self.bat_7_batt_over_current.text(), self.bat_7_batt_over_voltage.text(), self.bat_7_batt_short_circuit.text(), self.bat_7_batt_system_failure.text(), self.bat_7_charge_out_under_voltage.text(), self.bat_7_charge_out_over_voltage.text(), self.bat_7_charge_over_temp.text(), self.bat_7_charge_under_temp.text(), self.bat_7_charge_short_circuit.text(), self.bat_7_charge_over_current.text(), self.bat_7_charge_in_over_voltage.text(), self.bat_7_charge_in_under_voltage.text(), self.bat_7_charge_lost_com.text())
                self.add8 = ("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},0,0,0,0,0,0,0,0").format(self.bat_8_id.text() , self.bat_8_voltage.text(), self.bat_8_current.text(), self.bat_8_soc.text(), self.bat_8_temp.text(), self.bat_8_capacity.text(), self.bat_8_soh.text(), self.bat_8_cycle.text(), self.bat_8_batt_over_charge.text(), self.bat_8_batt_over_temp.text(), self.bat_8_batt_under_temp.text(), self.bat_8_batt_over_current.text(), self.bat_8_batt_over_voltage.text(), self.bat_8_batt_short_circuit.text(), self.bat_8_batt_system_failure.text(), self.bat_8_charge_out_under_voltage.text(), self.bat_8_charge_out_over_voltage.text(), self.bat_8_charge_over_temp.text(), self.bat_8_charge_under_temp.text(), self.bat_8_charge_short_circuit.text(), self.bat_8_charge_over_current.text(), self.bat_8_charge_in_over_voltage.text(), self.bat_8_charge_in_under_voltage.text(), self.bat_8_charge_lost_com.text())
                
                ## THE ARBITRATION_ID MAY CHANGE WHEN TRYING ON REAL BMS
                
                #HOLE 1                
                if self.msg.arbitration_id == 0x0C1:
                    self.BAT_1_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_1_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_1_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                
                if self.bat_1_handshaking_status == 1:
                    self.status_1.setPalette(self.p)

                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB1 = self.flagDB1 + 1
                        if self.flagDB1 == 1:
                            print(senddb(self.add))
                    else:
                        self.flagDB1 = 0
                    
                    #read Battery Data
                    if self.msg.arbitration_id == self.hole_1_msg_1:
                        self.BAT_1_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_1_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_1_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_1_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                       
                    if self.msg.arbitration_id == self.hole_1_msg_2:
                        self.BAT_1_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_1_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_1_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_1.setPalette(self.l)
                    self.bat_1_button_start.setEnabled(False)
                    
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
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB2 = self.flagDB2 + 1
                        if self.flagDB2 == 1:
                            print(senddb(self.add2))
                    else:
                        self.flagDB2 = 0 
                    
                    #read battery data
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
                    self.bat_2_button_start.setEnabled(False)

                    self.BAT_2_VOLTAGE.emit("0")
                    self.BAT_2_CURRENT.emit("0")
                    self.BAT_2_SOC.emit("0")
                    self.BAT_2_TEMP.emit("0")
                    self.BAT_2_CAPACITY.emit("0")
                    self.BAT_2_SOH.emit("0")
                    self.BAT_2_CYCLE.emit("0")
                    self.BAT_2_FAULT_CODE.emit(0)

                #HOLE 3
                if self.msg.arbitration_id == 0x0C3:
                    self.BAT_3_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_3_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_3_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_3_handshaking_status == 1:
                    self.status_3.setPalette(self.p)
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB3 = self.flagDB3 + 1
                        if self.flagDB3 == 1:
                            print(senddb(self.add3))
                    else:
                        self.flagDB3 = 0 
                    
                    #read battery data
                    if self.msg.arbitration_id == self.hole_3_msg_1:
                        self.BAT_3_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_3_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_3_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_3_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_3_msg_2:
                        self.BAT_3_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_3_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_3_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_3.setPalette(self.l)
                    self.bat_3_button_start.setEnabled(False)

                    self.BAT_3_VOLTAGE.emit("0")
                    self.BAT_3_CURRENT.emit("0")
                    self.BAT_3_SOC.emit("0")
                    self.BAT_3_TEMP.emit("0")
                    self.BAT_3_CAPACITY.emit("0")
                    self.BAT_3_SOH.emit("0")
                    self.BAT_3_CYCLE.emit("0")
                    self.BAT_3_FAULT_CODE.emit(0)
                
                #HOLE 4
                if self.msg.arbitration_id == 0x0C4:
                    self.BAT_4_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_4_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_4_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_4_handshaking_status == 1:
                    self.status_4.setPalette(self.p)
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB4 = self.flagDB4 + 1
                        if self.flagDB4 == 1:
                            print(senddb(self.add4))
                    else:
                        self.flagDB4 = 0 
                    
                    #read battery data
                    if self.msg.arbitration_id == self.hole_4_msg_1:
                        self.BAT_4_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_4_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_4_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_4_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_4_msg_2:
                        self.BAT_4_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_4_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_4_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_4.setPalette(self.l)
                    self.bat_4_button_start.setEnabled(False)

                    self.BAT_4_VOLTAGE.emit("0")
                    self.BAT_4_CURRENT.emit("0")
                    self.BAT_4_SOC.emit("0")
                    self.BAT_4_TEMP.emit("0")
                    self.BAT_4_CAPACITY.emit("0")
                    self.BAT_4_SOH.emit("0")
                    self.BAT_4_CYCLE.emit("0")
                    self.BAT_4_FAULT_CODE.emit(0)

                #HOLE 5
                if self.msg.arbitration_id == 0x0C5:
                    self.BAT_5_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_5_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_5_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_5_handshaking_status == 1:
                    self.status_5.setPalette(self.p)
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB5 = self.flagDB5 + 1
                        if self.flagDB5 == 1:
                            print(senddb(self.add5))
                    else:
                        self.flagDB5 = 0 
                    
                    #read battery data
                    if self.msg.arbitration_id == self.hole_5_msg_1:
                        self.BAT_5_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_5_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_5_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_5_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_5_msg_2:
                        self.BAT_5_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_5_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_5_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_5.setPalette(self.l)
                    self.bat_5_button_start.setEnabled(False)

                    self.BAT_5_VOLTAGE.emit("0")
                    self.BAT_5_CURRENT.emit("0")
                    self.BAT_5_SOC.emit("0")
                    self.BAT_5_TEMP.emit("0")
                    self.BAT_5_CAPACITY.emit("0")
                    self.BAT_5_SOH.emit("0")
                    self.BAT_5_CYCLE.emit("0")
                    self.BAT_5_FAULT_CODE.emit(0)

                #HOLE 6
                if self.msg.arbitration_id == 0x0C6:
                    self.BAT_6_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_6_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_6_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_6_handshaking_status == 1:
                    self.status_6.setPalette(self.p)
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB6 = self.flagDB6 + 1
                        if self.flagDB6 == 1:
                            print(senddb(self.add6))
                    else:
                        self.flagDB6 = 0 
                    
                    #read battery data
                    if self.msg.arbitration_id == self.hole_6_msg_1:
                        self.BAT_6_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_6_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_6_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_6_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_6_msg_2:
                        self.BAT_6_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_6_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_6_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_6.setPalette(self.l)
                    self.bat_6_button_start.setEnabled(False)

                    self.BAT_6_VOLTAGE.emit("0")
                    self.BAT_6_CURRENT.emit("0")
                    self.BAT_6_SOC.emit("0")
                    self.BAT_6_TEMP.emit("0")
                    self.BAT_6_CAPACITY.emit("0")
                    self.BAT_6_SOH.emit("0")
                    self.BAT_6_CYCLE.emit("0")
                    self.BAT_6_FAULT_CODE.emit(0)

                #HOLE 7
                if self.msg.arbitration_id == 0x0C7:
                    self.BAT_7_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_7_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_7_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_7_handshaking_status == 1:
                    self.status_7.setPalette(self.p)
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB7 = self.flagDB7 + 1
                        if self.flagDB7 == 1:
                            print(senddb(self.add7))
                    else:
                        self.flagDB7 = 0 
                    
                    #read battery data
                    if self.msg.arbitration_id == self.hole_7_msg_1:
                        self.BAT_7_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_7_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_7_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_7_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_7_msg_2:
                        self.BAT_7_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_7_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_7_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_7.setPalette(self.l)
                    self.bat_7_button_start.setEnabled(False)

                    self.BAT_7_VOLTAGE.emit("0")
                    self.BAT_7_CURRENT.emit("0")
                    self.BAT_7_SOC.emit("0")
                    self.BAT_7_TEMP.emit("0")
                    self.BAT_7_CAPACITY.emit("0")
                    self.BAT_7_SOH.emit("0")
                    self.BAT_7_CYCLE.emit("0")
                    self.BAT_7_FAULT_CODE.emit(0)

                #HOLE 8
                if self.msg.arbitration_id == 0x0C8:
                    self.BAT_8_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_8_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_8_HANDSHAKING.emit(int(frameparse(self.msg, "handshaking")))
                                    
                if self.bat_8_handshaking_status == 1:
                    self.status_8.setPalette(self.p)
                    
                    #send DB
                    if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):           #modulus tidak selalu tepat(dihitung selisih dengan waktu eksekusi baris progam lainnya)
                        self.flagDB8 = self.flagDB8 + 1
                        if self.flagDB8 == 1:
                            print(senddb(self.add8))
                    else:
                        self.flagDB8 = 0 
                    
                    #read battery data
                    if self.msg.arbitration_id == self.hole_8_msg_1:
                        self.BAT_8_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_8_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_8_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_8_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_8_msg_2:
                        self.BAT_8_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_8_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_8_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                    
                else:
                    self.status_8.setPalette(self.l)
                    self.bat_8_button_start.setEnabled(False)

                    self.BAT_8_VOLTAGE.emit("0")
                    self.BAT_8_CURRENT.emit("0")
                    self.BAT_8_SOC.emit("0")
                    self.BAT_8_TEMP.emit("0")
                    self.BAT_8_CAPACITY.emit("0")
                    self.BAT_8_SOH.emit("0")
                    self.BAT_8_CYCLE.emit("0")
                    self.BAT_8_FAULT_CODE.emit(0)
            
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

            self.BAT_3_VOLTAGE.emit("0")
            self.BAT_3_CURRENT.emit("0")
            self.BAT_3_SOC.emit("0")
            self.BAT_3_TEMP.emit("0")
            self.BAT_3_CAPACITY.emit("0")
            self.BAT_3_SOH.emit("0")
            self.BAT_3_CYCLE.emit("0")
            self.bat_3_id_1.setText("")
            self.bat_3_id.setText("")
            self.err_code_3.setText("0")
            self.BAT_3_FAULT_CODE.emit(0)

            self.BAT_4_VOLTAGE.emit("0")
            self.BAT_4_CURRENT.emit("0")
            self.BAT_4_SOC.emit("0")
            self.BAT_4_TEMP.emit("0")
            self.BAT_4_CAPACITY.emit("0")
            self.BAT_4_SOH.emit("0")
            self.BAT_4_CYCLE.emit("0")
            self.bat_4_id_1.setText("")
            self.bat_4_id.setText("")
            self.err_code_4.setText("0")
            self.BAT_4_FAULT_CODE.emit(0)

            self.BAT_5_VOLTAGE.emit("0")
            self.BAT_5_CURRENT.emit("0")
            self.BAT_5_SOC.emit("0")
            self.BAT_5_TEMP.emit("0")
            self.BAT_5_CAPACITY.emit("0")
            self.BAT_5_SOH.emit("0")
            self.BAT_5_CYCLE.emit("0")
            self.bat_5_id_1.setText("")
            self.bat_5_id.setText("")
            self.err_code_5.setText("0")
            self.BAT_5_FAULT_CODE.emit(0)

            self.BAT_6_VOLTAGE.emit("0")
            self.BAT_6_CURRENT.emit("0")
            self.BAT_6_SOC.emit("0")
            self.BAT_6_TEMP.emit("0")
            self.BAT_6_CAPACITY.emit("0")
            self.BAT_6_SOH.emit("0")
            self.BAT_6_CYCLE.emit("0")
            self.bat_6_id_1.setText("")
            self.bat_6_id.setText("")
            self.err_code_6.setText("0")
            self.BAT_6_FAULT_CODE.emit(0)

            self.BAT_7_VOLTAGE.emit("0")
            self.BAT_7_CURRENT.emit("0")
            self.BAT_7_SOC.emit("0")
            self.BAT_7_TEMP.emit("0")
            self.BAT_7_CAPACITY.emit("0")
            self.BAT_7_SOH.emit("0")
            self.BAT_7_CYCLE.emit("0")
            self.bat_7_id_1.setText("")
            self.bat_7_id.setText("")
            self.err_code_7.setText("0")
            self.BAT_7_FAULT_CODE.emit(0)

            self.BAT_8_VOLTAGE.emit("0")
            self.BAT_8_CURRENT.emit("0")
            self.BAT_8_SOC.emit("0")
            self.BAT_8_TEMP.emit("0")
            self.BAT_8_CAPACITY.emit("0")
            self.BAT_8_SOH.emit("0")
            self.BAT_8_CYCLE.emit("0")
            self.bat_8_id_1.setText("")
            self.bat_8_id.setText("")
            self.err_code_8.setText("0")
            self.BAT_8_FAULT_CODE.emit(0)

class CanSend(QtCore.QThread):
    def run(self):
        global bus
        bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')
        while True:
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = loadData, extended_id=False)
            if flagConnect == 1:
                bus.send(self.sendmsg)
            time.sleep(2)          
        
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
    floatformat = "{:4.2f}"

    if type == "bat_id":
        formatted_data = (frame.data[0] << 16) + (frame.data[1] << 8) + frame.data[2] 
        return formatted_data

    if type == "fault_code":
        formatted_data = frame.data[3]
        return formatted_data

    if type == "handshaking":
        formatted_data = frame.data[4]
        return formatted_data

    if type == "bat_voltage":
        x = (frame.data[1] << 8) + frame.data[0]
        formatted_data = int(x) 
        return formatted_data / 100 

    elif type == "bat_current":
        x = (frame.data[3] << 8) + frame.data[2]
        formatted_data = int(x) / 100 - 50
        return floatformat.format(formatted_data)

    elif type == "bat_soc":
        x = (frame.data[5] << 8) + frame.data[4]
        formatted_data = int(x) / 100 
        if formatted_data > 100: 
            formatted_data = 100
        return "{:4.0f}".format(formatted_data)

    elif type == "bat_temp":
        x = (frame.data[7] << 8) + frame.data[6]
        formatted_data = int(x) / 10 - 40
        return floatformat.format(formatted_data)

    elif type == "bat_capacity":
        x = (frame.data[1] << 8) + frame.data[0]
        formatted_data = int(x) / 100
        return formatted_data

    elif type == "bat_soh":
        x = (frame.data[3] << 8) + frame.data[2]
        formatted_data = int(x)
        return formatted_data

    elif type == "bat_cycle":
        x = (frame.data[5] << 8) + frame.data[4]
        formatted_data = int(x)
        return formatted_data

if __name__ == "__main__":
    window = QApplication(sys.argv)
    ui = MainClass()
    ui.show()
    #ui.showFullScreen()
    window.exec_()

