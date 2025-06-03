from PyQt5.QtWidgets import QFrame
import Styles.colors as cl

class SeparatorLine(QFrame):
    def __init__(self, color=f"{cl.SYS_SEP1}", orientation="H", length=100, thickness=1, parent=None):
        super().__init__(parent)

        # Orientation: HLine or VLine
        if orientation.upper() == "H":
            self.setFrameShape(QFrame.HLine)
            self.setFixedHeight(thickness)
            self.setFixedWidth(length)
        elif orientation.upper() == "V":
            self.setFrameShape(QFrame.VLine)
            self.setFixedWidth(thickness)
            self.setFixedHeight(length)
        else:
            raise ValueError("Orientation must be 'H' or 'V'")

        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet(f"background-color: {color}; border: none;")
