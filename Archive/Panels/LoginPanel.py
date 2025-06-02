#Qt Imports
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

#Styles Import
import Styles.styles as styles
import Styles.colors as cl

class LoginPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        # self.main_window = main_window

    def setup_ui(self):
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")
        layout = QVBoxLayout()

        self.label = QLabel("Login to SPPL India")
        self.label.setStyleSheet(styles.header_style1)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/sppl-logo-white.png"))
        self.logo.setFixedSize(150, 150)
        self.logo.setScaledContents(True)

        self.userid_input = QLineEdit()
        self.userid_input.setPlaceholderText("UserID")
        self.userid_input.setFixedSize(320, 30)
        self.userid_input.setStyleSheet(styles.input_style1)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(320, 30)
        self.password_input.setStyleSheet(styles.input_style1)

        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.onSubmit)
        self.button.setFixedSize(320, 35)
        self.button.setStyleSheet(styles.button_style1)
        self.button.setDefault(True)
        self.button.setAutoDefault(True)

        self.signup_label = QLabel("Don't have an account? Sign-up for Free")
        self.signup_label.setStyleSheet(styles.text_style1)
        self.signup_label.setCursor(QCursor(Qt.PointingHandCursor))

        layout.addStretch(1)
        layout.addWidget(self.logo, 0, Qt.AlignHCenter)
        layout.addSpacing(10)
        layout.addWidget(self.label, 0, Qt.AlignHCenter)
        layout.addSpacing(35)
        layout.addWidget(self.userid_input, 0, Qt.AlignHCenter)
        layout.addSpacing(5)
        layout.addWidget(self.password_input, 0, Qt.AlignHCenter)
        layout.addSpacing(25)
        layout.addWidget(self.button, 0, Qt.AlignHCenter)
        layout.addSpacing(35)
        layout.addWidget(self.signup_label, 0, Qt.AlignHCenter)
        layout.addStretch(2)

        layout.setSpacing(5)
        self.setLayout(layout)

    def onSubmit(self):
        userdid = self.userid_input.text
        password = self.password_input.text
