from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox,QStackedWidget
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

from qfluentwidgets import ComboBox , setTheme, Theme, setThemeColor , SwitchButton

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
import Styles.styles as styles
import Styles.colors as cl


class ToggleText(QWidget):
    def __init__(self,label,alignEnd=False,label_style = None):
        super().__init__()
        self.label = label
        self.alignEnd = alignEnd
        self.label_style = label_style
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        label= QLabel(self.label)
        if self.label_style == None:
            label.setStyleSheet(styles.text_style1)
        else:
            label.setStyleSheet(self.label_style)

        switchButton = SwitchButton(self)
        switchButton.setOffText("")
        switchButton.setOnText("")
        switchButton.setChecked(False)

        layout.addWidget(label,0,Qt.AlignVCenter)
        if self.alignEnd:
            layout.addStretch(1)
        layout.addWidget(switchButton,0,Qt.AlignVCenter)

        self.setLayout(layout)
