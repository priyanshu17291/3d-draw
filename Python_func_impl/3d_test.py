# import pyvista as pv
# import numpy as np
# import time

# # Create the plotting window
# plotter = pv.Plotter()

# # Generate initial grid
# x = np.linspace(-5, 5, 50)
# y = np.linspace(-5, 5, 50)
# x, y = np.meshgrid(x, y)
# z = np.sin(x)

# # Create the surface mesh
# surface = pv.StructuredGrid(x, y, z)

# # Add the mesh to the plotter
# plotter.add_mesh(surface, color='royalblue', show_edges=False)

# # Start the interactive window (non-blocking)
# plotter.show(auto_close=False, interactive_update=True)

# # Animation loop
# phase = 0.0
# for _ in range(500):  # animate 500 frames
#     phase += 0.1
#     new_z = np.sin(x + phase) * np.cos(y + phase)
#     surface.points[:, 2] = new_z.ravel()
#     surface.Modified()  # Capital M here
#     plotter.update()    # redraw the scene
#     time.sleep(0.05)    # ~20 FPS

# # Leave the window open
# plotter.close()

#the code below is for testing the joining of points by cylinders
import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, 
    QWidget, QLabel, QHBoxLayout, QLineEdit
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive 3D Editor - PyVista + Qt")
        self.setGeometry(100, 100, 1000, 700)

        # Initialize data
        self.points = []
        self.edges = []
        self.selected_points = []

        # UI and 3D setup
        self.init_ui()

        # Add sample points
        self.points = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        self.update_plot()

    def init_ui(self):
        """Create and lay out widgets."""
        self.frame = QWidget()
        self.layout = QHBoxLayout(self.frame)
        self.setCentralWidget(self.frame)

        # Plotter widget
        self.plotter = QtInteractor(self.frame)
        self.plotter.add_axes()
        self.layout.addWidget(self.plotter.interactor)

        # Right-side controls
        control_panel = QVBoxLayout()
        self.layout.addLayout(control_panel)

        self.input_fields = [QLineEdit() for _ in range(3)]
        for i, field in enumerate(self.input_fields):
            field.setPlaceholderText(f"Coord {['X','Y','Z'][i]}")
            control_panel.addWidget(field)

        buttons = [
            ("Add Point", self.add_point),
            ("Connect Selected Points", self.connect_points),
            ("Clear Selection", self.clear_selection),
            ("Clear All", self.clear_all),
            ("Test Select First Point", self.test_select_first_point),
        ]
        for label, handler in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            control_panel.addWidget(btn)

        self.status = QLabel("Status: Ready")
        control_panel.addWidget(self.status)

        # Enable point picking last (after plotter is ready)
        self.plotter.enable_point_picking(
            callback=self.pick_point,
            use_mesh=False,
            show_point=False,
            tolerance=0.15,
            left_clicking=True
        )

    def update_plot(self):
        """Refresh 3D scene."""
        self.plotter.clear()
        if not self.points:
            return

        mesh = pv.PolyData(np.array(self.points))
        if self.edges:
            lines = np.array([[2, *edge] for edge in self.edges])
            mesh.lines = lines

        colors = np.array([
            [255, 0, 0] if i in self.selected_points else [0, 0, 255]
            for i in range(len(self.points))
        ])
        mesh["colors"] = colors

        self.plotter.add_mesh(
            mesh, scalars="colors", rgb=True,
            point_size=15, render_points_as_spheres=True, line_width=5
        )
        self.plotter.reset_camera()

    def pick_point(self, picked):
        if not self.points:
            self.status.setText("No points available.")
            return

        pts = np.array(self.points)
        dists = np.linalg.norm(pts - picked, axis=1)
        nearest = np.argmin(dists)
        if dists[nearest] > self.selection_threshold():
            self.status.setText(f"Too far from any point.")
            return

        if nearest in self.selected_points:
            self.selected_points.remove(nearest)
            self.status.setText(f"Deselected point {nearest}")
        else:
            self.selected_points.append(nearest)
            self.status.setText(f"Selected point {nearest}")

        self.update_plot()

    def selection_threshold(self):
        if len(self.points) < 2:
            return 0.5
        dists = [
            np.linalg.norm(np.array(self.points[i]) - np.array(self.points[j]))
            for i in range(len(self.points)) for j in range(i+1, len(self.points))
        ]
        return np.mean(dists) * 0.5

    def add_point(self):
        try:
            coords = [float(f.text()) for f in self.input_fields]
            self.points.append(coords)
            for f in self.input_fields:
                f.clear()
            self.status.setText(f"✅ Added {coords}")
            self.update_plot()
        except ValueError:
            self.status.setText("❌ Enter valid X, Y, Z coordinates")

    def connect_points(self):
        if len(self.selected_points) != 2:
            self.status.setText("❌ Select exactly 2 points")
            return
        edge = sorted(self.selected_points)
        if edge in [sorted(e) for e in self.edges]:
            self.status.setText("❌ Edge already exists")
            return
        self.edges.append(edge)
        self.status.setText(f"✅ Connected: {edge}")
        self.selected_points.clear()
        self.update_plot()

    def clear_selection(self):
        self.selected_points.clear()
        self.status.setText("Selection cleared")
        self.update_plot()

    def clear_all(self):
        self.points.clear()
        self.edges.clear()
        self.selected_points.clear()
        self.status.setText("All cleared")
        self.update_plot()

    def test_select_first_point(self):
        if self.points:
            self.selected_points = [0]
            self.status.setText("Selected point 0")
            self.update_plot()
        else:
            self.status.setText("No points to select")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
