# File : QT_thermostat_1.py
# Simulated thermostat using QTdesigner .ui file directly
# Qtdesigner file : QT_thermostat_1.ui
# info@pcamus.be
# 31/7/2022

import sys, random, time
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import * # non graphical elements as timer

# Derived class to add events management to raw main application window
class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = loadUi("QT_thermostat_1.ui", self)
              
        # timer 1 creation, link to handler and inititialization
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.handleTimer1)
        self.timer1.start(3000) # 3000 ms
        
        # timer 2 creation, link to handler and inititialization
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.handleTimer2)
        self.timer2.start(1000) # 1000 ms
        
        self.statusBar().showMessage(time.asctime(time.localtime()))
        
    # Temperature sampling timer handler
    def handleTimer1(self):
        temperature=random.randint(100, 400)/10
        self.ui.lcdNumber.display(str(temperature))
        consigne=self.ui.spinBox.value()
        if consigne > temperature :
            self.ui.lbl_state_val.setText("ON")
            self.ui.lbl_state_val.setStyleSheet("background-color: red")
        else :
            self.ui.lbl_state_val.setText("OFF")
            self.ui.lbl_state_val.setStyleSheet("background-color: cyan")
            
    # Date and time refresh timer handler
    def handleTimer2(self):
        self.statusBar().showMessage(time.asctime(time.localtime()))


app = QtWidgets.QApplication([]) # main application
mywindow().show()
sys.exit(app.exec())  
