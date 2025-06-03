from PyQt5.QtWidgets import QWidget, QApplication , QVBoxLayout
from PyQt5.QtGui import QColor, QPainter, QFont, QPen
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty, QVariantAnimation, QEasingCurve
import sys

class SwitchButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._on = False
        self.onText = "ON"
        self.offText = "OFF"
        self.onColor = QColor(66, 133, 244)   # Google blue
        self.offColor = QColor(200, 200, 200)
        self._circle_position = 3
        self._current_color = self.offColor

        # Circle animation
        self._circle_anim = QPropertyAnimation(self, b"circle_position", self)
        self._circle_anim.setDuration(300)
        self._circle_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Color animation
        self._color_anim = QVariantAnimation(self)
        self._color_anim.setDuration(300)
        self._color_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._color_anim.valueChanged.connect(self._update_color)

    def _update_color(self, value):
        self._current_color = value
        self.update()

    def mousePressEvent(self, event):
        self._on = not self._on

        # Animate circle
        start = 3 if not self._on else self.width() - 27
        end = self.width() - 27 if not self._on else 3
        self._circle_anim.stop()
        self._circle_anim.setStartValue(start)
        self._circle_anim.setEndValue(end)
        self._circle_anim.start()

        # Animate background color
        self._color_anim.stop()
        self._color_anim.setStartValue(self.offColor if self._on else self.onColor)
        self._color_anim.setEndValue(self.onColor if self._on else self.offColor)
        self._color_anim.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # Background
        p.setBrush(self._current_color)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(rect, 15, 15)

        # Toggle Circle
        p.setBrush(Qt.white)
        p.drawEllipse(QRectF(self._circle_position, 3, 24, 24))

        # Text
        p.setFont(QFont("Arial", 8, QFont.Bold))
        p.setPen(QPen(Qt.white))
        text = self.onText if self._on else self.offText
        p.drawText(rect, Qt.AlignCenter, text)

    def isChecked(self):
        return self._on

    def setChecked(self, checked):
        if self._on != checked:
            self.mousePressEvent(None)

    def get_circle_position(self):
        return self._circle_position

    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = pyqtProperty(int, fget=get_circle_position, fset=set_circle_position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    win_layout = QVBoxLayout()
    w = SwitchButton()
    win_layout.addWidget(w)
    win.setLayout(win_layout)
    win.show()
    sys.exit(app.exec_())
