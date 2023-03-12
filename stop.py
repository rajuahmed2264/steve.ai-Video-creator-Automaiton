import json
import time

import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
from os import path
ui, _ = loadUiType(path.join(path.dirname(__file__), "stop.ui"))
global datatoprinttext, datatoprintpercent
datatoprinttext= "Starting"
datatoprintpercent = 1
runprogram = True
def getpidfromtext():
    global pidfromtext, pidfromtext2, mainpidfromtext

    with open("processtemp.file", "r") as file:
        pidfromtext = file.readlines()[0]

    with open("temppid.file", "r") as file2:
        pidfromtext2 = file2.readlines()[0]

def quiteappwithpid():
    global pidfromtext, pidfromtext2, mainpidfromtext
    getpidfromtext()
    temppidfile = open("processtemp.file", "r+")
    temppidfile.seek(0)
    temppidfile.truncate()
    process2 = psutil.Process(int(pidfromtext2))
    for child in process2.children(recursive=True):  # or parent.children() for recursive=False
        child.kill()
    process2.terminate()
    temppidfile = open("temppid.file", "r+")
    temppidfile.seek(0)
    temppidfile.truncate()
    process1 = psutil.Process(int(pidfromtext))
    for child in process1.children(recursive=True):  # or parent.children() for recursive=False
        child.kill()
    process1.terminate()

def loaddatafromjson():
    global datatoprinttext, datatoprintpercent
    f = open("otptdt.dt")
    raju = f.readlines()[0]
    raju=str(raju)
    raju = raju[0]
    if raju=="{":
        f = open("otptdt.dt")
        data = json.load(f)
        data = data.get("data")
        datatoprinttext = data.get("outputtext")
        datatoprintpercent = data.get("numbertooutput")


class MainApp(QMainWindow, ui):
    global datatoprinttext, datatoprintpercent
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.stopbutton.clicked.connect(self.stopbuttoncliick)
        self.qTimer = QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(500)  # 1000 ms = 1 s
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getSensorValue)
        # start timer
        self.qTimer.start()
    def stopbuttoncliick(self):
        quiteappwithpid()
        sys.exit()

    def getSensorValue(self):
        self.printoutput()

    def printoutput(self):
        global datatoprinttext, datatoprintpercent
        loaddatafromjson()

        self.outputtxt.setText(datatoprinttext)
        self.progressBar.setValue(int(datatoprintpercent))
        time.sleep(.5)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.aboutToQuit.connect(quiteappwithpid)
    app.exec_()

if __name__ == '__main__':
    main()