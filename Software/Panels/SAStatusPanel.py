from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox,QScrollArea
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
import Styles.styles as styles
import Styles.colors as cl

class SAStatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(styles.panel_style1)
        layout = QVBoxLayout()
        layout.setContentsMargins(20,1,10,10)
        layout.setSpacing(0)

        sampleText = """
Current Sensor : S10023
Server Status : Connected
Network : Online

[10:00] : 1001.json saved
[10:05] : 1002.json saved
[10:10] : 1003.json saved
"""
        sampleLabel = QLabel(sampleText)
        sampleLabel.setStyleSheet(styles.infotext_style1)
        layout.addWidget(sampleLabel)
        layout.addStretch(1)
        



        self.setLayout(layout)