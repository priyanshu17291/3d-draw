import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QLabel


dark_stylesheet = """
QMainWindow {
    background-color: #2b2b2b;
}

QDockWidget {
    background-color: #3c3f41;
    color: white;
    font-weight: bold;
    border: 1px solid #222;
}

QDockWidget::title {
    background-color: black;
    padding: 4px;
}

QLabel, QTextEdit {
    color: white;
    background-color: #2b2b2b;
    border: none;
}
"""


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dockable Window Example")
        self.setGeometry(100, 100, 800, 600)

        # Central widget (e.g., your main editor area)
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Create a dockable widget
        dock1 = QDockWidget("Toolbox", self)
        dock1.setWidget(QLabel("This is the toolbox"))
        dock1.setFloating(False)  # Start docked
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        # Another dockable panel
        dock2 = QDockWidget("Properties", self)
        dock2.setWidget(QLabel("Properties go here"))
        self.addDockWidget(Qt.RightDockWidgetArea, dock2)

        # You can allow them to be moved around
        dock1.setFeatures(QDockWidget.DockWidgetMovable |
                          QDockWidget.DockWidgetFloatable |
                          QDockWidget.DockWidgetClosable)
        dock2.setFeatures(QDockWidget.DockWidgetMovable |
                          QDockWidget.DockWidgetFloatable |
                          QDockWidget.DockWidgetClosable)
        
        

if __name__ == "__main__":
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_stylesheet)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
