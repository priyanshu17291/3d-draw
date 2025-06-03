from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
import Styles.styles as styles
import Styles.colors as cl


class AlarmPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(styles.panel_style1)
        layout = QVBoxLayout()
        layout.setContentsMargins(1,1,1,1)
        layout.setSpacing(0)

        # self.header = QLabel("Alarms")
        # self.header.setStyleSheet(styles.text_style2+";border:none;outline:none;margin:4px")

        # layout.addWidget(self.header,0)
        # layout.addStretch(1)

        self.setLayout(layout)