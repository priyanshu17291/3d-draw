from PyQt5 import QtWidgets
import pyvista as pv
from pyvistaqt import QtInteractor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Control panel widget
        control_panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(control_panel)
        add_sphere_btn = QtWidgets.QPushButton("Add Sphere")
        layout.addWidget(add_sphere_btn)

        # PyVista 3D widget
        self.plotter = QtInteractor(self)
        
        # Connect button to action
        add_sphere_btn.clicked.connect(self.add_sphere)

        # Layout setup
        container = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(container)
        h_layout.addWidget(control_panel, 1)      # control panel takes 1/4th width
        h_layout.addWidget(self.plotter.interactor, 3)  # 3D view takes rest

        self.setCentralWidget(container)

    def add_sphere(self):
        sphere = pv.Sphere()
        self.plotter.add_mesh(sphere)
        self.plotter.reset_camera()
        self.plotter.render()

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()
