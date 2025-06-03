from PyQt5.QtWidgets import QWidget , QVBoxLayout , QLabel 
from PyQt5.QtCore import pyqtSignal , Qt
from PyQt5.QtGui import QCursor , QPixmap

import Styles.colors as cl

class VerticalIconTextButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, icon_path, text, parent=None,hover_bg = cl.SYS_BG1):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)

        # Icon
        self.icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet(f"""
            color: {cl.SYS_FG1};
            font-size: 12px;
            font-weight: 500;
        """)

        # Add to layout
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

        # Base style
        self.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border: none;
                margin-top:5px;
            }}
            QWidget:hover {{
                background-color: {hover_bg}
            }}
        """)

        self.setFixedSize(85, 60)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()