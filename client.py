
from PySide6.QtWidgets import (QApplication, QLineEdit, QPlainTextEdit, QPushButton,
                               QScrollArea, QSizePolicy, QTextBrowser, QWidget)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
import sys
import socket
import threading
import ctypes
# ----------------------------------------------------------Graphic User Interface----------------------------------------------------------


class Ui_Widget(object):
    component = []

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.plainTextEdit = QPlainTextEdit(Widget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 530, 651, 61))
        Ui_Widget.component.append(self.plainTextEdit)

        self.textBrowser = QTextBrowser(Widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 651, 511))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(13)
        self.textBrowser.setFont(font)
        self.textBrowser.setStyleSheet(
            "QTextBrowser {padding: 10px; border: 1px solid black;}")
        Ui_Widget.component.append(self.textBrowser)

        self.scrollArea = QScrollArea(Widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(670, 10, 120, 511))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(
            u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 118, 509))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        Ui_Widget.component.append(self.scrollArea)

        # LIST OF USERS
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(
            u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 118, 509))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        Ui_Widget.component.append(self.scrollAreaWidgetContents)

        # SEND BUTTON
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(680, 540, 83, 29))
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


# create a widget object
app = QApplication(sys.argv)
widget = Widget()

# ----------------------------------------------------------TCP Socket Programming----------------------------------------------------------


# receive messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            widget.ui.textBrowser.append(message)
        except:
            ctypes.windll.user32.MessageBoxW(
                0, "You have been disconnected from the server", "Notification", 0)
            client.close()
            break

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ----------------------------------------------------------Main----------------------------------------------------------
if __name__ == "__main__":

    # USAGE: python client.py <host> <port>
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)

    # get host and port from command line
    host = sys.argv[1]
    port = int(sys.argv[2])

    # connect to the server
    try:
        client.connect((host, port))
    except:
        ctypes.windll.user32.MessageBoxW(
            0, "Cannot connect to the server", "Error", 0)
        sys.exit(1)

    # request and store nickname
    nickname = input('Choose your nickname: ')
    client.send(nickname.encode('utf-8'))
    message = client.recv(1024).decode('utf-8')
    while message == 'RESEND_NICK':
        nickname = input('Nickname already in use. Choose another: ')
        client.send(nickname.encode('utf-8'))
        message = client.recv(1024).decode('utf-8')

    # start threads for listening and writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # start the widget
    widget.ui.set_state(True)
    widget.show()
    app.aboutToQuit.connect(lambda: client.close())
    sys.exit(app.exec())
