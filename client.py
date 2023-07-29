
from PySide6.QtWidgets import (QApplication, QLineEdit, QPlainTextEdit, QPushButton,
                               QScrollArea, QSizePolicy, QTextBrowser, QWidget, QLabel)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QIntValidator)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)

import sys
import socket
import threading
import ctypes


# ---------------------------------------------------------------Connect Form---------------------------------------------------------------


class Form(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")

        Widget.resize(422, 325)

        self.port_input = QLineEdit(Widget)
        self.port_input.setObjectName(u"port_input")
        self.port_input.setGeometry(QRect(150, 140, 161, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.port_input.sizePolicy().hasHeightForWidth())
        self.port_input.setSizePolicy(sizePolicy)
        self.port_input.setStyleSheet(u"text-align: center; \n"
                                      "vertical-align: center;")

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.port_input.setFont(font)

        self.host_input = QLineEdit(Widget)
        self.host_input.setObjectName(u"host_input")
        self.host_input.setGeometry(QRect(150, 50, 241, 51))
        sizePolicy.setHeightForWidth(
            self.host_input.sizePolicy().hasHeightForWidth())
        self.host_input.setSizePolicy(sizePolicy)
        self.host_input.setFont(font)
        self.host_input.setStyleSheet(u"text-align: center; \n"
                                      "vertical-align: center;")

        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 60, 111, 31))

        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)

        self.label.setFont(font1)
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 150, 81, 31))

        font2 = QFont()
        font2.setPointSize(18)
        font2.setBold(True)
        self.label_2.setFont(font2)

        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 250, 141, 41))
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setStyleSheet(u"text-align: center; \n"
                                      "vertical-align: center;")
        self.pushButton.setFont(font)
        self.pushButton.setText(
            QCoreApplication.translate("Widget", u"Connect", None))

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(
            QCoreApplication.translate("Widget", u"Connect to server", None))
        self.host_input.setText("")
        self.label.setText(QCoreApplication.translate("Widget", u"HOST", None))
        self.label_2.setText(
            QCoreApplication.translate("Widget", u"PORT", None))


class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Form()
        self.ui.setupUi(self)
        self.ui.host_input.setFocus()

        # set criteria for input area
        self.ui.pushButton.setEnabled(0)
        self.ui.pushButton.clicked.connect(self.connect)

        self.ui.host_input.textChanged.connect(lambda:  self.ui.pushButton.setEnabled(
            self.ui.host_input.text() != "" and self.ui.port_input.text() != ""))
        self.ui.host_input.returnPressed.connect(
            lambda: self.ui.port_input.setFocus())
        self.ui.host_input.setAlignment(Qt.AlignCenter)

        self.ui.port_input.textChanged.connect(lambda: self.ui.pushButton.setEnabled(
            self.ui.host_input.text() != "" and self.ui.port_input.text() != ""))
        self.ui.port_input.setValidator(QIntValidator(0, 65535))
        self.ui.port_input.returnPressed.connect(
            lambda: self.ui.pushButton.click() if self.ui.pushButton.isEnabled() else None)
        self.ui.port_input.setAlignment(Qt.AlignCenter)

        self.ui.host_input.setTabOrder(self.ui.host_input, self.ui.port_input)
        self.ui.port_input.setTabOrder(self.ui.port_input, self.ui.pushButton)
        # restrict resizing windows
        self.setFixedSize(self.size())

    def connect(self):
        try:
            client.connect((self.ui.host_input.text(),
                           int(self.ui.port_input.text())))
            print("Connected successfully")
            self.close()
        except:
            ctypes.windll.user32.MessageBoxW(
                0, "Cannot connect to the server", "Error", 0)


# ----------------------------------------------------------Graphic User Interface----------------------------------------------------------


class Ui_Widget(object):
    component = []

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.plainTextEdit = QPlainTextEdit(Widget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 530, 650, 50))
        Ui_Widget.component.append(self.plainTextEdit)

        self.textBrowser = QTextBrowser(Widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 650, 500))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        self.textBrowser.setFont(font)
        self.textBrowser.setStyleSheet(
            u"border: 1px solid gray; text-indent: 10px; line-height: 1.2;")
        Ui_Widget.component.append(self.textBrowser)

        self.scrollArea = QScrollArea(Widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(670, 10, 120, 500))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(
            u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 120, 500))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        Ui_Widget.component.append(self.scrollArea)

        # LIST OF USERS
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(
            u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 120, 500))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        Ui_Widget.component.append(self.scrollAreaWidgetContents)

        # SEND BUTTON
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(680, 540, 80, 35))
        Ui_Widget.component.append(self.pushButton)

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(
            QCoreApplication.translate("Widget", u"Widget", None))
        self.pushButton.setText(
            QCoreApplication.translate("Widget", u"Send", None))
        # restrict resizing windows
        Widget.setFixedSize(Widget.size())

    def set_state(self, state: bool) -> None:
        for component in Ui_Widget.component:
            component.setEnabled(state)
        # disable send button if there is no text and plainTextEdit is enabled
        self.plainTextEdit.textChanged.connect(
            lambda: self.pushButton.setEnabled(len(self.plainTextEdit.toPlainText()) > 0 and self.plainTextEdit.isEnabled()))
        self.pushButton.setEnabled(False)


class Widget(QWidget):
    def eventFilter(self, watched: QObject, event: any) -> bool:
        if watched == self.ui.plainTextEdit:
            # if single Enter key is pressed, send message
            # if Shift+Enter key is pressed, insert a new line
            if event.type() == QEvent.KeyPress:
                if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter):
                    if event.modifiers() & Qt.ShiftModifier:
                        self.ui.plainTextEdit.insertPlainText("\n")
                        return True
                    self.ui.pushButton.click()
                    return True
        return super().eventFilter(watched, event)

    def send_message(self) -> None:
        message = self.ui.plainTextEdit.toPlainText()
        client.send(message.encode('utf-8'))
        self.ui.textBrowser.append("You: "+message)
        self.ui.plainTextEdit.clear()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.plainTextEdit.setFocus()
        self.ui.plainTextEdit.installEventFilter(self)


# ----------------------------------------------------------TCP Socket Programming----------------------------------------------------------


# receive messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_room.ui.textBrowser.append(message)
        except:
            client.close()
            break


# --------------------------------------------------------------Global Variables--------------------------------------------------------------
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app = QApplication(sys.argv)
chat_room = Widget()

# ----------------------------------------------------------Main----------------------------------------------------------
if __name__ == "__main__":

    # create a login widget
    login = Login()
    login.show()
    
    # request and store nickname
    # nickname = input('Choose your nickname: ')
    # client.send(nickname.encode('utf-8'))
    # message = client.recv(1024).decode('utf-8')
    # while message == 'RESEND_NICK' or message == "INVALID_NICK":
    #     if message == "INVALID_NICK":
    #         nickname = input('Invalid nickname. Choose another: ')
    #     else:
    #         nickname = input('Nickname already in use. Choose another: ')
    #     client.send(nickname.encode('utf-8'))
    #     message = client.recv(1024).decode('utf-8')

    # # start threads for listening and writing
    # receive_thread = threading.Thread(target=receive)
    # receive_thread.start()

    # # start the widget
    # widget.ui.set_state(True)
    # widget.show()
    app.aboutToQuit.connect(lambda: client.close())
    sys.exit(app.exec())
