from dateTools import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import QIcon

def calculate():
    open("config.txt","a")
    if w.l1.text() == "" or int(w.l1.text())  < 0:
        QMessageBox.critical(w,"Error","Invalid hour input")
    else:
        beginDate = w.d1.date().toString("yyyy-M-d")
        option = w.c2.currentText()[0]
        hours = int(w.l1.text())
        if w.c1.isChecked():
            countd = True
        else:
            countd = False
        beginDate = dtool.dateToDict(beginDate)
        holdayList = extrholdays()
        w.l2.setText(dtool.dictToDate(dtool.calcEndDate(beginDate,hours,option,countd,holdayList)))

def extrholdays():
    F = open("config.txt","r")
    item = F.readline()
    T=[]
    while item != "":
        T.append(item[:-1])
        item = F.readline()
    F.close()
    return T

def settings():
    open("config.txt","a")
    loadconfig()
    s.show()

def loadconfig():
    s.lw.clear()
    F = open("config.txt","r")
    s.lw.addItem("CURRENT HOLIDAYS ==>")
    item = F.readline()
    while item != "":
        s.lw.addItem(item[:-1])
        item = F.readline()
    F.close()

def add():
    F = open("config.txt","r")
    test = True
    item = F.readline()
    while item != "":
        if item[:-1] == s.d1.date().toString("yyyy-M-d"):
            test = False
        item = F.readline()
    F.close()
    if test:
        F = open("config.txt","a")
        F.write(s.d1.date().toString("yyyy-M-d")+"\n")
        F.close()
    loadconfig()

def remove():
    F = open("config.txt","r")
    T = []
    j = 0
    item = F.readline()
    while item != "":
        if item[:-1] != s.d1.date().toString("yyyy-M-d"):
            T.append(item[:-1])
            j += 1
        item = F.readline()
    F.close()
    F = open("config.txt","w")
    for i in range(j):
        F.write(str(T[i])+"\n")
    F.close()
    loadconfig()
    
app=QApplication([])
w=loadUi("interface.ui")
s=loadUi("settings.ui")
# w.c1.setStyleSheet("QCheckBox::indicator { background-color: #253144; }")
icon = QIcon('gear.png')
w.b2.setIcon(icon)
w.b2.setStyleSheet("background:background-color:#253144;")
w.b2.setIconSize(icon.actualSize(w.b2.sizeHint())*0.75)
w.b1.clicked.connect(calculate)
w.b2.clicked.connect(settings)
s.b1.clicked.connect(add)
s.b2.clicked.connect(remove)
w.show()
app.exec()
