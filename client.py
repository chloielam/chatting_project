
import re
import ctypes
import threading
import socket
import sys
from PySide6.QtWidgets import (QApplication, QLineEdit, QPlainTextEdit, QPushButton, QVBoxLayout,
                               QScrollArea, QSizePolicy, QTextBrowser, QWidget, QLabel)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QIntValidator, QRegularExpressionValidator)

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent, QRegularExpression)


# ---------------------------------------------------------Connect Form--------------------------------------------------------


class ConnectWidget(object):
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


class ConnectFormGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui = ConnectWidget()
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

        # testing purpose
        self.ui.host_input.setText("Z-DESKTOP")
        self.ui.port_input.setText("9999")

    def connect(self):
        try:
            client_socket.connect((self.ui.host_input.text(),
                                   int(self.ui.port_input.text())))
            name_gui.show()
            self.close()
        except:
            ctypes.windll.user32.MessageBoxW(
                0, "Cannot connect to the server!", "Error", 0)


# ----------------------------------------------------------Name Form----------------------------------------------------------


class NameWidget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")

        Widget.resize(450, 300)

        self.nickname_input = QLineEdit(Widget)
        self.nickname_input.setObjectName(u"nickname_input")
        self.nickname_input.setGeometry(QRect(100, 110, 250, 50))

        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(15)
        font.setBold(True)
        self.nickname_input.setFont(font)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 50, 450, 51))
        self.label.setAlignment(Qt.AlignCenter)

        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)
        self.warning_label = QLabel(Widget)
        self.warning_label.setObjectName(u"warning_label")
        self.warning_label.setGeometry(QRect(0, 150, 450, 51))

        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.warning_label.setFont(font2)
        self.warning_label.setStyleSheet(u"text-align: center;\n"
                                         "vertical-align: center;\n"
                                         "color: red;")
        self.warning_label.setAlignment(Qt.AlignCenter)

        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(150, 200, 150, 51))
        self.pushButton.setStyleSheet(u"text-align: center;\n"
                                      "vertical-align: center;")
        self.pushButton.setFont(font)
        self.pushButton.setAutoDefault(True)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(
            QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate(
            "Widget", u"Choose a nickname", None))
        self.warning_label.setText("")
        self.pushButton.setText(QCoreApplication.translate(
            "Widget", u"Enter Room", None))


class NameFormGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui = NameWidget()
        self.ui.setupUi(self)

        # set criteria for input area
        self.ui.pushButton.setEnabled(0)
        self.ui.pushButton.clicked.connect(self.enter_room)

        self.ui.nickname_input.setFocus()
        self.ui.nickname_input.setAlignment(Qt.AlignCenter)
        self.ui.nickname_input.textChanged.connect(self.on_text_changed)
        self.ui.nickname_input.returnPressed.connect(
            lambda: self.ui.pushButton.click() if self.ui.pushButton.isEnabled() else None)
        self.ui.nickname_input.setMaxLength(16)
        self.ui.nickname_input.setPlaceholderText("2-16 characters")
        self.ui.nickname_input.setTabOrder(
            self.ui.nickname_input, self.ui.pushButton)

        # restrict resizing windows
        self.setFixedSize(self.size())

    def on_text_changed(self) -> None:
        is_valid_name = self.validate_nickname()
        self.ui.pushButton.setEnabled(
            self.ui.nickname_input.text() != "" and is_valid_name)
        self.ui.warning_label.setText(
            "Invalid nickname!") if not is_valid_name else self.ui.warning_label.setText("")

    def validate_nickname(self) -> bool:

        valid_pattern = re.compile(
            r'^(?=.{2,16}$)(?![_.\s])(?!.*[_.]{2})(?!.*[\s]{2})[\w\s]+(?<![_.\s])$')
    # username is 2-16 characters long
    # no _ or . or whitespace at the beginning
    # no __ or _. or ._ or .. or double whitespace inside
    # allowed characters
    # no _ or . or whitespace at the end
        return valid_pattern.match(self.ui.nickname_input.text()) is not None

    def enter_room(self) -> None:
        try:
            nickname = self.ui.nickname_input.text()
            client_socket.send(nickname.encode('utf-8'))
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'RESEND_NICK':
                self.ui.warning_label.setText(
                    "Nickname already in use!")
                return
            chat_room.ui.textBrowser.append(message)
            chat_room.start_room()
            self.close()
        except:
            ctypes.windll.user32.MessageBoxW(
                0, "Cannot connect to the server!", "Error", 0)
            client_socket.close()
            sys.exit(0)


# ----------------------------------------------------------Chat Room----------------------------------------------------------


class ChatRoom(object):

    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)

        self.textBrowser = QTextBrowser(Widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 10, 650, 500))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        self.textBrowser.setFont(font)
        self.textBrowser.setStyleSheet(
            u"border: 1px solid gray; text-indent: 10px; line-height: 1.2;")

        self.plainTextEdit = QPlainTextEdit(Widget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 530, 650, 50))
        self.plainTextEdit.setFont(font)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(
            u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 120, 500))

        # SCROLL AREA
        self.scrollArea = QScrollArea(Widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(670, 10, 120, 500))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # SEND BUTTON
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(680, 540, 80, 35))

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(
            QCoreApplication.translate("Widget", u"LAN Chatter", None))
        self.pushButton.setText(
            QCoreApplication.translate("Widget", u"Send", None))
        # restrict resizing windows
        Widget.setFixedSize(Widget.size())


class ChatRoomGUI(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = ChatRoom()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.plainTextEdit.setFocus()
        self.ui.plainTextEdit.installEventFilter(self)
        self.ui.plainTextEdit.textChanged.connect(
            lambda: self.ui.pushButton.setEnabled(len(self.ui.plainTextEdit.toPlainText()) > 0 and self.ui.plainTextEdit.isEnabled()))
        self.ui.plainTextEdit.setTabOrder(
            self.ui.plainTextEdit, self.ui.pushButton)
        self.ui.plainTextEdit.setPlaceholderText("Type your message here")
        self.ui.plainTextEdit.setAcceptDrops(True)
        self.ui.plainTextEdit.setUndoRedoEnabled(True)
        self.ui.plainTextEdit.textChanged.connect(
            lambda: self.ui.plainTextEdit.setPlainText(self.ui.plainTextEdit.toPlainText(
            )[:1024]) if len(self.ui.plainTextEdit.toPlainText()) > 1024 else None
        )
        self.ui.pushButton.setEnabled(False)
        self.ui.scrollArea.setAlignment(Qt.AlignTop)
        self.ui.scrollAreaWidgetContents.setLayout(QVBoxLayout())
        self.ui.scrollAreaWidgetContents.layout().setAlignment(Qt.AlignTop)
        self.font = QFont()
        self.font.setPointSize(13)
        self.font.setBold(True)

    def update_online_users(self) -> None:
        for i in reversed(range(self.ui.scrollAreaWidgetContents.layout().count())):
            self.ui.scrollAreaWidgetContents.layout().itemAt(i).widget().setParent(None)
        label = QLabel()
        label.setObjectName(u"Users")
        label.setText(QCoreApplication.translate("Widget", u"Online:", None))
        label.setAlignment(Qt.AlignLeft)
        label.setGeometry(QRect(0, 0, 120, 120))
        label.setFont(self.font)
        for user in online_users:
            label = QLabel()
            label.setObjectName(u"label")
            label.setText(QCoreApplication.translate(
                "Widget", f"{user}", None))
            label.setAlignment(Qt.AlignLeft)
            label.setGeometry(QRect(0, 0, 120, 80))
            label.setStyleSheet(
                u"border: 1px solid gray; text-indent: 10px; line-height: 1.5;")
            label.setFont(self.font)
            self.ui.scrollAreaWidgetContents.layout().addWidget(label)

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

    def __send_message(self, message: str) -> None:
        if re.compile(r'^\s*/help\s*$').match(message):
            self.ui.textBrowser.append(
                "-----------------------------   List of commands   -----------------------------\n")
            self.ui.textBrowser.append(
                "/help: List of commands\n")
            self.ui.textBrowser.append(
                "/private (<username>) <message>: Send private message to a user\n")
            self.ui.textBrowser.append(
                "/quit: Leave the chatroom\n")
            self.ui.textBrowser.append(
                "/clear: Clear the chat history\n")
            self.ui.textBrowser.append(
                "--------------------------------------------------------------------------------\n")
            self.ui.plainTextEdit.clear()
            return
        if re.compile(r'^\s*/quit\s*$').match(message):
            ctypes.windll.user32.MessageBoxW(
                0, "You have left the chatroom!", "Info", 0)
            self.close()
            client_socket.close()
            sys.exit(0)
        if re.compile(r'^\s*/clear\s*$').match(message):
            self.ui.textBrowser.clear()
            self.ui.plainTextEdit.clear()
            return
        if re.compile(r'^\s*/private.*$').match(message):
            valid_private_pattern = re.compile(
                r"^[\n\s]*(/private)\s+(\(.{2,16}\))\s+(.+)$")
            if valid_private_pattern.match(message):
                _, receiver, content = valid_private_pattern.match(
                    message).groups()
                if content.strip() == "":
                    self.ui.plainTextEdit.clear()
                    self.ui.textBrowser.append(
                        "---- Warning: Cannot send empty message!\n")
                    return
                # client_socket.send(
                #    f"/private {receiver} {content.strip()}".encode('utf-8'))
                send_to_server(f'/private {receiver} {content.strip()}')

                self.ui.textBrowser.append(
                    f"You to {receiver[1:-1]}: {content.strip()}")
                self.ui.plainTextEdit.clear()
                return
            else:
                self.ui.plainTextEdit.clear()
                self.ui.textBrowser.append(
                    "---- Usage: /private (<username>) <message>\n")
                return
        send_to_server(message)
        self.ui.textBrowser.append("You: " + message)
        self.ui.plainTextEdit.clear()

    def send_message(self) -> None:
        try:
            self.__send_message(self.ui.plainTextEdit.toPlainText())
        except:
            self.ui.textBrowser.append(
                "---------------------------   Cannot connect to the server!  ---------------------------\n")
            self.ui.pushButton.setEnabled(False)
            client_socket.close()

    def start_room(self) -> None:
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        self.show()


# ---------------------------------------------------TCP Socket Programming----------------------------------------------------


def send_to_server(message: str) -> None:
    if len(message) < 1024:
        message = message + (1024-len(message))*'\x00'
        client_socket.send(message.encode('utf-8'))
    else:
        message_list = []
        while len(message) > 1024:
            message_list.append(message[:1024])
            message = message[1024:]
        message_list.append(message + (1024-len(message))*'\x00')
        if message_list[-1] == 1024 * '\x00':
            message_list.pop()
        for message in message_list:
            client_socket.send(message.encode('utf-8'))


def receive() -> None:
    while True:
        try:
            message = client_socket.recv(1024)
        # if message.startswith((b'UPDATE')):
        #     print("yes")
        #     continue
            raw_message = message.decode('utf-8')
        # print('---')
        # print(raw_message)
        # print(len(raw_message))
        # print('---')
            chat_room.ui.textBrowser.append(raw_message)
        except:
            chat_room.ui.textBrowser.append(
                "---------------------------   Cannot connect to the server!  ---------------------------\n")
            chat_room.ui.pushButton.setEnabled(False)
            client_socket.close()
            break


def receive_file() -> None:
    pass


def send_file() -> None:
    pass


# ------------------------------------------------------Global Variables-------------------------------------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app = QApplication(sys.argv)
login = ConnectFormGUI()
name_gui = NameFormGUI()
chat_room = ChatRoomGUI()
online_users = []

# ----------------------------------------------------------Main----------------------------------------------------------
if __name__ == "__main__":
    login.show()
    app.aboutToQuit.connect(lambda: client_socket.close())
    sys.exit(app.exec())
