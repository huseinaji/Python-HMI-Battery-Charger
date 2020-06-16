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
DBtime = 30
CanTime = 2
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "mqtt/subscribe"

class MainClass(QDialog, interface.Ui_MainWindow):
    
    loadData = [0, 0, 0, 0, 0, 0, 0, 0]

    BAT_1_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_1_FAULT_CODE = QtCore.pyqtSignal(int)
    BAT_1_HANDSHACKING = QtCore.pyqtSignal(int)
    BAT_1_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_1_CURRENT = QtCore.pyqtSignal(str)
    BAT_1_SOC = QtCore.pyqtSignal(str)
    BAT_1_TEMP = QtCore.pyqtSignal(str)
    BAT_1_CAPACITY = QtCore.pyqtSignal(str)
    BAT_1_SOH = QtCore.pyqtSignal(str)
    BAT_1_CYCLE = QtCore.pyqtSignal(str)

    BAT_2_HOLE_ID = QtCore.pyqtSignal(int)
    BAT_2_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_2_CURRENT = QtCore.pyqtSignal(str)
    BAT_2_SOC = QtCore.pyqtSignal(str)
    BAT_2_TEMP = QtCore.pyqtSignal(str)
    BAT_2_CAPACITY = QtCore.pyqtSignal(str)
    BAT_2_SOH = QtCore.pyqtSignal(str)
    BAT_2_CYCLE = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.i = 0
        self.val = 1
        self.setupUi(self)
        self.handshacking_1_status = 0

        self.BAT_1_HOLE_ID.connect(self.bat_1_hole_id_handle)
        self.BAT_1_FAULT_CODE.connect(self.bat_1_fault_code_handle)
        self.BAT_1_HANDSHACKING.connect(self.bat_1_handshacking_handle)
        self.BAT_1_VOLTAGE.connect(self.bat_1_voltage_handle)
        self.BAT_1_CURRENT.connect(self.bat_1_current_handle)
        self.BAT_1_SOC.connect(self.bat_1_soc_handle)
        self.BAT_1_TEMP.connect(self.bat_1_temp_handle)
        self.BAT_1_CAPACITY.connect(self.bat_1_capacity_handle)
        self.BAT_1_SOH.connect(self.bat_1_soh_handle)
        self.BAT_1_CYCLE.connect(self.bat_1_cycle_handle)

        self.BAT_2_VOLTAGE.connect(self.bat_2_voltage_handle)
        self.BAT_2_CURRENT.connect(self.bat_2_current_handle)
        self.BAT_2_SOC.connect(self.bat_2_soc_handle)
        self.BAT_2_TEMP.connect(self.bat_2_temp_handle)
        self.BAT_2_CAPACITY.connect(self.bat_2_capacity_handle)
        self.BAT_2_SOH.connect(self.bat_2_soh_handle)
        self.BAT_2_CYCLE.connect(self.bat_2_cycle_handle)

        self.button_connect.clicked.connect(self.canConnect)
        self.button_disconnect.clicked.connect(self.button_disconnect_handle)
        self.button_send_data.clicked.connect(self.button_send_data_handle)
        self.bat_1_button_start.clicked.connect(self.bat_1_button_start_handle)
        self.bat_1_button_stop.clicked.connect(self.bat_1_button_stop_handle)
        self.bat_2_button_start.clicked.connect(self.bat_2_button_start_handle)
        self.bat_2_button_stop.clicked.connect(self.bat_2_button_stop_handle)

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
        self.l.setColor(QtGui.QPalette.Highlight, QtGui.QColor(QtCore.Qt.red))
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
    
    ## every handle method below affected by every single canbus signal transmit
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
                url = ("http://charging.genmotorcycles.com/index.php?bat_id={}&volt={}&curr={}&soc={}&temp={}&capc={}&soh={}&cycle={}&B_over_charge={}&B_over_temp={}&B_under_temp={}&B_over_curr={}&B_over_volt={}&B_short_cirr={}&B_sys_failure={}&C_out_u_volt={}&C_out_o_volt={}&C_over_temp={}&C_under_temp={}&C_short_cirr={}&C_over_curr={}&C_in_o_voltage={}&C_in_u_voltage={}&C_lost_conn={}&doc=0&dot=0&dut=0&odc=0&imb=0&cs=0&ds=0&ss=0").format(self.bat_1_id.text() , self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_batt_over_charge.text(), self.bat_1_batt_over_temp.text(), self.bat_1_batt_under_temp.text(), self.bat_1_batt_over_current.text(), self.bat_1_batt_over_voltage.text(), self.bat_1_batt_short_circuit.text(), self.bat_1_batt_system_failure.text(), self.bat_1_charge_out_under_voltage.text(), self.bat_1_charge_out_over_voltage.text(), self.bat_1_charge_over_temp.text(), self.bat_1_charge_under_temp.text(), self.bat_1_charge_short_circuit.text(), self.bat_1_charge_over_current.text(), self.bat_1_charge_in_over_voltage.text(), self.bat_1_charge_in_under_voltage.text(), self.bat_1_charge_lost_com.text())
                webUrl = urllib.request.urlopen(url)
                print("result code " + str(webUrl.getcode()))

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
    def bat_1_handshacking_handle(self, value):
        self.handshacking_1_status = value
        #print(self.handshacking_1_status)        
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
        self.progressBar.setPalette(self.l) if self.progressBar.value() <= 20 else self.progressBar.setPalette(self.p)
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
        self.progressBar_2.setPalette(self.l) if self.progressBar_2.value() <= 20 else self.progressBar_2.setPalette(self.p)
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
   
    def button_send_data_handle(self):
        url = ("http://charging.genmotorcycles.com/index.php?bat_id={:x}&volt={}&curr={}&soc={}&temp={}&capc={}&soh={}&cycle={}&doc=0&coc={}&sc={}&dot=0&dut=0&cot={}&cut={}&uv={}&ov={}&odc=0&imb=0&sf={}&cs=0&ds=0&ss=0").format(self.hole_1_msg_1, self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_batt_over_current.text(),self.bat_1_batt_short_circuit, self.bat_1_batt_over_temp.text(), self.bat_1_batt_under_temp.text(), self.bat_1_charge_out_under_voltage.text(), self.bat_1_batt_over_voltage.text(), self.bat_1_system_failure.text())
        webUrl = urllib.request.urlopen(url)
        #self.status_connect.setText(str(webUrl.getcode()))
        print("result code " + str(webUrl.getcode()))
        
    def bat_1_button_start_handle(self):
        try:
            #self.bat_1_button_start.setEnabled(False)
            self.bat_1_button_stop.setEnabled(True)
            self.loadData.pop(0)
            self.loadData.insert(0, 1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
            self.bus.send(self.sendmsg)
            self.charging_status.setText("Hole 1 charging started")    
        except:
            self.charging_status.setText("Hole 1 charging starting failed")

    def bat_1_button_stop_handle(self):    
        try:
            #self.bat_1_button_stop.setEnabled(False)
            self.loadData.pop(0)
            self.loadData.insert(0,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
            self.bus.send(self.sendmsg)
            self.charging_status.setText("Hole 1 charging stopped")

            ##reset the display value
            self.bat_1_id.setText("0")
            self.bat_1_id_1.setText("0")
            self.voltage_1.setText("0")
            self.temp_1.setText("0")
            self.err_code_1.setText("0")
            self.bat_1_voltage.setText("0")
            self.bat_1_current.setText("0")
            self.bat_1_temp.setText("0")
            self.bat_1_soc.setText("0")
            self.progressBar.setValue(0)
            self.bat_1_capacity.setText("0")
            self.bat_1_soh.setText("0")
            self.bat_1_cycle.setText("0")
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

        except:
            self.charging_status.setText("Hole 1 charging failed to stop")    

    def bat_2_button_start_handle(self):
        try:
            self.bat_2_button_start.setEnabled(False)
            self.bat_2_button_stop.setEnabled(True)
            self.loadData.pop(2)
            self.loadData.insert(2, 1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id = False)
            self.bus.send(self.sendmsg)
            self.charging_status.setText("Hole 2 charging started")    
        except:
            self.charging_status.setText("Hole 2 charging starting failed")

    def bat_2_button_stop_handle(self):
        try:
            self.bat_2_button_stop.setEnabled(False)
            self.loadData.pop(2)
            self.loadData.insert(2,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id = False)
            self.bus.send(self.sendmsg)

            self.charging_status.setText("Hole 2 charging stopped")
        except:
            self.charging_status.setText("Hole 2 charging failed to stop")    

    def mqtt_connect(self, client, userdata, flags, rc):
        self.status_connect.setText("Connected with result code " + str(rc))
        print("Connected with result code " + str(rc))

    def button_disconnect_handle(self):
        try: 
            os.system("sudo ip link set {} down".format(CHANNEL))
            self.status_connect.setText("Canbus disconnected")
            self.button_connect.setEnabled(True)
            self.button_disconnect.setEnabled(False)
        except:
            self.status_connect.setText("Canbus disconnecting failed")

    def canConnect(self):           ##try to parse data
        try:
            flagDB = 0
            flagCAN = 0
            self.flagServ = 0
            tic = time.perf_counter()
            os.system("sudo ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))
            self.bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')
            self.status_connect.setText("Canbus initiating sucess")
            self.button_connect.setEnabled(False)
            self.button_disconnect.setEnabled(True)
            
            while True:
                self.msg = self.bus.recv()
                toc = time.perf_counter()
                timm = toc - tic
                SendCanTime = "".join("{:0.2f}".format(timm % CanTime))
                #SendCanTime = timm % CanTime
                SendDbTime = "".join("{:0.2f}".format(timm % DBtime))
                #SendDbTime = timm % DBtime

                ## THE ARBITRATION_ID MAY CHANGE WHEN TRYING ON REAL BMS
                if self.msg.arbitration_id == 0x0C1:
                    self.bat_1_button_start.setEnabled(True)
                    self.BAT_1_HOLE_ID.emit(int(frameparse(self.msg, "bat_id")))          
                    self.BAT_1_FAULT_CODE.emit(frameparse(self.msg, "fault_code"))
                    self.BAT_1_HANDSHACKING.emit(int(frameparse(self.msg, "handshaking")))
                
                if self.handshacking_1_status == 1:
                    self.charging_status.setText("Hole 1 Connection success")
                    if self.msg.arbitration_id == self.hole_1_msg_1:
                        self.BAT_1_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_1_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_1_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_1_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_1_msg_2:
                        self.BAT_1_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_1_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_1_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                
                if (float(SendDbTime) > 0) & (float(SendDbTime) < 1):
                    flagDB = flagDB + 1
                    if flagDB == 1:
                        #print("xxx")
                        #url = ("http://charging.genmotorcycles.com/index.php?bat_id=b0ffff2&volt=50&curr=4&soc=0&temp=0&capc=0&soh=0&cycle=0&B_over_charge=0&B_over_temp=0&B_under_temp=0&B_over_curr=0&B_over_volt=0&B_short_cirr=0&B_sys_failure=0&C_out_u_volt=0&C_out_o_volt=0&C_over_temp=0&C_under_temp=0&C_short_cirr=0&C_over_curr=0&C_in_o_voltage=0&C_in_u_voltage=0&C_lost_conn=0&doc=0&dot=0&dut=0&odc=0&imb=0&cs=0&ds=0&ss=0")
                        #print("{}".format(self.bat_1_id.text()))
                        url = ("http://charging.genmotorcycles.com/index.php?bat_id={}&volt={}&curr={}&soc={}&temp={}&capc={}&soh={}&cycle={}&B_over_charge={}&B_over_temp={}&B_under_temp={}&B_over_curr={}&B_over_volt={}&B_short_cirr={}&B_sys_failure={}&C_out_u_volt={}&C_out_o_volt={}&C_over_temp={}&C_under_temp={}&C_short_cirr={}&C_over_curr={}&C_in_o_voltage={}&C_in_u_voltage={}&C_lost_conn={}&doc=0&dot=0&dut=0&odc=0&imb=0&cs=0&ds=0&ss=0").format(self.bat_1_id.text() , self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_batt_over_charge.text(), self.bat_1_batt_over_temp.text(), self.bat_1_batt_under_temp.text(), self.bat_1_batt_over_current.text(), self.bat_1_batt_over_voltage.text(), self.bat_1_batt_short_circuit.text(), self.bat_1_batt_system_failure.text(), self.bat_1_charge_out_under_voltage.text(), self.bat_1_charge_out_over_voltage.text(), self.bat_1_charge_over_temp.text(), self.bat_1_charge_under_temp.text(), self.bat_1_charge_short_circuit.text(), self.bat_1_charge_over_current.text(), self.bat_1_charge_in_over_voltage.text(), self.bat_1_charge_in_under_voltage.text(), self.bat_1_charge_lost_com.text())
                        webUrl = urllib.request.urlopen(url)
                        print("result code " + str(webUrl.getcode()))
                else:
                    flagDB = 0
                
                #print(float(SendCanTime))    
                if (float(SendCanTime) > 0.0) & (float(SendCanTime) < 1.0):
                    
                    flagCAN = flagCAN + 1
                    #print(flagCAN)
                    if flagCAN == 1:
                        #print("xxx")       
                        self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData, is_extended_id=False)
                        self.bus.send(self.sendmsg) 
                else:
                    flagCAN = 0
                
        except:
            self.status_connect.setText("Canbus initiating failed")

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
        formatted_data = int(x, 16) 
        return formatted_data

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
    V    1. ngirim data nang database / menit gawe timer
    3. develop multithread / timer
    '''
