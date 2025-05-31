import sys
from PyQt5 import QtWidgets, QtGui
import pyvista as pv
from pyvistaqt import QtInteractor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set custom app icon (taskbar + window)
        icon = QtGui.QIcon("app_icon.ico")  # Use .ico for full effect on Windows
        self.setWindowIcon(icon)

        # Control panel widget
        control_panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(control_panel)
        add_sphere_btn = QtWidgets.QPushButton("Add Sphere")
        layout.addWidget(add_sphere_btn)

        # PyVista 3D widget
        self.plotter = QtInteractor(self)
        add_sphere_btn.clicked.connect(self.add_sphere)

        # Layout setup
        container = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(container)
        h_layout.addWidget(control_panel, 1)
        h_layout.addWidget(self.plotter.interactor, 3)
        self.setCentralWidget(container)

    def add_sphere(self):
        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere)
        self.plotter.reset_camera()
        self.plotter.render()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Set icon for the QApplication (affects taskbar on some OS)
    app.setWindowIcon(QtGui.QIcon("app_icon.ico"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
