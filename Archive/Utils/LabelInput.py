from PyQt5.QtWidgets import (
    QLabel,QLineEdit
)
from qfluentwidgets import ComboBox
import Styles.styles as styles


def GetLabelLineEdit(label_text,placeholder_text):
    label = QLabel(label_text)
    label.setStyleSheet(styles.text_style3)
    input = QLineEdit()
    input.setPlaceholderText(placeholder_text)
    input.setStyleSheet(styles.input_style1+";QLineEdit::placeholder{font-size:8px}")
    input.setFixedHeight(24)

    return label,input

def GetLabelCombo(label_text,combo_items):
    label = QLabel(label_text)
    label.setStyleSheet(styles.text_style3)
    combo = ComboBox()
    combo.addItems(combo_items)
    dfont = combo.font()
    dfont.setPointSize(11)
    combo.setFont(dfont)
    combo.setFixedHeight(25)

    return label,combo