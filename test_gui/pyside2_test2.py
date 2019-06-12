import sys
import time

import numpy as np

#from mainwindow import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets
#from PySide2.QtWidgets import QMainWindow, QApplication
#from PySide2.QtWidgets.QApplication import *
#from PySide2.QtGui import QFont    
#from PySide2 import QtCore, QtGui, QtWidgets
#from PySide2.QtWidgets import QToolTip, QPushButton, QApplication, QMainWindow
from PySide2.QtWidgets import *
#

#class Example(QMainWindow):
#
#    def __init__(self, parent = None):
#        super().__init__()
#
#        self.initUI()
#
#
#    def initUI(self):
#
#        # 10pxのサンセリフフォントを吹き出しに使う
#        QToolTip.setFont(QFont('SansSerif', 10))
#
#        # 画面の吹き出し設定
#        self.setToolTip('This is a <b>QWidget</b> widget')
#
#        # ボタン作り
#        btn = QPushButton('Button', self)
#        # ボタンの吹き出し設定
#        btn.setToolTip('This is a <b>QPushButton</b> widget')
#        # ボタンのサイズをいい感じに自動設定
#        btn.resize(btn.sizeHint())
#        # ボタンの位置設定
#        btn.move(50, 50)       
#
#        self.setGeometry(300, 300, 300, 200)
#        self.setWindowTitle('Tooltips')    
#        self.show()
#        
#class Example(object):
#    def setupUi(self, MainWindow):
#        MainWindow.setObjectName("MainWindow")
#        MainWindow.resize(400, 300)
#        self.menuBar = QtWidgets.QMenuBar(MainWindow)
#        self.menuBar.setObjectName("menuBar")
#        MainWindow.setMenuBar(self.menuBar)
#        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
#        self.mainToolBar.setObjectName("mainToolBar")
#        MainWindow.addToolBar(self.mainToolBar)
#        self.centralWidget = QtWidgets.QWidget(MainWindow)
#        self.centralWidget.setObjectName("centralWidget")
#        MainWindow.setCentralWidget(self.centralWidget)
#        self.statusBar = QtWidgets.QStatusBar(MainWindow)
#        self.statusBar.setObjectName("statusBar")
#        MainWindow.setStatusBar(self.statusBar)
#
#        self.retranslateUi(MainWindow)
#        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#    def retranslateUi(self, MainWindow):
#        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
#
#class MainWindow(QMainWindow):
#    #Ui_MainWindow生成のための初期化処理
#    def __init__(self, parent = None):
#
#        #UI初期化処理
#        super(MainWindow, self).__init__()
#        self.ui = Example()
#        self.ui.setupUi(self)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(self.mainToolBar)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
    

class MainWindow(QMainWindow):
    #Ui_MainWindow生成のための初期化処理
    def __init__(self, parent = None):

        #Initialization of UI
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):

        #メッセージ画面の設定いろいろ
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        

#実行処理
if __name__=="__main__":
    #アプリケーション作成
    app = QApplication(sys.argv)
    
    #オブジェクト作成
    window = MainWindow()
    
    #MainWindowの表示
    window.show()
    
    #MainWindowの実行
    app.exec_()
    
    
    
'''
import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
'''
#    sys.exit(app.exec_())
    

#from PySide2 import QtWidgets

#class MainWindow(QtWidgets.QMainWindow):
#    def __init__(self, parent=None):
#        super(MainWindow, self).__init__(parent)
#        self.construct_ui()
#
#    def construct_ui(self):
#        self.setStyleSheet(hou.qt.styleSheet())
#        self.setProperty("houdiniStyle", True)
#        self.setWindowTitle('PySide2 Test')
#        # main widget
#        main_widget = QtWidgets.QWidget(self)
#        self.setCentralWidget(main_widget)
#        # layout initialize
#        g_layout = QtWidgets.QVBoxLayout()
#        layout = QtWidgets.QFormLayout()
#        main_widget.setLayout(g_layout)
#        # Add Widgets
#        self.parm = QtWidgets.QSpinBox()
#        self.parm.setValue(30)
#        layout.addRow('Parameter', self.parm)
#        self.exec_btn = QtWidgets.QPushButton('Execute')
#        # global layout setting
#        g_layout.addLayout(layout)
#        g_layout.addWidget(self.exec_btn)
