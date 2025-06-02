from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.setGeometry(100, 100, 400, 300)
        self.label = QLabel("Hello from PyQt5!", self)
        self.label.move(100, 130)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
