import sys
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFrame, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QPainter
from PyQt5.QtWidgets import (QRadioButton, QWidget, QStylePainter, QSizePolicy,
                             QStyleOptionButton, QStyle, QButtonGroup, QApplication)
from PyQt5.QtCore import QRect, QSize, Qt

ROUTE_COLORS = {'2': 'red', '3': 'ForestGreen', '4': 'DodgerBlue', '7': 'DarkOrange',
                '12': 'blue', '15': 'DarkOrchid', '16': 'Lime', '67': 'DeepPink'}
ROUTE_WIDTH = 3


# Класс используется для рисования линий разного цвета
class RouteLine(QFrame):
    def __init__(self, *args, **kwargs):
        QFrame.__init__(self, *args, **kwargs)
        self.bustop = args[0].to_clear_stops
        self.line_color = "black"
        self.setLineWidth(3)
        self.setColor(QColor("line_color"))

    def setColor(self, color):
        palitr = self.palette()
        palitr.setColor(QPalette.WindowText, color)
        self.setPalette(palitr)

    def paintEvent(self, event):
        pnt = QPainter(self)
        pnt.setPen(QColor(self.line_color))
        pnt.setBrush(QColor(self.line_color))
        pnt.drawRect(0, 0, self.width(), self.height())
        pnt.end()


# Класс для рисования вертикальных RadioButton'ов
# RadioButton'ы используются в качестве остановок
class VerticalRadioButton(QRadioButton):
    def __init__(self, *args, **kwargs):
        QRadioButton.__init__(self, *args, **kwargs)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.setFixedWidth(2 * self.fontMetrics().height())
        self.bustop = args[0].to_clear_stops
        self.start_box = args[0].start_box
        self.finish_box = args[0].finish_box
        self.Bus_Stop = args[0].Bus_Stop
        self.transf_stops = args[0].transf_stops
        self.rbline = []

    def paintEvent(self, event):
        pnt_obj = QStylePainter(self)
        pnt_obj.rotate(270)
        pnt_obj.translate(-self.height(), 0)
        opt_btn = QStyleOptionButton()
        self.initStyleOption(opt_btn)
        size = opt_btn.rect.size()
        size.transpose()
        opt_btn.rect.setSize(size)
        start_name = self.start_box.currentText()
        finish_name = self.finish_box.currentText()
        self.setStyleSheet("QRadioButton"
                           "{"
                           "background-color : none"
                           "}")
        flag = False
        for i in range(len(self.bustop)):
            if self.bustop[i] == self:
                flag = True
        if flag is False:
            self.setChecked(False)  # защита от активации кнопки пользователем
        else:
            if self.Bus_Stop[start_name.strip()] == self or\
                    self.Bus_Stop[finish_name.strip()] == self:
                self.setStyleSheet("QRadioButton"
                               "{"
                               "background-color : lightgreen"
                               "}")
            for elem in self.transf_stops:
                if self.Bus_Stop[elem.strip()] == self:
                    self.setStyleSheet("QRadioButton"
                                       "{"
                                       "background-color : #fbec5d"
                                       "}")
        pnt_obj.drawControl(QStyle.CE_RadioButton, opt_btn)


# Класс для рисования горизонтальных RadioButton'ов
class HorizontalRadioButton(QRadioButton):
    def __init__(self, *args, **kwargs):
        QRadioButton.__init__(self, *args, **kwargs)

        self.bustop = args[0].to_clear_stops
        self.start_box = args[0].start_box
        self.finish_box = args[0].finish_box
        self.Bus_Stop = args[0].Bus_Stop
        self.transf_stops = args[0].transf_stops
        self.rbline = []

    def paintEvent(self, event):
        pnt_obj = QStylePainter(self)
        opt_btn = QStyleOptionButton()
        self.initStyleOption(opt_btn)
        size = opt_btn.rect.size()
        opt_btn.rect.setSize(size)
        start_name = self.start_box.currentText()
        finish_name = self.finish_box.currentText()
        self.setStyleSheet("QRadioButton"
                           "{"
                           "background-color : none"
                           "}")
        flag = False
        for i in range(len(self.bustop)):
            if self.bustop[i] == self:
                flag = True
        if flag is False:
            self.setChecked(False)  # защита от активации кнопки пользователем
        else:
            if self.Bus_Stop[start_name.strip()] == self or \
                    self.Bus_Stop[finish_name.strip()] == self:
                self.setStyleSheet("QRadioButton"
                                   "{"
                                   "background-color : lightgreen"
                                   "}")
            for elem in self.transf_stops:
                if self.Bus_Stop[elem.strip()] == self:
                    self.setStyleSheet("QRadioButton"
                                       "{"
                                       "background-color : #fbec5d"
                                       "}")
        pnt_obj.drawControl(QStyle.CE_RadioButton, opt_btn)


# Класс оформления формы с фотографией
class Ui_Pic_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 700)
        Form.setWindowTitle("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 781, 581))
        self.label.setText("")
        self.label.setObjectName("label")
        self.change_pic_button = QtWidgets.QPushButton(Form)
        self.change_pic_button.setGeometry(QtCore.QRect(310, 630, 221, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.change_pic_button.setFont(font)
        self.change_pic_button.setObjectName("change_pic_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.change_pic_button.setText(_translate("Form", "Загрузить свою картинку"))


# Класс формы с фотографией
class PictureForm(QWidget, Ui_Pic_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.change_pic_button.clicked.connect(self.change_picture)

    def change_picture(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '',
                                                'Картинка (*.jpg);;Картинка (*.jpeg);;'
                                                'Картинка (*.png);;Все файлы (*)')[0]
        if file_name != '':
            con = sqlite3.connect('troll_test.db')
            cur = con.cursor()
            command = f'''UPDATE images_buttons SET image = ? WHERE name = ?'''
            cur.execute(command, (file_name, self.windowTitle()))
            con.commit()
            con.close()
            self.update_picture()

    def update_picture(self):
        con = sqlite3.connect('troll_test.db')
        cur = con.cursor()
        command = '''SELECT image FROM images_buttons WHERE name = ?'''
        res = cur.execute(command, (self.windowTitle(),)).fetchall()
        self.pixmap = QPixmap(res[0][0])
        self.label.setPixmap(self.pixmap)
        self.update()


# Класс оформления основного окна
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(1240, 170, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.search_button.setFont(font)
        self.search_button.setObjectName("search_button")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1140, 110, 401, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_box = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.start_box.setFont(font)
        self.start_box.setObjectName("start_box")
        self.horizontalLayout.addWidget(self.start_box)
        self.finish_box = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.finish_box.setFont(font)
        self.finish_box.setObjectName("finish_box")
        self.horizontalLayout.addWidget(self.finish_box)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(30, 700, 30, 30))
        self.pushButton_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1.setIcon(icon)
        self.pushButton_1.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_1.setObjectName("pushButton_1")
        self.place_buttons = QtWidgets.QButtonGroup(MainWindow)
        self.place_buttons.setObjectName("place_buttons")
        self.place_buttons.addButton(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 700, 30, 30))
        self.pushButton_2.setText("")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.place_buttons.addButton(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 700, 30, 30))
        self.pushButton_3.setText("")
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.place_buttons.addButton(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(220, 700, 30, 30))
        self.pushButton_4.setText("")
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.place_buttons.addButton(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(320, 590, 30, 30))
        self.pushButton_5.setText("")
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_5.setObjectName("pushButton_5")
        self.place_buttons.addButton(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(390, 460, 30, 30))
        self.pushButton_6.setText("")
        self.pushButton_6.setIcon(icon)
        self.pushButton_6.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_6.setObjectName("pushButton_6")
        self.place_buttons.addButton(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(450, 460, 30, 30))
        self.pushButton_7.setText("")
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_7.setObjectName("pushButton_7")
        self.place_buttons.addButton(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(500, 460, 30, 30))
        self.pushButton_8.setText("")
        self.pushButton_8.setIcon(icon)
        self.pushButton_8.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_8.setObjectName("pushButton_8")
        self.place_buttons.addButton(self.pushButton_8)
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(580, 490, 30, 30))
        self.pushButton_9.setText("")
        self.pushButton_9.setIcon(icon)
        self.pushButton_9.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_9.setObjectName("pushButton_9")
        self.place_buttons.addButton(self.pushButton_9)
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(660, 470, 30, 30))
        self.pushButton_10.setText("")
        self.pushButton_10.setIcon(icon)
        self.pushButton_10.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_10.setObjectName("pushButton_10")
        self.place_buttons.addButton(self.pushButton_10)
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(710, 470, 30, 30))
        self.pushButton_11.setText("")
        self.pushButton_11.setIcon(icon)
        self.pushButton_11.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_11.setObjectName("pushButton_11")
        self.place_buttons.addButton(self.pushButton_11)
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(760, 470, 30, 30))
        self.pushButton_12.setText("")
        self.pushButton_12.setIcon(icon)
        self.pushButton_12.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_12.setObjectName("pushButton_12")
        self.place_buttons.addButton(self.pushButton_12)
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(820, 470, 30, 30))
        self.pushButton_13.setText("")
        self.pushButton_13.setIcon(icon)
        self.pushButton_13.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_13.setObjectName("pushButton_13")
        self.place_buttons.addButton(self.pushButton_13)
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setGeometry(QtCore.QRect(730, 270, 30, 30))
        self.pushButton_14.setText("")
        self.pushButton_14.setIcon(icon)
        self.pushButton_14.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_14.setObjectName("pushButton_14")
        self.place_buttons.addButton(self.pushButton_14)
        self.pushButton_15 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_15.setGeometry(QtCore.QRect(510, 300, 30, 30))
        self.pushButton_15.setText("")
        self.pushButton_15.setIcon(icon)
        self.pushButton_15.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_15.setObjectName("pushButton_15")
        self.place_buttons.addButton(self.pushButton_15)
        self.pushButton_16 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_16.setGeometry(QtCore.QRect(550, 300, 30, 30))
        self.pushButton_16.setText("")
        self.pushButton_16.setIcon(icon)
        self.pushButton_16.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_16.setObjectName("pushButton_16")
        self.place_buttons.addButton(self.pushButton_16)
        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_17.setGeometry(QtCore.QRect(470, 300, 30, 30))
        self.pushButton_17.setText("")
        self.pushButton_17.setIcon(icon)
        self.pushButton_17.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_17.setObjectName("pushButton_17")
        self.place_buttons.addButton(self.pushButton_17)
        self.pushButton_18 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_18.setGeometry(QtCore.QRect(350, 390, 30, 30))
        self.pushButton_18.setText("")
        self.pushButton_18.setIcon(icon)
        self.pushButton_18.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_18.setObjectName("pushButton_18")
        self.place_buttons.addButton(self.pushButton_18)
        self.pushButton_19 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_19.setGeometry(QtCore.QRect(190, 230, 30, 30))
        self.pushButton_19.setText("")
        self.pushButton_19.setIcon(icon)
        self.pushButton_19.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_19.setObjectName("pushButton_19")
        self.place_buttons.addButton(self.pushButton_19)
        self.pushButton_20 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_20.setGeometry(QtCore.QRect(240, 230, 30, 30))
        self.pushButton_20.setText("")
        self.pushButton_20.setIcon(icon)
        self.pushButton_20.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_20.setObjectName("pushButton_20")
        self.place_buttons.addButton(self.pushButton_20)
        self.pushButton_21 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_21.setGeometry(QtCore.QRect(280, 230, 30, 30))
        self.pushButton_21.setText("")
        self.pushButton_21.setIcon(icon)
        self.pushButton_21.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_21.setObjectName("pushButton_21")
        self.place_buttons.addButton(self.pushButton_21)
        self.pushButton_22 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_22.setGeometry(QtCore.QRect(330, 230, 30, 30))
        self.pushButton_22.setText("")
        self.pushButton_22.setIcon(icon)
        self.pushButton_22.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_22.setObjectName("pushButton_22")
        self.place_buttons.addButton(self.pushButton_22)
        self.pushButton_23 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_23.setGeometry(QtCore.QRect(280, 400, 30, 30))
        self.pushButton_23.setText("")
        self.pushButton_23.setIcon(icon)
        self.pushButton_23.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_23.setObjectName("pushButton_23")
        self.place_buttons.addButton(self.pushButton_23)
        self.pushButton_24 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_24.setGeometry(QtCore.QRect(150, 440, 30, 30))
        self.pushButton_24.setText("")
        self.pushButton_24.setIcon(icon)
        self.pushButton_24.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_24.setObjectName("pushButton_24")
        self.place_buttons.addButton(self.pushButton_24)
        self.pushButton_25 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_25.setGeometry(QtCore.QRect(150, 510, 30, 30))
        self.pushButton_25.setText("")
        self.pushButton_25.setIcon(icon)
        self.pushButton_25.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_25.setObjectName("pushButton_25")
        self.place_buttons.addButton(self.pushButton_25)
        self.pushButton_26 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_26.setGeometry(QtCore.QRect(100, 510, 30, 30))
        self.pushButton_26.setText("")
        self.pushButton_26.setIcon(icon)
        self.pushButton_26.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_26.setObjectName("pushButton_26")
        self.place_buttons.addButton(self.pushButton_26)
        self.pushButton_27 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_27.setGeometry(QtCore.QRect(50, 510, 30, 30))
        self.pushButton_27.setText("")
        self.pushButton_27.setIcon(icon)
        self.pushButton_27.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_27.setObjectName("pushButton_27")
        self.place_buttons.addButton(self.pushButton_27)
        self.pushButton_28 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_28.setGeometry(QtCore.QRect(10, 160, 30, 30))
        self.pushButton_28.setText("")
        self.pushButton_28.setIcon(icon)
        self.pushButton_28.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_28.setObjectName("pushButton_28")
        self.place_buttons.addButton(self.pushButton_28)
        self.pushButton_29 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_29.setGeometry(QtCore.QRect(10, 230, 30, 30))
        self.pushButton_29.setText("")
        self.pushButton_29.setIcon(icon)
        self.pushButton_29.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_29.setObjectName("pushButton_29")
        self.place_buttons.addButton(self.pushButton_29)
        self.pushButton_30 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_30.setGeometry(QtCore.QRect(10, 290, 30, 30))
        self.pushButton_30.setText("")
        self.pushButton_30.setIcon(icon)
        self.pushButton_30.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_30.setObjectName("pushButton_30")
        self.place_buttons.addButton(self.pushButton_30)
        self.pushButton_31 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_31.setGeometry(QtCore.QRect(10, 340, 30, 30))
        self.pushButton_31.setText("")
        self.pushButton_31.setIcon(icon)
        self.pushButton_31.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_31.setObjectName("pushButton_31")
        self.place_buttons.addButton(self.pushButton_31)
        self.pushButton_32 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_32.setGeometry(QtCore.QRect(370, 230, 30, 30))
        self.pushButton_32.setText("")
        self.pushButton_32.setIcon(icon)
        self.pushButton_32.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_32.setObjectName("pushButton_32")
        self.place_buttons.addButton(self.pushButton_32)
        self.pushButton_33 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_33.setGeometry(QtCore.QRect(410, 230, 30, 30))
        self.pushButton_33.setText("")
        self.pushButton_33.setIcon(icon)
        self.pushButton_33.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_33.setObjectName("pushButton_33")
        self.place_buttons.addButton(self.pushButton_33)
        self.pushButton_34 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_34.setGeometry(QtCore.QRect(410, 180, 30, 30))
        self.pushButton_34.setText("")
        self.pushButton_34.setIcon(icon)
        self.pushButton_34.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_34.setObjectName("pushButton_34")
        self.place_buttons.addButton(self.pushButton_34)
        self.pushButton_35 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_35.setGeometry(QtCore.QRect(410, 100, 30, 30))
        self.pushButton_35.setText("")
        self.pushButton_35.setIcon(icon)
        self.pushButton_35.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_35.setObjectName("pushButton_35")
        self.place_buttons.addButton(self.pushButton_35)
        self.pushButton_36 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_36.setGeometry(QtCore.QRect(760, 200, 30, 30))
        self.pushButton_36.setText("")
        self.pushButton_36.setIcon(icon)
        self.pushButton_36.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_36.setObjectName("pushButton_36")
        self.place_buttons.addButton(self.pushButton_36)
        self.pushButton_37 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_37.setGeometry(QtCore.QRect(760, 140, 30, 30))
        self.pushButton_37.setText("")
        self.pushButton_37.setIcon(icon)
        self.pushButton_37.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_37.setObjectName("pushButton_37")
        self.place_buttons.addButton(self.pushButton_37)
        self.pushButton_38 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_38.setGeometry(QtCore.QRect(760, 50, 30, 30))
        self.pushButton_38.setText("")
        self.pushButton_38.setIcon(icon)
        self.pushButton_38.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_38.setObjectName("pushButton_38")
        self.place_buttons.addButton(self.pushButton_38)
        self.pushButton_39 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_39.setGeometry(QtCore.QRect(820, 50, 30, 30))
        self.pushButton_39.setText("")
        self.pushButton_39.setIcon(icon)
        self.pushButton_39.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_39.setObjectName("pushButton_39")
        self.place_buttons.addButton(self.pushButton_39)
        self.pushButton_40 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_40.setGeometry(QtCore.QRect(860, 50, 30, 30))
        self.pushButton_40.setText("")
        self.pushButton_40.setIcon(icon)
        self.pushButton_40.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_40.setObjectName("pushButton_40")
        self.place_buttons.addButton(self.pushButton_40)
        self.pushButton_41 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_41.setGeometry(QtCore.QRect(930, 50, 30, 30))
        self.pushButton_41.setText("")
        self.pushButton_41.setIcon(icon)
        self.pushButton_41.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_41.setObjectName("pushButton_41")
        self.place_buttons.addButton(self.pushButton_41)
        self.pushButton_42 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_42.setGeometry(QtCore.QRect(1000, 50, 30, 30))
        self.pushButton_42.setText("")
        self.pushButton_42.setIcon(icon)
        self.pushButton_42.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_42.setObjectName("pushButton_42")
        self.place_buttons.addButton(self.pushButton_42)
        self.pushButton_43 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_43.setGeometry(QtCore.QRect(920, 290, 30, 30))
        self.pushButton_43.setText("")
        self.pushButton_43.setIcon(icon)
        self.pushButton_43.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_43.setObjectName("pushButton_43")
        self.place_buttons.addButton(self.pushButton_43)
        self.how_to_go_widget = QtWidgets.QListWidget(self.centralwidget)
        self.how_to_go_widget.setGeometry(QtCore.QRect(1170, 240, 401, 551))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.how_to_go_widget.setFont(font)
        self.how_to_go_widget.setObjectName("how_to_go_widget")
        self.hide_button = QtWidgets.QPushButton(self.centralwidget)
        self.hide_button.setGeometry(QtCore.QRect(30, 790, 261, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.hide_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/sleep.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hide_button.setIcon(icon1)
        self.hide_button.setIconSize(QtCore.QSize(25, 25))
        self.hide_button.setObjectName("hide_button")
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(1250, 810, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1300, 50, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1200, 80, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1410, 80, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.color_troll_widget = QtWidgets.QTextBrowser(self.centralwidget)
        self.color_troll_widget.setGeometry(QtCore.QRect(1100, 240, 71, 551))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        self.color_troll_widget.setFont(font)
        self.color_troll_widget.setObjectName("color_troll_widget")
        self.search_button.raise_()
        self.layoutWidget.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_7.raise_()
        self.pushButton_8.raise_()
        self.pushButton_9.raise_()
        self.pushButton_10.raise_()
        self.pushButton_11.raise_()
        self.pushButton_12.raise_()
        self.pushButton_13.raise_()
        self.pushButton_14.raise_()
        self.pushButton_15.raise_()
        self.pushButton_16.raise_()
        self.pushButton_17.raise_()
        self.pushButton_18.raise_()
        self.pushButton_19.raise_()
        self.pushButton_20.raise_()
        self.pushButton_21.raise_()
        self.pushButton_22.raise_()
        self.pushButton_23.raise_()
        self.pushButton_24.raise_()
        self.pushButton_25.raise_()
        self.pushButton_26.raise_()
        self.pushButton_27.raise_()
        self.pushButton_28.raise_()
        self.pushButton_29.raise_()
        self.pushButton_30.raise_()
        self.pushButton_31.raise_()
        self.pushButton_32.raise_()
        self.pushButton_33.raise_()
        self.pushButton_34.raise_()
        self.pushButton_35.raise_()
        self.pushButton_36.raise_()
        self.pushButton_37.raise_()
        self.pushButton_38.raise_()
        self.pushButton_39.raise_()
        self.pushButton_40.raise_()
        self.pushButton_41.raise_()
        self.pushButton_42.raise_()
        self.pushButton_43.raise_()
        self.how_to_go_widget.raise_()
        self.hide_button.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_1.raise_()
        self.save_button.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.color_troll_widget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Троллейбусный маршрут"))
        self.search_button.setText(_translate("MainWindow", "Построить маршрут"))
        self.hide_button.setText(_translate("MainWindow", "Фотографии г.Омска"))
        self.save_button.setText(_translate("MainWindow", "Сохранить маршрут"))
        self.label.setText(_translate("MainWindow", "Маршрут"))
        self.label_2.setText(_translate("MainWindow", "Начало"))
        self.label_3.setText(_translate("MainWindow", "Конец"))


# Класс основного окна приложения
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.search_button.clicked.connect(self.search)
        self.hide_button.clicked.connect(self.hide_and_seek)
        self.save_button.clicked.connect(self.save_personal_route)

        self.place_buttons_list = self.place_buttons.buttons()
        for btn in self.place_buttons_list:
            btn.clicked.connect(self.open_picture)
            btn.hide()
        self.hide_f = True

        self.Bus_Stop = {}
        self.to_clear_stops = []
        self.transf_stops = []
        self.troll_stops = []
        self.text = []
        self.text_dimension = True

        self.line_init()
        self.fill_stops_combobox()

    def open_picture(self):
        """Открытие формы с фотографией"""
        self.picture = PictureForm(self)
        button = self.picture.sender().objectName()
        con = sqlite3.connect('troll_test.db')
        cur = con.cursor()
        command = '''SELECT image, name FROM images_buttons WHERE button = ?'''
        res = cur.execute(command, (button,)).fetchall()
        image = res[0][0]
        if '/' in image:
            self.pixmap = QPixmap(image)
        else:
            self.pixmap = QPixmap(f'images/{image}')
        self.picture.label.setPixmap(self.pixmap)
        title = res[0][1]
        self.picture.setWindowTitle(title)
        self.picture.show()

    def save_personal_route(self):
        """Сохранение построенного для пользователя маршрута"""
        current_text = []
        if self.text_dimension is True:
            for i in range(len(self.text)):
                current_text.append(self.text[i] + '\n')
        else:
            for elem in self.text:
                for el in elem:
                    current_text.append(el + '\n')
        file_name = QFileDialog.getSaveFileName(self, 'Выбрать папку', '')[0]
        with open(f'{file_name}.txt', mode='wt', encoding='utf-8') as f:
            file = f.writelines(current_text)

    def fill_stops_combobox(self):
        """"Заполнение виджетов с названиями остановок из БД"""
        con = sqlite3.connect('troll_test.db')
        cur = con.cursor()
        command = '''SELECT name FROM troll_stops'''
        result = cur.execute(command).fetchall()
        for elem in result:
            self.troll_stops.append(elem[0])
        self.troll_stops.sort()
        self.start_box.addItems(self.troll_stops)
        self.finish_box.addItems(self.troll_stops)

    def fill_troll_colors(self, nums):
        """Показывает номер маршрута его цветом"""
        out_list = []
        nums = [str(num) for num in nums]
        for num in nums:
            HTML = f"<font color='{ROUTE_COLORS[num]}' size = 15 >{num}</font>"
            out_list.append(HTML)
        self.color_troll_widget.setHtml('<br>'.join(out_list))

    def search(self):
        """
        Поиск маршрута от остановки А до остановки В
        с прямыми маршрутами и пересадками (функция transfer)
        """
        self.how_to_go_widget.clear()  # очистка предыдущего маршрута
        while len(self.to_clear_stops) > 0:
            self.to_clear_stops[0].setChecked(False)  # остановки предыдущих маршрутов убираются
            for elem in self.to_clear_stops[0].rbline:  # убираются линии предыдущих маршрутов
                elem.line_color = 'black'
            self.to_clear_stops.pop(0)
        while len(self.transf_stops) > 0:
            self.transf_stops.pop(0)
        start = self.start_box.currentText()
        finish = self.finish_box.currentText()
        nums = []
        con = sqlite3.connect('troll_test.db')
        cur = con.cursor()
        command = f'''SELECT troll_nums FROM troll_stops WHERE name = ?'''
        result = cur.execute(command, (start,)).fetchall()  # из БД запрашиваются номера троллейбусов
        if result[0][0].__class__ is str:
            nums = result[0][0].split(';')
        else:
            nums = [result[0][0]]
        true_nums = []
        f = False
        for num in nums:
            stops = []
            con = sqlite3.connect('troll_test.db')
            cur = con.cursor()
            command = f'''SELECT * FROM troll_{num}'''
            result = cur.execute(command).fetchall()  # из БД запрашиваются остановки троллейбусов
            for elem in result:
                stops.append(elem[1])
            if finish in stops:
                true_nums.append(num)
                f = True  # найден прямой маршрут
        if f is False:
            self.transfer(start, finish)  # поиск пересадок
        else:
            if start == finish:
                self.color_troll_widget.setText('')
                self.how_to_go_widget.addItem('Вы уже на месте!')
            else:
                self.set_on_selected_route(str(true_nums[0]), start, finish)  # построение прямого маршрута
                self.text = [f'Троллейбус {", ".join([str(x) for x in true_nums])}',
                             f'{start} - {finish}', '👍🚎']
                self.how_to_go_widget.addItems(self.text)
                self.text_dimension = True
                self.fill_troll_colors(true_nums)
        self.update()

    def transfer(self, start, finish):
        """Поиск маршрутов с пересадкой"""
        coinc_f = False
        trans_result = []
        num_lst = []
        trans_place = ''
        true_num_f = ''
        true_num_s = ''
        con = sqlite3.connect('troll_test.db')
        cur = con.cursor()
        command = '''SELECT troll_nums FROM troll_stops WHERE name = ?'''
        result = cur.execute(command, (start, )).fetchall()  # из БД запрашиваются номера троллейбусов
        if result[0][0].__class__ == str:
            start_nums = result[0][0].split(';')
        else:
            start_nums = [result[0][0]]
        command = '''SELECT troll_nums FROM troll_stops WHERE name = ?'''
        result = cur.execute(command, (finish, )).fetchall()  # из БД запрашиваются остановки троллейбусов
        if result[0][0].__class__ == str:
            finish_nums = result[0][0].split(';')
        else:
            finish_nums = [result[0][0]]
        for num_s in start_nums:  # перебор всех маршрутов с остановкой А
            start_stops = []
            for num_f in finish_nums:  # перебор всех маршрутов с остановкой В
                finish_stops = []
                res = cur.execute(f'''SELECT stop_name FROM troll_{num_s}''').fetchall()
                for elem in res:
                    start_stops.append(elem[0])
                res = cur.execute(f'''SELECT stop_name FROM troll_{num_f}''').fetchall()
                for elem in res:
                    finish_stops.append(elem[0])
                if len(set(start_stops) & set(finish_stops)) > 0:
                    coincidence = list(set(start_stops) & set(finish_stops))  # поиск совпадений остановок
                    true_num_s = num_s
                    true_num_f = num_f
                    coinc_f = True
                    ind = start_stops.index(start)
                    while ind < len(start_stops):  # поиск ближайшей остановки для пересадки
                        if start_stops[ind] in coincidence:
                            trans_place = start_stops[ind]
                            break
                        ind += 1
                    ind = start_stops.index(start)
                    while ind > 0:
                        if start_stops[ind] in coincidence:
                            trans_place = start_stops[ind]
                            break
                        ind -= 1
                    # строим найденный маршрут от А до пересадки
                    self.set_on_selected_route(str(true_num_s), start, trans_place)
                    # строим найденный маршрут от пересадки до В
                    self.set_on_selected_route(str(true_num_f), trans_place, finish)
                    trans_result.append([f'Остановка {start}',
                                        f'Троллейбус {true_num_s}',
                                        f'Пересадка на остановке {trans_place}',
                                        f'Троллейбус {true_num_f}',
                                        f'Остановка {finish}', ''])
                    num_lst.append(true_num_f)
                    num_lst.append(true_num_s)
                    self.transf_stops.append(trans_place)
        if coinc_f is False:
            self.text = ['Увы, пересадок больше одной, поэтому\n'
                                          'воспользуйтесь другим видом транспорта...', '🚎🚫😭']
            self.color_troll_widget.setText('')
            self.text_dimension = True
            self.how_to_go_widget.addItems(self.text)
        else:  # вывод текстового пояснения результата поиска
            i = 1
            self.text = []
            for elem in trans_result:
                self.text.append(elem)
                self.how_to_go_widget.addItem(f'{i})')
                self.how_to_go_widget.addItems(elem)
                i += 1
            self.how_to_go_widget.addItem('👍🚎')
            self.text_dimension = False
            if len(self.text) == 1:
                num_lst = [true_num_s, true_num_f]
            else:
                num_lst = sorted(list(set(num_lst)), key=lambda x: int(x))
            self.fill_troll_colors(num_lst)

    def hide_and_seek(self):
        """Эта функция прячет/показывает метки для фотографий"""
        if self.hide_f:
            for btn in self.place_buttons_list:
                btn.show()
            self.hide_button.setIcon(QIcon('images/look.png'))
            self.hide_f = False
        else:
            for btn in self.place_buttons_list:
                btn.hide()
            self.hide_button.setIcon(QIcon('images/sleep.png'))
            self.hide_f = True

    def create_rbline(self, pos_x, pos_y, max_str_len, line_len, vrb, rtl, route_w):
        """Создание линии маршрута"""
        rbline = RouteLine(self)
        if vrb is True:
            rbline.setFrameShape(QFrame.HLine)
            if rtl is True:
                rbline.setGeometry(QRect(pos_x - line_len + 6, pos_y + 4, line_len, route_w))
            else:
                rbline.setGeometry(QRect(pos_x - line_len + 6, pos_y
                                         + self.fontMetrics().width(max_str_len) - 8, line_len, route_w))
        else:
            rbline.setFrameShape(QFrame.VLine)
            if rtl is True:
                rbline.setGeometry(
                    QRect(pos_x + self.fontMetrics().width(max_str_len) - 9, pos_y - line_len + 8, route_w, line_len))
            else:
                rbline.setGeometry(QRect(pos_x + 4, pos_y - line_len + 8, route_w, line_len))
        return rbline

    def add_bus_stop(self, pos_x, pos_y, street_name, step, vrb, rtl, rvs, startline, stopline):
        """
        Добавление остановки и связанных с ней линий
        на схему троллейбусного маршрута. Объект линия создается совместно
        с горизонтальным или вертикальным RadioButton'ом (остановка).
        Информация об объекте линия запоминается в классе RadioButton'а
        для дальнейшей совместной работы с ним.
        """
        step_x = 0
        step_y = 0
        route_w = ROUTE_WIDTH
        street = []
        if step == 0:
            street.append(street_name)
        else:
            con = sqlite3.connect('troll_test.db')
            cur = con.cursor()
            command = '''SELECT name FROM troll_stops WHERE street_id IN (SELECT id FROM streets WHERE name = ?)'''
            res = cur.execute(command, (street_name,))  # выбираем название остановки из БД
            for elem in res:
                street.append(elem[0])
            if rvs:
                street.reverse()
        max_name = sorted(street, key=lambda x: len(x))
        max_str_len = max_name[-1]
        max_str_len += '          '
        if startline != 0:  # создаем линию первой остановки (если необходимо)
            rbline_s = self.create_rbline(pos_x, pos_y, max_str_len, startline, vrb, rtl, route_w)
        for i in range(len(street)):  # создаем остановки, расположенные на одной улице
            rbline = RouteLine(self)
            if vrb is True:  # создаем вертикальную RadioButton
                but = VerticalRadioButton(self)
                rbline.setFrameShape(QFrame.HLine)
                step_x = i * step
            else:  # создаем горизонтальную RadioButton
                but = HorizontalRadioButton(self)
                rbline.setFrameShape(QFrame.VLine)
                step_y = i * step
            if rtl is True:  # выравнивание текста справа налево
                but.setLayoutDirection(Qt.RightToLeft)
            else:  # выравнивание текста слева направо
                but.setLayoutDirection(Qt.LeftToRight)
            but.setText(street[i])
            but.move(pos_x + step_x, pos_y + step_y)

            if vrb is True:  # Рисование вертикальной линии маршрута
                if rtl is True:
                    rbline.setGeometry(QRect(pos_x + step_x + 16, pos_y + 4, int(step/2), route_w))
                else:
                    rbline.setGeometry(QRect(pos_x + step_x + 16,
                                             pos_y + self.fontMetrics().width(max_str_len) - 8, int(step / 2), route_w))
                but.resize(self.fontMetrics().height() * 2, self.fontMetrics().width(max_str_len))
            else:  # Рисование горизонтальной линии маршрута
                if rtl is True:
                    rbline.setGeometry(QRect(pos_x + self.fontMetrics().width(max_str_len) - 9, pos_y + step_y + 15, route_w, step))
                else:
                    rbline.setGeometry(QRect(pos_x + 4, pos_y + step_y + 15, route_w, step))
                but.resize(self.fontMetrics().width(max_str_len), self.fontMetrics().height() * 2)
            btn_group = QButtonGroup(self)
            btn_group.setObjectName(f"buttonGroup{i}")
            btn_group.addButton(but)
            btn_group.setExclusive(False)
            if i == 0 and startline != 0:
                but.rbline.append(rbline_s)  # Добавление объекта линии к остановке
            but.rbline.append(rbline)  # Добавление объекта линии к остановке
            self.Bus_Stop[street[i].strip()] = but  # сохранение созданной остановки в словаре остановок
        if stopline != 0:  # создаем линию конечной остановки (если необходимо)
            if vrb is True:
                if rtl is True:
                    rbline.setGeometry(QRect(pos_x + step_x + 16, pos_y + 4, stopline, route_w))
                else:
                    rbline.setGeometry(QRect(pos_x + step_x + 16,
                                             pos_y + self.fontMetrics().width(max_str_len) - 8, stopline, route_w))
            else:
                if rtl is True:
                    rbline.setGeometry(QRect(pos_x + self.fontMetrics().width(max_str_len) - 9, pos_y + step_y + 15, route_w, stopline))
                else:
                    rbline.setGeometry(QRect(pos_x + 4, pos_y + (len(street) - 1) * step + 15, route_w, stopline))
        else:
            but.rbline.pop()
            if vrb is True:
                rbline.setGeometry(QRect(pos_x + step_x + 16, pos_y + 4, 0, 0))
            else:
                rbline.setGeometry(QRect(pos_x + 4, pos_y + step_y + 15, 0, 0))

    def set_on_selected_route(self, tnum, stop_1, stop_2):
        """Выводит построенный маршрут на схеме"""
        bus_stop_name = []
        color = ROUTE_COLORS[tnum]
        con = sqlite3.connect('troll_test.db')
        cur = con.cursor()
        command = f'''SELECT stop_name FROM troll_{tnum}'''
        result = cur.execute(command).fetchall()  # Извлекаем из БД остановки выбранного маршрута
        for elem in result:
            bus_stop_name.append(elem[0])
        con.close()
        i = 0
        while (i < len(bus_stop_name)) and bus_stop_name[i].strip() != stop_1\
                and bus_stop_name[i].strip() != stop_2:
            i += 1
        if i < len(bus_stop_name):
            self.to_clear_stops.append(self.Bus_Stop[bus_stop_name[i].strip()])
            self.Bus_Stop[bus_stop_name[i].strip()].setChecked(True)  # активна остановка А
            # убирает лишние линии начала маршрута
            for elem in self.Bus_Stop[bus_stop_name[i].strip()].rbline:
                pos_line = elem.pos()
                pos_1 = self.Bus_Stop[bus_stop_name[i].strip()].pos()
                pos_2 = self.Bus_Stop[bus_stop_name[i + 1].strip()].pos()
                if pos_1.x() < pos_line.x() - 4 and pos_2.x() > pos_line.x() or\
                        pos_2.x() < pos_line.x() - 4 and pos_1.x() > pos_line.x():
                    elem.line_color = color
                if pos_1.y() < pos_line.y() - 4 and pos_2.y() > pos_line.y() or\
                        pos_2.y() < pos_line.y() - 4 and pos_1.y() > pos_line.y():
                    elem.line_color = color
            i += 1
        # Делает активными RadioButton'ы выбранного маршрута
        # Подсветка линий выбранного маршрута
        while (i < len(bus_stop_name)) and bus_stop_name[i].strip() != stop_1 \
                and bus_stop_name[i].strip() != stop_2:
            self.to_clear_stops.append(self.Bus_Stop[bus_stop_name[i].strip()])
            self.Bus_Stop[bus_stop_name[i].strip()].setChecked(True)  # активна остановка В
            for elem in self.Bus_Stop[bus_stop_name[i].strip()].rbline:
                elem.line_color = color
            i += 1
        # убирает лишние линии завершения маршрута
        if i < len(bus_stop_name):
            self.to_clear_stops.append(self.Bus_Stop[bus_stop_name[i].strip()])
            self.Bus_Stop[bus_stop_name[i].strip()].setChecked(True)
            for elem in self.Bus_Stop[bus_stop_name[i].strip()].rbline:
                pos_line = elem.pos()
                pos_1 = self.Bus_Stop[bus_stop_name[i].strip()].pos()
                pos_2 = self.Bus_Stop[bus_stop_name[i - 1].strip()].pos()
                if pos_1.x() < pos_line.x() - 4 and pos_2.x() > pos_line.x() or\
                        pos_2.x() < pos_line.x() - 4 and pos_1.x() > pos_line.x():
                    elem.line_color = color
                if pos_1.y() < pos_line.y() - 4 and pos_2.y() > pos_line.y() or\
                        pos_2.y() < pos_line.y() - 4 and pos_1.y() > pos_line.y():
                    elem.line_color = color

    def line_init(self):
        """Создание улиц, по которым проложены троллейбусные маршруты"""
        self.add_bus_stop(20, 587, 'Dianova_st', 20, True, True, True, 0, 12)
        self.add_bus_stop(180, 400, 'Lukashevicha_st', 30, False, False, True, 28, 28)
        self.add_bus_stop(210, 587, 'Vatutina_st', 20, True, True, False, 28, 50)
        self.add_bus_stop(290, 540, 'Pereleta_st', 20, False, False, True, 14, 19)
        self.add_bus_stop(300, 430, 'Komarova_av', 20, True, False, False, 11, 21)

        rbline = RouteLine(self)  # дополнительная линия маршрута
        rbline.setFrameShape(QFrame.VLine)
        rbline.setGeometry(QRect(374, 500, ROUTE_WIDTH, 36))
        self.Bus_Stop['ЖК Кристалл'].rbline.append(rbline)

        self.add_bus_stop(390, 493, 'October_70_years', 20, True, True, False, 22, 10)
        self.add_bus_stop(60, 373, 'Mira_av', 20, True, True, True, 17, 31)
        self.add_bus_stop(45, 150, 'Neftezavodskaya_st', 25, False, False, True, 0, 15)
        self.add_bus_stop(465, 333, 'Marksa_av_left', 20, True, True, False, 12, 36)
        self.add_bus_stop(454, 90, 'October_10_years', 20, False, False, True, 0, 55)
        self.add_bus_stop(585, 280, 'Mayakovskogo_st', 20, False, False, True, 36, 22)
        self.add_bus_stop(650, 333, 'Marksa_av_right', 20, True, True, False, 100, 0)
        self.add_bus_stop(194, 257, 'Krasniy_put', 20, True, False, False, 14, 10)

        rbline = RouteLine(self)  # дополнительная линия маршрута
        rbline.setFrameShape(QFrame.VLine)
        rbline.setGeometry(QRect(357, 339, ROUTE_WIDTH, 40))
        self.Bus_Stop['КДЦ Маяковский'].rbline.append(rbline)

        self.add_bus_stop(370, 251, 'Gagarina_st', 20, True, False, False, 19, 33)
        self.add_bus_stop(685, 245, 'Hmelnitskogo_st', 20, True, True, False, 102, 30)
        self.add_bus_stop(600, 60, 'Kosmicheskiy_av', 20, False, True, True, 0, 16)
        self.add_bus_stop(800, 122, 'Kirova_st', 20, True, False, False, 56, 10)
        self.add_bus_stop(960, 275, 'Gasheka_st', 20, False, True, False, 34, 0)
        self.add_bus_stop(550, 460, 'Парк Победы', 0, False, False, False, 0, 25)
        self.add_bus_stop(550, 432, 'ДОСААФ', 0, False, False, False, 0, 20)
        self.add_bus_stop(550, 370, 'м-н Жемчужина', 0, False, False, False, 40, 54)

stylesheet = """
MyWindow {
            background-image: url("images/background.jpg");
            background-repeat: no-repeat;
            background-position: center;
            }"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    w = MyWindow()
    w.setMinimumSize(QSize(0, 400))
    w.show()
    sys.exit(app.exec_())
