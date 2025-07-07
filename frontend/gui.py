from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import os
import socket
from backend.aes_utils import encrypt_message, decrypt_message

import sys

HOST = '127.0.0.1'
PORT = 9999
shared_key = "my_shared_secret"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


class ReceiverThread(QThread):
    message_received = pyqtSignal(str)

    def run(self):
        while True:
            try:
                msg = client.recv(4096).decode()
                decrypted = decrypt_message(shared_key, msg)
                self.message_received.emit("Friend: " + decrypted)
            except:
                break


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enchat - Secure Chat")
        self.setGeometry(100, 100, 500, 400)

        icon_path = os.path.join(os.path.dirname(__file__), 'fav.png')
        self.setWindowIcon(QIcon(icon_path))


        self.main_layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.main_layout.addWidget(self.chat_display)

        self.message_input = QLineEdit()
        self.main_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.main_layout.addWidget(self.send_button)

        self.setLayout(self.main_layout)  # setLayout() is valid

        self.receiver = ReceiverThread()
        self.receiver.message_received.connect(self.update_chat)
        self.receiver.start()


    def send_message(self):
        msg = self.message_input.text()
        self.message_input.clear()
        encrypted = encrypt_message(shared_key, msg)
        client.send(encrypted.encode())
        self.chat_display.append("You: " + msg)

    def update_chat(self, msg):
        self.chat_display.append(msg)


def start_gui():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_gui()
