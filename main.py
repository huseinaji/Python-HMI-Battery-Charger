from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QLabel

import jajali
from PyQt5.QtCore import QTimer

class MainClass(QDialog, jajali.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
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
        self.voltage_1.setText(str(self.dial.value()))
        self.temp_1.setText(str(self.dial.value()))
        
    '''    
    def handleTimer(self):
        value = self.progressBar.value()
        if value < 100:
            value = value + 1
            self.progressBar.setValue(value)
        else:
            self.timer.stop()
	'''
if __name__ == "__main__":
    window = QApplication(sys.argv)
    ui = MainClass()
    ui.show()
    window.exec_()
