from PyQt5.QtWidgets import QLabel 

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


def GetIcon(path:str,size:float):
    icon_label = QLabel()
    pixmap = QPixmap(path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    icon_label.setPixmap(pixmap)
    icon_label.setAlignment(Qt.AlignCenter)
    icon_label.setStyleSheet("border:none;outline:none")
    icon_label.setCursor(Qt.PointingHandCursor)

    return icon_label