################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
from SugenoMandi import SugenoMandi
import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient,QIcon)
from PySide2.QtWidgets import *
from PyQt5 import QtGui
from PySide2.QtCore import Qt
#tableview

import numpy as np
import xlrd


## ==> SPLASH SCREEN
from ui_splash_screen import Ui_SplashScreen

## ==> MAIN WINDOW
from ui_main import Ui_MainWindow

## ==> GLOBALS
table = {}
counter = 0
classes = 0
counts = 1
filename = str()
disease_name = str()
disease_names = []
start_diap = 0
diapasons = []
module = []
modelValues = []


## MY APP
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.table = QtWidgets.QTableView()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setFixedSize(918, 471)
        
        #enable unusing widgets at the start of programm
        self.ui.trainButton.setEnabled(False)
        self.ui.saveButton.setEnabled(False)
        self.ui.diagButton.setEnabled(False)

        self.ui.numDiesases.setEnabled(False)
        self.ui.diseaseLine.setEnabled(False) 
        self.ui.diapLine1.setEnabled(False)      
        self.ui.diapLine2.setEnabled(False)     
        
        #connecting widgets to the functions
        self.ui.diagButton.clicked.connect(self.diagButton)
        self.ui.numDiesases.valueChanged.connect(self.counter)
        self.ui.btn_Browse.clicked.connect(self.pushButton)
        self.ui.saveButton.clicked.connect(self.saveButton)
        self.ui.trainButton.clicked.connect(self.trainButton)
        self.ui.diapLine1.setText(str(1))
        

    def pushButton(self):
        try:    
            fname = QFileDialog.getOpenFileName(self,'Открыть файл','/','XLS files only(*.xls)')
            self.ui.filename.setText(fname[0])
            self.ui.numDiesases.setEnabled(True)
        except:
            QtWidgets.QMessageBox.information(self, 'Выберите .xls формат', IOError)


    def diagButton(self):
        global module,filename,classes,disease_names,table,modelValues
        location_file = filename
        wb = xlrd.open_workbook(location_file)
        sheet = wb.sheet_by_index(1)

        row_number = sheet.nrows
        cols_number = sheet.ncols
        num_classes = classes
        n = row_number
        m = cols_number
        #getting the value of matrix to diagnose
        matrix_toDiag = np.zeros((n,m))
        for i in range(row_number):
            for j in range(cols_number):
                matrix_toDiag[i][j] = sheet.cell(i,j).value
        Betta = module['Bettas']
        B = module['B']
        U_1 = np.ones((n,1))
        X = np.concatenate((U_1,matrix_toDiag),axis=1)
        summa = 0
        Ys = []
        for r in range(n):
            for i in range(num_classes):
                for j in range(m+1):
                    summa = summa + Betta[r][i]*B[i][j]*X[r][j]
            Ys.append(summa)
            summa = 0
        values = [round(v) for v in Ys]

        #calculating the percentage of correctnes
        percentage = []

        for i in range(len(values)):
            percentage.append((1-(round(values[i])-values[i]))*100)
        #getting which one is ill,and which disease
        m = {}
        k = 1
        for i in disease_names:
            m[i] = k
            k+=1
        modelValues = values
        for i in m:
            for j in range(len(values)):
                if m[i] == values[j]:
                    modelValues[j] = i   
        #creating dictionary for table view
        table['Неболен'] = []
        for i in disease_names:
            table[i] = []
            for j in range(len(modelValues)):
                if i == modelValues[j]:
                    table[i].append(str(j+1))
                else:
                    table['Неболен'].append(str(j+1))
        self.main = TableView(table,len(modelValues),len(disease_names)+1)
        self.main.show()
                    
    def counter(self):
        global classes,diapasons,disease_names,counts,filename
        counts = 1
        classes = 0
        diapasons.clear()
        disease_names.clear()
        classes = int(self.ui.numDiesases.text())
        self.ui.diseaseLine.setEnabled(True)     
        self.ui.diapLine2.setEnabled(True)      
        self.ui.saveButton.setEnabled(True)
        filename = self.ui.filename.text()
    def saveButton(self):
        global disease_name,counts,diapasons
        if counts <= classes and ' ' not in self.ui.diapLine2.text() and self.ui.diapLine2.text() !='' and ' ' not in self.ui.diseaseLine.text() and self.ui.diseaseLine.text() !='' and int(self.ui.diapLine2.text())>int(self.ui.diapLine1.text()):
            counts += 1
            disease_names.append(self.ui.diseaseLine.text())
            diapasons.append(int(self.ui.diapLine2.text()))
            self.ui.diapLine1.setText(self.ui.diapLine2.text())
            self.ui.diapLine1.setEnabled(False)
            self.ui.diseaseLine.clear()
            self.ui.diapLine2.clear()
        else:
            centerPoint = QDesktopWidget().availableGeometry().center()
            msg = u""" Необходимо заполнить всю форму или заполнено с ошибкой"""
            about = QtWidgets.QMessageBox()
            about.setGeometry(450, 300,200,200)
            about.setIcon(QtWidgets.QMessageBox.Information)
            about.setText(u"Error")
            about.setInformativeText(msg)
            about.setWindowTitle(u"Error!")
            about.setStandardButtons(QtWidgets.QMessageBox.Ok)
            about.move(centerPoint)
            about.exec_()         
        if counts == classes + 1:
            counts -= 1
            self.ui.saveButton.setEnabled(False)
            self.ui.trainButton.setEnabled(True)
            self.ui.diseaseLine.setEnabled(False)
            self.ui.diapLine2.setEnabled(False)
        
        self.ui.diesaseLabel.setText('{0}'.format(counts))
        disease_name = self.ui.diseaseLine.text()
        self.ui.numDiesases.setEnabled(True)
    def trainButton(self):
        global filename,diapasons,classes,module
        datas = {}
        centerPoint = QDesktopWidget().availableGeometry().center()
        
        datas['file'] = filename
        datas['diapasons'] = diapasons
        datas['classes'] = classes
        #getting the values of the model
        readFile = SugenoMandi.Inputing(datas)
        module = SugenoMandi.calculating_Module(readFile)
        
        #notification about the model
        msg = """Модел создан"""
        about = QtWidgets.QMessageBox()
        about.setIcon(QtWidgets.QMessageBox.Information)
        about.setText(u"Обучение успешно")
        about.setInformativeText(msg)
        about.setWindowTitle(u"Информация обучения")
        about.setStandardButtons(QtWidgets.QMessageBox.Ok)
        about.move(centerPoint)
        about.exec_()  
        self.ui.trainButton.setEnabled(False)
        self.ui.diagButton.setEnabled(True)


# SPLASH SCREEN
class SplashScreen(QMainWindow):
    def __init__(self):
        try: 
            QMainWindow.__init__(self)
            self.ui = Ui_SplashScreen()
            self.ui.setupUi(self)
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)
            self.move(qtRectangle.topLeft())

            ## UI ==> INTERFACE CODES
            ########################################################################

            ## REMOVE TITLE BAR
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            ## DROP SHADOW EFFECT
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(20)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0,0,0,60))
            self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

            ## QTTIMER ==> START
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.progress)
            # TIMER IN  MILLISECONDS
            self.timer.start(35)

            #CHANGE DESCRIPTION
            
            #INITIAL TEXT
            self.ui.label_description.setText("<strong>")
            
            # Change Text
            QtCore.QTimer.singleShot(0,lambda:self.ui.label_description.setText("<strong>DIAGNOSTICS</strong> ACCORDING TO INDICATIONS"))
            QtCore.QTimer.singleShot(1500,lambda:self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
            QtCore.QTimer.singleShot(3000,lambda:self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))
            ## SHOW ==> MAIN WINDOW
            ########################################################################
            self.show()

            ## ==> END ##
        except IOError:
            QtWidgets.QMessageBox.information(self, 'Пожалуйста выберите .xls формат', IOError)

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):

        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH  SCREEN AND OPEN APP
        if counter>100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            #CLOSE SPLASH SCREEN
            self.close()
        #INCREASE COUNTER
        counter +=1

class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.height = 1000
        self.width = 500
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.move(centerPoint)
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())