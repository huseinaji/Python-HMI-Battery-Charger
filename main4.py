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

A = 60
B = 55.1
C = "iso cuyy"
MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "mqtt/subscribe"

class MainClass(QDialog, interface.Ui_MainWindow):
    FLAG = 0
    loadData = [0, 0, 0, 0]

    HOLE_1_ID = QtCore.pyqtSignal(int)
    HOLE_2_ID = QtCore.pyqtSignal(int)
    FAULT_CODE_1 = QtCore.pyqtSignal(int)
    HANDSHACKING_1 = QtCore.pyqtSignal(int)

    BAT_1_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_1_CURRENT = QtCore.pyqtSignal(str)
    BAT_1_SOC = QtCore.pyqtSignal(str)
    BAT_1_TEMP = QtCore.pyqtSignal(str)
    BAT_1_CAPACITY = QtCore.pyqtSignal(str)
    BAT_1_SOH = QtCore.pyqtSignal(str)
    BAT_1_CYCLE = QtCore.pyqtSignal(str)

    BAT_1_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_1_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_1_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_1_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_1_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_1_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_1_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_1_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_1_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_1_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_2_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_2_CURRENT = QtCore.pyqtSignal(str)
    BAT_2_SOC = QtCore.pyqtSignal(str)
    BAT_2_TEMP = QtCore.pyqtSignal(str)
    BAT_2_CAPACITY = QtCore.pyqtSignal(str)
    BAT_2_SOH = QtCore.pyqtSignal(str)
    BAT_2_CYCLE = QtCore.pyqtSignal(str)

    BAT_2_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_2_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_2_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_2_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_2_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_2_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_2_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_2_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_2_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_2_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_3_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_3_CURRENT = QtCore.pyqtSignal(str)
    BAT_3_SOC = QtCore.pyqtSignal(str)
    BAT_3_TEMP = QtCore.pyqtSignal(str)
    BAT_3_CAPACITY = QtCore.pyqtSignal(str)
    BAT_3_SOH = QtCore.pyqtSignal(str)
    BAT_3_CYCLE = QtCore.pyqtSignal(str)
    
    BAT_3_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_3_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_3_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_3_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_3_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_3_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_3_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_3_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_3_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_3_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_4_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_4_CURRENT = QtCore.pyqtSignal(str)
    BAT_4_SOC = QtCore.pyqtSignal(str)
    BAT_4_TEMP = QtCore.pyqtSignal(str)
    BAT_4_CAPACITY = QtCore.pyqtSignal(str)
    BAT_4_SOH = QtCore.pyqtSignal(str)
    BAT_4_CYCLE = QtCore.pyqtSignal(str)
    
    BAT_4_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_4_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_4_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_4_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_4_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_4_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_4_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_4_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_4_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_4_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_5_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_5_CURRENT = QtCore.pyqtSignal(str)
    BAT_5_SOC = QtCore.pyqtSignal(str)
    BAT_5_TEMP = QtCore.pyqtSignal(str)
    BAT_5_CAPACITY = QtCore.pyqtSignal(str)
    BAT_5_SOH = QtCore.pyqtSignal(str)
    BAT_5_CYCLE = QtCore.pyqtSignal(str)
    
    BAT_5_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_5_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_5_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_5_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_5_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_5_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_5_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_5_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_5_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_5_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_6_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_6_CURRENT = QtCore.pyqtSignal(str)
    BAT_6_SOC = QtCore.pyqtSignal(str)
    BAT_6_TEMP = QtCore.pyqtSignal(str)
    BAT_6_CAPACITY = QtCore.pyqtSignal(str)
    BAT_6_SOH = QtCore.pyqtSignal(str)
    BAT_6_CYCLE = QtCore.pyqtSignal(str)
    
    BAT_6_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_6_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_6_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_6_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_6_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_6_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_6_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_6_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_6_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_6_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_7_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_7_CURRENT = QtCore.pyqtSignal(str)
    BAT_7_SOC = QtCore.pyqtSignal(str)
    BAT_7_TEMP = QtCore.pyqtSignal(str)
    BAT_7_CAPACITY = QtCore.pyqtSignal(str)
    BAT_7_SOH = QtCore.pyqtSignal(str)
    BAT_7_CYCLE = QtCore.pyqtSignal(str)
    
    BAT_7_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_7_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_7_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_7_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_7_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_7_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_7_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_7_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_7_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_7_SLEEP_STATE = QtCore.pyqtSignal(str)

    BAT_8_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_8_CURRENT = QtCore.pyqtSignal(str)
    BAT_8_SOC = QtCore.pyqtSignal(str)
    BAT_8_TEMP = QtCore.pyqtSignal(str)
    BAT_8_CAPACITY = QtCore.pyqtSignal(str)
    BAT_8_SOH = QtCore.pyqtSignal(str)
    BAT_8_CYCLE = QtCore.pyqtSignal(str)
    
    BAT_8_CHARGE_OVER_CURRENT = QtCore.pyqtSignal(str)
    BAT_8_CHARGE_OVER_TEMP = QtCore.pyqtSignal(str)
    BAT_8_CHARGE_UNDER_TEMP = QtCore.pyqtSignal(str)
    BAT_8_UNDER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_8_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_8_OVER_VOLTAGE = QtCore.pyqtSignal(str)
    BAT_8_SHORT_CIRCUIT = QtCore.pyqtSignal(str)
    BAT_8_SYSTEM_FAILURE = QtCore.pyqtSignal(str)
    BAT_8_CHARGE_STATE = QtCore.pyqtSignal(str)
    BAT_8_SLEEP_STATE = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.i = 0
        self.val = 1
        self.setupUi(self)
        self.handshacking_1_status = 0

        self.HOLE_1_ID.connect(self.hole_1_id_handle)
        self.FAULT_CODE_1.connect(self.fault_code_1_handle)
        self.HANDSHACKING_1.connect(self.handshacking_1_handle)

        self.BAT_1_VOLTAGE.connect(self.bat_1_voltage_handle)
        self.BAT_1_CURRENT.connect(self.bat_1_current_handle)
        self.BAT_1_SOC.connect(self.bat_1_soc_handle)
        self.BAT_1_TEMP.connect(self.bat_1_temp_handle)
        self.BAT_1_CAPACITY.connect(self.bat_1_capacity_handle)
        self.BAT_1_SOH.connect(self.bat_1_soh_handle)
        self.BAT_1_CYCLE.connect(self.bat_1_cycle_handle)

        '''
        self.BAT_1_CHARGE_OVER_CURRENT.connect(self.bat_1_charge_over_current_handle)
        self.BAT_1_SHORT_CIRCUIT.connect(self.bat_1_short_circuit_handle)
        self.BAT_1_CHARGE_OVER_TEMP.connect(self.bat_1_charge_over_temp_handle)
        self.BAT_1_CHARGE_UNDER_TEMP.connect(self.bat_1_charge_under_temp_handle)
        self.BAT_1_UNDER_VOLTAGE.connect(self.bat_1_under_voltage_handle)
        self.BAT_1_OVER_VOLTAGE.connect(self.bat_1_over_voltage_handle)
        self.BAT_1_SYSTEM_FAILURE.connect(self.bat_1_system_failure_handle)
        self.BAT_1_CHARGE_STATE.connect(self.bat_1_charge_state_handle)
        self.BAT_1_SLEEP_STATE.connect(self.bat_1_sleep_state_handle)
        '''

        self.BAT_2_VOLTAGE.connect(self.bat_2_voltage_handle)
        self.BAT_2_CURRENT.connect(self.bat_2_current_handle)
        self.BAT_2_SOC.connect(self.bat_2_soc_handle)
        self.BAT_2_TEMP.connect(self.bat_2_temp_handle)
        self.BAT_2_CAPACITY.connect(self.bat_2_capacity_handle)
        self.BAT_2_SOH.connect(self.bat_2_soh_handle)
        self.BAT_2_CYCLE.connect(self.bat_2_cycle_handle)

        self.BAT_2_CHARGE_OVER_CURRENT.connect(self.bat_2_charge_over_current_handle)
        self.BAT_2_SHORT_CIRCUIT.connect(self.bat_2_short_circuit_handle)
        self.BAT_2_CHARGE_OVER_TEMP.connect(self.bat_2_charge_over_temp_handle)
        self.BAT_2_CHARGE_UNDER_TEMP.connect(self.bat_2_charge_under_temp_handle)
        self.BAT_2_UNDER_VOLTAGE.connect(self.bat_2_under_voltage_handle)
        self.BAT_2_OVER_VOLTAGE.connect(self.bat_2_over_voltage_handle)
        self.BAT_2_SYSTEM_FAILURE.connect(self.bat_2_system_failure_handle)
        self.BAT_2_CHARGE_STATE.connect(self.bat_2_charge_state_handle)
        self.BAT_2_SLEEP_STATE.connect(self.bat_2_sleep_state_handle)
        
        self.BAT_3_VOLTAGE.connect(self.bat_3_voltage_handle)
        self.BAT_3_CURRENT.connect(self.bat_3_current_handle)
        self.BAT_3_SOC.connect(self.bat_3_soc_handle)
        self.BAT_3_TEMP.connect(self.bat_3_temp_handle)
        self.BAT_3_CAPACITY.connect(self.bat_3_capacity_handle)
        self.BAT_3_SOH.connect(self.bat_3_soh_handle)
        self.BAT_3_CYCLE.connect(self.bat_3_cycle_handle)

        self.BAT_3_CHARGE_OVER_CURRENT.connect(self.bat_3_charge_over_current_handle)
        self.BAT_3_SHORT_CIRCUIT.connect(self.bat_3_short_circuit_handle)
        self.BAT_3_CHARGE_OVER_TEMP.connect(self.bat_3_charge_over_temp_handle)
        self.BAT_3_CHARGE_UNDER_TEMP.connect(self.bat_3_charge_under_temp_handle)
        self.BAT_3_UNDER_VOLTAGE.connect(self.bat_3_under_voltage_handle)
        self.BAT_3_OVER_VOLTAGE.connect(self.bat_3_over_voltage_handle)
        self.BAT_3_SYSTEM_FAILURE.connect(self.bat_3_system_failure_handle)
        self.BAT_3_CHARGE_STATE.connect(self.bat_3_charge_state_handle)
        self.BAT_3_SLEEP_STATE.connect(self.bat_3_sleep_state_handle)

        self.BAT_4_VOLTAGE.connect(self.bat_4_voltage_handle)
        self.BAT_4_CURRENT.connect(self.bat_4_current_handle)
        self.BAT_4_SOC.connect(self.bat_4_soc_handle)
        self.BAT_4_TEMP.connect(self.bat_4_temp_handle)
        self.BAT_4_CAPACITY.connect(self.bat_4_capacity_handle)
        self.BAT_4_SOH.connect(self.bat_4_soh_handle)
        self.BAT_4_CYCLE.connect(self.bat_4_cycle_handle)

        self.BAT_4_CHARGE_OVER_CURRENT.connect(self.bat_4_charge_over_current_handle)
        self.BAT_4_SHORT_CIRCUIT.connect(self.bat_4_short_circuit_handle)
        self.BAT_4_CHARGE_OVER_TEMP.connect(self.bat_4_charge_over_temp_handle)
        self.BAT_4_CHARGE_UNDER_TEMP.connect(self.bat_4_charge_under_temp_handle)
        self.BAT_4_UNDER_VOLTAGE.connect(self.bat_4_under_voltage_handle)
        self.BAT_4_OVER_VOLTAGE.connect(self.bat_4_over_voltage_handle)
        self.BAT_4_SYSTEM_FAILURE.connect(self.bat_4_system_failure_handle)
        self.BAT_4_CHARGE_STATE.connect(self.bat_4_charge_state_handle)
        self.BAT_4_SLEEP_STATE.connect(self.bat_4_sleep_state_handle)

        self.BAT_5_VOLTAGE.connect(self.bat_5_voltage_handle)
        self.BAT_5_CURRENT.connect(self.bat_5_current_handle)
        self.BAT_5_SOC.connect(self.bat_5_soc_handle)
        self.BAT_5_TEMP.connect(self.bat_5_temp_handle)
        self.BAT_5_CAPACITY.connect(self.bat_5_capacity_handle)
        self.BAT_5_SOH.connect(self.bat_5_soh_handle)
        self.BAT_5_CYCLE.connect(self.bat_5_cycle_handle)

        self.BAT_5_CHARGE_OVER_CURRENT.connect(self.bat_5_charge_over_current_handle)
        self.BAT_5_SHORT_CIRCUIT.connect(self.bat_5_short_circuit_handle)
        self.BAT_5_CHARGE_OVER_TEMP.connect(self.bat_5_charge_over_temp_handle)
        self.BAT_5_CHARGE_UNDER_TEMP.connect(self.bat_5_charge_under_temp_handle)
        self.BAT_5_UNDER_VOLTAGE.connect(self.bat_5_under_voltage_handle)
        self.BAT_5_OVER_VOLTAGE.connect(self.bat_5_over_voltage_handle)
        self.BAT_5_SYSTEM_FAILURE.connect(self.bat_5_system_failure_handle)
        self.BAT_5_CHARGE_STATE.connect(self.bat_5_charge_state_handle)
        self.BAT_5_SLEEP_STATE.connect(self.bat_5_sleep_state_handle)

        self.BAT_6_VOLTAGE.connect(self.bat_6_voltage_handle)
        self.BAT_6_CURRENT.connect(self.bat_6_current_handle)
        self.BAT_6_SOC.connect(self.bat_6_soc_handle)
        self.BAT_6_TEMP.connect(self.bat_6_temp_handle)
        self.BAT_6_CAPACITY.connect(self.bat_6_capacity_handle)
        self.BAT_6_SOH.connect(self.bat_6_soh_handle)
        self.BAT_6_CYCLE.connect(self.bat_6_cycle_handle)

        self.BAT_6_CHARGE_OVER_CURRENT.connect(self.bat_6_charge_over_current_handle)
        self.BAT_6_SHORT_CIRCUIT.connect(self.bat_6_short_circuit_handle)
        self.BAT_6_CHARGE_OVER_TEMP.connect(self.bat_6_charge_over_temp_handle)
        self.BAT_6_CHARGE_UNDER_TEMP.connect(self.bat_6_charge_under_temp_handle)
        self.BAT_6_UNDER_VOLTAGE.connect(self.bat_6_under_voltage_handle)
        self.BAT_6_OVER_VOLTAGE.connect(self.bat_6_over_voltage_handle)
        self.BAT_6_SYSTEM_FAILURE.connect(self.bat_6_system_failure_handle)
        self.BAT_6_CHARGE_STATE.connect(self.bat_6_charge_state_handle)
        self.BAT_6_SLEEP_STATE.connect(self.bat_6_sleep_state_handle)
    
        self.BAT_7_VOLTAGE.connect(self.bat_7_voltage_handle)
        self.BAT_7_CURRENT.connect(self.bat_7_current_handle)
        self.BAT_7_SOC.connect(self.bat_7_soc_handle)
        self.BAT_7_TEMP.connect(self.bat_7_temp_handle)
        self.BAT_7_CAPACITY.connect(self.bat_7_capacity_handle)
        self.BAT_7_SOH.connect(self.bat_7_soh_handle)
        self.BAT_7_CYCLE.connect(self.bat_7_cycle_handle)

        self.BAT_7_CHARGE_OVER_CURRENT.connect(self.bat_7_charge_over_current_handle)
        self.BAT_7_SHORT_CIRCUIT.connect(self.bat_7_short_circuit_handle)
        self.BAT_7_CHARGE_OVER_TEMP.connect(self.bat_7_charge_over_temp_handle)
        self.BAT_7_CHARGE_UNDER_TEMP.connect(self.bat_7_charge_under_temp_handle)
        self.BAT_7_UNDER_VOLTAGE.connect(self.bat_7_under_voltage_handle)
        self.BAT_7_OVER_VOLTAGE.connect(self.bat_7_over_voltage_handle)
        self.BAT_7_SYSTEM_FAILURE.connect(self.bat_7_system_failure_handle)
        self.BAT_7_CHARGE_STATE.connect(self.bat_7_charge_state_handle)
        self.BAT_7_SLEEP_STATE.connect(self.bat_7_sleep_state_handle)

        self.BAT_8_VOLTAGE.connect(self.bat_8_voltage_handle)
        self.BAT_8_CURRENT.connect(self.bat_8_current_handle)
        self.BAT_8_SOC.connect(self.bat_8_soc_handle)
        self.BAT_8_TEMP.connect(self.bat_8_temp_handle)
        self.BAT_8_CAPACITY.connect(self.bat_8_capacity_handle)
        self.BAT_8_SOH.connect(self.bat_8_soh_handle)
        self.BAT_8_CYCLE.connect(self.bat_8_cycle_handle)

        self.BAT_8_CHARGE_OVER_CURRENT.connect(self.bat_8_charge_over_current_handle)
        self.BAT_8_SHORT_CIRCUIT.connect(self.bat_8_short_circuit_handle)
        self.BAT_8_CHARGE_OVER_TEMP.connect(self.bat_8_charge_over_temp_handle)
        self.BAT_8_CHARGE_UNDER_TEMP.connect(self.bat_8_charge_under_temp_handle)
        self.BAT_8_UNDER_VOLTAGE.connect(self.bat_8_under_voltage_handle)
        self.BAT_8_OVER_VOLTAGE.connect(self.bat_8_over_voltage_handle)
        self.BAT_8_SYSTEM_FAILURE.connect(self.bat_8_system_failure_handle)
        self.BAT_8_CHARGE_STATE.connect(self.bat_8_charge_state_handle)
        self.BAT_8_SLEEP_STATE.connect(self.bat_8_sleep_state_handle)

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

    #def do_something(self):
    #    print("clickable")
    ''' 
    def dialValue(self):
        pass
        
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
    '''
    
    ## every handle method below affected by every single canbus signal transmit
    def hole_1_id_handle(self, value):
        self.hole_1_msg_1 = 0xB0 << 20 | value
        self.hole_1_msg_2 = 0xB1 << 20 | value
        value = "".join("{:x}".format(value))
        self.bat_1_id.setText(str(value))
        self.bat_1_id_1.setText(str(value))
        #print("{:x}".format(self.hole_1_msg_2))
        QtWidgets.QApplication.processEvents()
    
    def fault_code_1_handle(self, value):
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

        elif value == 0:
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
    
    def handshacking_1_handle(self, value):
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
    '''
    def bat_1_charge_over_current_handle(self, value):
        #self.bat_1_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_short_circuit_handle(self, value):
        #self.bat_1_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_charge_over_temp_handle(self, value):
        #self.bat_1_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_charge_under_temp_handle(self, value):
        #self.bat_1_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_under_voltage_handle(self, value):
        #self.bat_1_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_over_voltage_handle(self, value):
        #self.bat_1_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_system_failure_handle(self, value):
        #self.bat_1_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_charge_state_handle(self, value):
        #self.bat_1_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_1_sleep_state_handle(self, value):
        #self.bat_1_sleep_state.setText(value)
        QtWidgets.QApplication.processEvents()
    '''
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
    def bat_2_charge_over_current_handle(self, value):
        self.bat_2_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_short_circuit_handle(self, value):
        self.bat_2_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_charge_over_temp_handle(self, value):
        self.bat_2_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_charge_under_temp_handle(self, value):
        self.bat_2_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_under_voltage_handle(self, value):
        self.bat_2_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_over_voltage_handle(self, value):
        self.bat_2_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_system_failure_handle(self, value):
        self.bat_2_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_charge_state_handle(self, value):
        self.bat_2_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_2_sleep_state_handle(self, value):
        self.bat_2_sleep_state.setText(value)
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
        self.progressBar_3.setPalette(self.l) if self.progressBar_3.value() <= 20 else self.progressBar_3.setPalette(self.p)
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
    def bat_3_charge_over_current_handle(self, value):
        self.bat_3_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_short_circuit_handle(self, value):
        self.bat_3_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_charge_over_temp_handle(self, value):
        self.bat_3_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_charge_under_temp_handle(self, value):
        self.bat_3_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_under_voltage_handle(self, value):
        self.bat_3_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_over_voltage_handle(self, value):
        self.bat_3_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_system_failure_handle(self, value):
        self.bat_3_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_charge_state_handle(self, value):
        self.bat_3_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_3_sleep_state_handle(self, value):
        self.bat_3_sleep_state.setText(value)
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
        self.progressBar_4.setPalette(self.l) if self.progressBar_4.value() <= 20 else self.progressBar_4.setPalette(self.p)
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
    def bat_4_charge_over_current_handle(self, value):
        self.bat_4_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_short_circuit_handle(self, value):
        self.bat_4_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_charge_over_temp_handle(self, value):
        self.bat_4_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_charge_under_temp_handle(self, value):
        self.bat_4_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_under_voltage_handle(self, value):
        self.bat_4_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_over_voltage_handle(self, value):
        self.bat_4_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_system_failure_handle(self, value):
        self.bat_4_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_charge_state_handle(self, value):
        self.bat_4_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_4_sleep_state_handle(self, value):
        self.bat_4_sleep_state.setText(value)
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
        self.progressBar_5.setPalette(self.l) if self.progressBar_2.value() <= 20 else self.progressBar_2.setPalette(self.p)
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
    def bat_5_charge_over_current_handle(self, value):
        self.bat_5_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_short_circuit_handle(self, value):
        self.bat_5_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_charge_over_temp_handle(self, value):
        self.bat_5_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_charge_under_temp_handle(self, value):
        self.bat_5_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_under_voltage_handle(self, value):
        self.bat_5_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_over_voltage_handle(self, value):
        self.bat_5_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_system_failure_handle(self, value):
        self.bat_5_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_charge_state_handle(self, value):
        self.bat_5_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_5_sleep_state_handle(self, value):
        self.bat_5_sleep_state.setText(value)
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
        self.progressBar_6.setPalette(self.l) if self.progressBar_6.value() <= 20 else self.progressBar_6.setPalette(self.p)
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
    def bat_6_charge_over_current_handle(self, value):
        self.bat_6_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_short_circuit_handle(self, value):
        self.bat_6_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_charge_over_temp_handle(self, value):
        self.bat_6_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_charge_under_temp_handle(self, value):
        self.bat_6_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_under_voltage_handle(self, value):
        self.bat_6_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_over_voltage_handle(self, value):
        self.bat_6_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_system_failure_handle(self, value):
        self.bat_6_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_charge_state_handle(self, value):
        self.bat_6_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_6_sleep_state_handle(self, value):
        self.bat_6_sleep_state.setText(value)
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
        self.progressBar_7.setPalette(self.l) if self.progressBar_7.value() <= 20 else self.progressBar_7.setPalette(self.p)
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
    def bat_7_charge_over_current_handle(self, value):
        self.bat_7_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_short_circuit_handle(self, value):
        self.bat_7_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_charge_over_temp_handle(self, value):
        self.bat_7_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_charge_under_temp_handle(self, value):
        self.bat_7_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_under_voltage_handle(self, value):
        self.bat_7_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_over_voltage_handle(self, value):
        self.bat_7_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_system_failure_handle(self, value):
        self.bat_7_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_charge_state_handle(self, value):
        self.bat_7_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_7_sleep_state_handle(self, value):
        self.bat_7_sleep_state.setText(value)
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
        self.progressBar_8.setPalette(self.l) if self.progressBar_8.value() <= 20 else self.progressBar_8.setPalette(self.p)
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
    def bat_8_charge_over_current_handle(self, value):
        self.bat_8_charge_over_current.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_short_circuit_handle(self, value):
        self.bat_8_short_circuit.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_charge_over_temp_handle(self, value):
        self.bat_8_charge_over_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_charge_under_temp_handle(self, value):
        self.bat_8_charge_under_temp.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_under_voltage_handle(self, value):
        self.bat_8_under_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_over_voltage_handle(self, value):
        self.bat_8_over_voltage.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_system_failure_handle(self, value):
        self.bat_8_system_failure.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_charge_state_handle(self, value):
        self.bat_8_charger_state.setText(value)
        QtWidgets.QApplication.processEvents()
    def bat_8_sleep_state_handle(self, value):
        self.bat_8_sleep_state.setText(value)
        QtWidgets.QApplication.processEvents()

    def button_send_data_handle(self):
        url = ("http://charging.genmotorcycles.com/index.php?bat_id={:x}&volt={}&curr={}&soc={}&temp={}&capc={}&soh={}&cycle={}&doc=0&coc={}&sc={}&dot=0&dut=0&cot={}&cut={}&uv={}&ov={}&odc=0&imb=0&sf={}&cs={}&ds=0&ss={}").format(self.hole_1_msg_1, self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_charge_over_current.text(),self.bat_1_short_circuit.text(), self.bat_1_charge_over_temp.text(), self.bat_1_charge_under_temp.text(), self.bat_1_under_voltage.text(), self.bat_1_over_voltage.text(), self.bat_1_system_failure.text(), self.bat_1_charger_state.text(), self.bat_1_sleep_state.text())
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
        except:
            self.charging_status.setText("Hole 1 charging failed to stop")    

    def bat_2_button_start_handle(self):
        try:
            self.bat_2_button_start.setEnabled(False)
            self.bat_2_button_stop.setEnabled(True)
            self.loadData.pop(2)
            self.loadData.insert(2, 1)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData)
            self.bus.send(self.sendmsg)
            self.charging_status.setText("Hole 2 charging started")    
        except:
            self.charging_status.setText("Hole 2 charging starting failed")

    def bat_2_button_stop_handle(self):
        try:
            self.bat_2_button_stop.setEnabled(False)
            self.loadData.pop(2)
            self.loadData.insert(2,0)
            self.sendmsg = can.Message(arbitration_id=0x1C0, data = self.loadData)
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
            os.system("sudo ip link set {} up type can bitrate {}".format(CHANNEL, BITRATE))
            self.bus = can.interface.Bus(channel = CHANNEL, bustype = 'socketcan')
            self.status_connect.setText("Canbus initiating sucess")
            self.button_connect.setEnabled(False)
            self.button_disconnect.setEnabled(True)
            
            '''
            self.client = mqtt.Client()
            self.client.reinitialise(client_id="clientidmqtt", clean_session=True, userdata=None)
            self.client.on_connect = self.mqtt_connect
            self.client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
            '''
            
            while True:
                self.msg = self.bus.recv() 
                '''
                self.buff = {
                    "bat_1_voltage" : self.bat_1_voltage.text(),
                    "bat_1_current" : self.bat_1_current.text(),
                    "bat_1_soc" : self.bat_1_soc.text(),
                    "bat_1_temp" : self.bat_1_temp.text(),
                    "bat_1_capacity" : self.bat_1_capacity.text(),
                    "bat_1_soh" : self.bat_1_soh.text(),
                    "bat_1_cycle" : self.bat_1_cycle.text(),   
                    "bat_1_over_charge" : self.bat_1_batt_over_charge.text(),                 
                    "bat_1_charge_over_current" : self.bat_1_batt_over_current.text(),
                    "bat_1_short_circuit" : self.bat_1_batt_short_circuit.text(),
                    "bat_1_charge_over_temp" : self.bat_1_.text(),
                    "bat_1_charge_under_temp" : self.bat_1_charge_under_temp.text(),
                    "bat_1_under_voltage" : self.bat_1_under_voltage.text(),
                    "bat_1_over_voltage" : self.bat_1_over_voltage.text(),
                    "bat_1_system_failure" : self.bat_1_system_failure.text(),
                    "bat_1_charger_state" : self.bat_1_charger_state.text(),
                    "bat_1_sleep_state" : self.bat_1_sleep_state.text()
                }
                '''
                #self.client.subscribe(MQTT_TOPIC)
                
                ## THE ARBITRATION_ID MAY CHANGE WHEN TRYING ON REAL BMS
                if self.msg.arbitration_id == 0x0C1:

                    self.bat_1_button_start.setEnabled(True)
                    self.HOLE_1_ID.emit(int(frameparse(self.msg, "bat_id")))                    
                    self.FAULT_CODE_1.emit(frameparse(self.msg, "fault_code"))
                    self.HANDSHACKING_1.emit(int(frameparse(self.msg, "handshaking")))
                    
                    
                    #self.brokers_out = json.dumps(self.buff)
                    #self.client.publish(MQTT_TOPIC, self.brokers_out)
                    
                    #url = ("http://charging.genmotorcycles.com/index.php?bat_id={:x}&volt={}&curr={}&soc={}&temp={}&capc={}&soh={}&cycle={}&doc=0&coc={}&sc={}&dot=0&dut=0&cot={}&cut={}&uv={}&ov={}&odc=0&imb=0&sf={}&cs={}&ds=0&ss={}").format(self.hole_1_msg_1, self.bat_1_voltage.text(), self.bat_1_current.text(), self.bat_1_soc.text(), self.bat_1_temp.text(), self.bat_1_capacity.text(), self.bat_1_soh.text(), self.bat_1_cycle.text(), self.bat_1_charge_over_current.text(),self.bat_1_short_circuit.text(), self.bat_1_charge_over_temp.text(), self.bat_1_charge_under_temp.text(), self.bat_1_under_voltage.text(), self.bat_1_over_voltage.text(), self.bat_1_system_failure.text(), self.bat_1_charger_state.text(), self.bat_1_sleep_state.text())
                    #webUrl = urllib.request.urlopen(url)
                    #self.status_connect.setText(str(webUrl.getcode()))
                    #print("result code " + str(webUrl.getcode()))
                    
                if self.handshacking_1_status == 1:                    
                    self.charging_status.setText("Hole 1 Connection success")
                    #print("asdf")
                    if self.msg.arbitration_id == self.hole_1_msg_1:
                        self.BAT_1_VOLTAGE.emit(str(frameparse(self.msg, "bat_voltage")))
                        self.BAT_1_CURRENT.emit(str(frameparse(self.msg, "bat_current")))
                        self.BAT_1_SOC.emit(str(frameparse(self.msg, "bat_soc")))
                        self.BAT_1_TEMP.emit(str(frameparse(self.msg, "bat_temp")))
                        
                    if self.msg.arbitration_id == self.hole_1_msg_2:
                        self.BAT_1_CAPACITY.emit(str(frameparse(self.msg, "bat_capacity")))
                        self.BAT_1_SOH.emit(str(frameparse(self.msg, "bat_soh")))
                        self.BAT_1_CYCLE.emit(str(frameparse(self.msg, "bat_cycle")))
                        #self.BAT_1_CHARGE_OVER_CURRENT.emit(str(frameparse(self.msg, "status")[1]))
                        #self.BAT_1_SHORT_CIRCUIT.emit(str(frameparse(self.msg, "status")[2]))
                        #self.BAT_1_CHARGE_OVER_TEMP.emit(str(frameparse(self.msg, "status")[5]))
                        #self.BAT_1_CHARGE_UNDER_TEMP.emit(str(frameparse(self.msg, "status")[6]))
                        #self.BAT_1_UNDER_VOLTAGE.emit(str(frameparse(self.msg, "status")[7]))
                        #self.BAT_1_OVER_VOLTAGE.emit(str(frameparse(self.msg, "status")[8]))
                        #self.BAT_1_SYSTEM_FAILURE.emit(str(frameparse(self.msg, "status")[11]))
                        #self.BAT_1_CHARGE_STATE.emit(str(frameparse(self.msg, "status")[12]))                      
                        #self.BAT_1_SLEEP_STATE.emit(str(frameparse(self.msg, "status")[14]))   
                  
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
    V    1. ngirim data nang database
    V    2. struktur program awal baca sampek akhir
    3. develop multithread / timer
    V    4. ganti data string nang database battery id 
    '''