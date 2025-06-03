#Qt Imports
from PyQt5.QtWidgets import (
    QWidget ,QHBoxLayout, QLabel
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

#Styles Import
import Styles.styles as styles


class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
    
    def setup_ui(self):
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        header_layout.setSpacing(0)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/sppl-logo-white.png"))
        self.logo.setFixedSize(50, 50)
        self.logo.setStyleSheet("margin:5px")
        self.logo.setScaledContents(True)

        self.logoLabel1 = QLabel("SPPL India")
        self.logoLabel1.setStyleSheet(styles.text_style2)

        header_layout.addSpacing(10)
        header_layout.addWidget(self.logo,Qt.AlignVCenter)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.logoLabel1,Qt.AlignVCenter)
        

        self.setLayout(header_layout)