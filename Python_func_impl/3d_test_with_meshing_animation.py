import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, 
    QWidget, QLabel, QHBoxLayout, QLineEdit, QFileDialog, QSplitter
)
from PyQt5.QtCore import QTimer
import trimesh
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive 3D Editor - PyVista + Qt")
        self.setGeometry(100, 100, 1000, 700)

        # Initialize data
        self.points = []
        self.edges = []
        self.selected_points = []
        self.surfaces = []  # List to store all created surface meshes

        # UI and 3D setup
        self.init_ui()

        # Add sample points
        self.points = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        self.update_plot()
        self.surface_mesh = None  # Store the surface
        self.surface_actor = None
        self.original_surface_points = None
        self.vibration_timer = QTimer()
        self.vibration_timer.timeout.connect(self.animate_surface)
        self.vibration_phase = 0.0


    def init_ui(self):
        """Create and lay out widgets."""
        self.frame = QWidget()
        self.setCentralWidget(self.frame)

        # Use a splitter for a resizable layout
        self.layout = QHBoxLayout(self.frame)
        splitter = QSplitter()
        self.layout.addWidget(splitter)

        # Left-side controls
        control_panel_widget = QWidget()
        control_panel = QVBoxLayout(control_panel_widget)
        splitter.addWidget(control_panel_widget)

        # Plotter widget on the right
        self.plotter = QtInteractor(self.frame)
        self.plotter.enable_terrain_style()
        self.plotter.add_axes(interactive=True)
        splitter.addWidget(self.plotter.interactor)

        # Coordinate input fields
        self.input_fields = [QLineEdit() for _ in range(3)]
        for i, field in enumerate(self.input_fields):
            field.setPlaceholderText(f"Coord {['X','Y','Z'][i]}")
            control_panel.addWidget(field)

        # NEW input field for number of points to add (n)
        self.input_n = QLineEdit()
        self.input_n.setPlaceholderText("Number of points to add (n)")
        control_panel.addWidget(self.input_n)

        # Buttons and their handlers including the new button
        buttons = [
            ("Open File", lambda: QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")[0]),
            ("Save File", lambda: QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")[0]),
            ("Add Point", self.add_point),
            ("Connect Selected Points", self.connect_points),
            ("Generate Surface", self.generate_surface),
            ("Clear Selection", self.clear_selection),
            ("Clear All", self.clear_all),
            ("Test Select First Point", self.test_select_first_point),
            ("Export to GLTF", self.export_to_gltf),
            ("Add Points Along Line", self.add_points_along_line),  # NEW button added here
        ]
        for label, handler in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            control_panel.addWidget(btn)

        # Vibration buttons
        start_vibration_btn = QPushButton("Start Vibration")
        start_vibration_btn.clicked.connect(self.start_vibration)
        control_panel.addWidget(start_vibration_btn)

        # Status label
        self.status = QLabel("Status: Ready")
        control_panel.addWidget(self.status)

        # Enable point picking
        self.plotter.enable_point_picking(
            callback=self.pick_point,
            use_mesh=False,
            show_point=False,
            tolerance=0.15,
            left_clicking=True
        )

    def load_structure(self, file_path):
        try:
            mesh = pv.read(file_path)
            self.plotter.clear()  # Clear current scene

            # Re-add mesh to the scene
            self.plotter.add_mesh(mesh, show_edges=True)
            self.plotter.reset_camera()
            self.plotter.render()
            self.loaded_mesh = mesh
            print(f"Loaded: {file_path}")
        except Exception as e:
            print(f"Failed to load file: {e}")

    def save_structure(self, file_path):
        try:
            # Combine all elements (points, lines, surfaces) into a single PolyData if needed
            if hasattr(self, 'loaded_mesh'):
                self.loaded_mesh.save(file_path)
                print(f"Saved to: {file_path}")
            else:
                print("No mesh loaded or generated to save.")
        except Exception as e:
            print(f"Failed to save file: {e}")
    def generate_surface(self):
        if len(self.selected_points) < 3:
            self.status.setText("❌ Select at least 3 points to generate a surface.")
            return

        # Get selected point coordinates
        pts = np.array([self.points[i] for i in self.selected_points])

        # Create surface mesh using Delaunay triangulation
        surface = pv.PolyData(pts).delaunay_2d()
        surface = surface.subdivide(nsub=3, subfilter="linear")
        surface = surface.smooth(n_iter=100, relaxation_factor=0.1)
        self.surfaces.append(surface)

        # Add surface to the plotter
        self.plotter.add_mesh(
            surface,
            color='lightgreen',
            opacity=0.6,
            name=f'surface_{len(self.surfaces)}',
            pickable=False,
            show_edges=True,
            edge_color='white',
            lighting=True,
            specular=1.0,
            smooth_shading=True
        )

        self.status.setText("✅ Surface generated.")
        self.selected_points.clear()
        self.update_plot(redraw_surfaces=False)  # Prevent surfaces from being cleared


    def update_plot(self, redraw_surfaces=True):
        """Refresh 3D scene, optionally skipping surface re-addition."""

        # Remove old points mesh (don't reset camera yet)
        self.plotter.remove_actor("points_mesh", reset_camera=False)

        # If no points, nothing to draw
        if not self.points:
            return

        # Create PolyData mesh from points
        mesh = pv.PolyData(np.array(self.points, dtype=np.float32))  # Use float32 to avoid warnings

        # If edges exist, create lines representation
        if self.edges:
            # Each line has format [num_points_in_line, point1_index, point2_index]
            lines = np.array([[2, *edge] for edge in self.edges])
            mesh.lines = lines

        # Assign colors: red for selected points, blue otherwise
        colors = np.array([
            [255, 0, 0] if i in self.selected_points else [0, 0, 255]
            for i in range(len(self.points))
        ])
        mesh["colors"] = colors

        # Add points mesh to plotter
        self.plotter.add_mesh(
            mesh,
            scalars="colors",
            rgb=True,
            name="points_mesh",
            point_size=15,
            render_points_as_spheres=True,
            line_width=5
        )

        # Optionally redraw surfaces if any (like generated mesh surfaces)
        if redraw_surfaces and hasattr(self, "surfaces"):
            for i, surface in enumerate(self.surfaces):
                self.plotter.add_mesh(
                    surface,
                    color="lightgray",
                    opacity=0.6,
                    name=f"surface_{i}",
                    show_edges=True
                )

        # Reset camera to include all points, but could be modified
        self.plotter.reset_camera()



    def animate_surface(self):
        if not self.surfaces:
            return
        current_surface = self.surfaces[-1]  # Use the last generated surface
        amp = 0.1           # Vibration amplitude
        freq = 2.0          # Frequency (Hz)
        t = self.vibration_phase
        points = current_surface.points.copy()

        # Wave-like motion using phase shift based on point index
        phase_shift = np.linspace(0, 2 * np.pi, len(points))
        points[:, 2] += amp * np.sin(2 * np.pi * freq * t + phase_shift)

        current_surface.points = points
        self.surface_modified = True
        self.vibration_phase += 0.05
        self.plotter.update()

    def export_to_gltf(self):
        """Export the current 3D structure to a GLTF file using trimesh."""
        if not self.points and not self.surfaces:
            self.status.setText("❌ No geometry to export.")
            return

        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Export to GLTF", 
            "scene.gltf", 
            "GLTF Files (*.gltf);;All Files (*)"
        )
        
        if not file_path:
            return  # User cancelled

        try:
            # Create a scene to hold all meshes
            scene = trimesh.Scene()

            # Export points as small spheres
            if self.points:
                for i, point in enumerate(self.points):
                    sphere = trimesh.creation.icosphere(subdivisions=1, radius=0.05)
                    sphere.apply_translation(point)
                    
                    # Color based on selection
                    if i in self.selected_points:
                        sphere.visual.face_colors = [255, 0, 0, 255]  # Red for selected
                    else:
                        sphere.visual.face_colors = [0, 0, 255, 255]  # Blue for unselected
                    
                    scene.add_geometry(sphere, node_name=f'point_{i}')

            # Export edges as cylinders
            if self.edges:
                for i, edge in enumerate(self.edges):
                    p1 = np.array(self.points[edge[0]])
                    p2 = np.array(self.points[edge[1]])
                    
                    # Calculate cylinder parameters
                    direction = p2 - p1
                    length = np.linalg.norm(direction)
                    center = (p1 + p2) / 2
                    
                    if length > 0:
                        # Create cylinder
                        cylinder = trimesh.creation.cylinder(radius=0.02, height=length)
                        
                        # Align cylinder with edge direction
                        if not np.allclose(direction, [0, 0, length]):
                            # Calculate rotation to align cylinder with edge
                            z_axis = np.array([0, 0, 1])
                            direction_norm = direction / length
                            
                            if not np.allclose(direction_norm, z_axis):
                                rotation_axis = np.cross(z_axis, direction_norm)
                                if np.linalg.norm(rotation_axis) > 1e-6:
                                    rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
                                    angle = np.arccos(np.clip(np.dot(z_axis, direction_norm), -1, 1))
                                    rotation_matrix = trimesh.transformations.rotation_matrix(angle, rotation_axis)
                                    cylinder.apply_transform(rotation_matrix)
                        
                        cylinder.apply_translation(center)
                        cylinder.visual.face_colors = [0, 255, 0, 255]  # Green for edges
                        scene.add_geometry(cylinder, node_name=f'edge_{i}')

            # Export surfaces
            if self.surfaces:
                for i, surface in enumerate(self.surfaces):
                    # Convert PyVista mesh to trimesh
                    vertices = surface.points
                    faces = surface.faces.reshape(-1, 4)[:, 1:4]  # Remove the first column (face size)
                    
                    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
                    mesh.visual.face_colors = [0, 255, 0, 128]  # Semi-transparent green
                    scene.add_geometry(mesh, node_name=f'surface_{i}')

            # Export the scene
            scene.export(file_path)
            
            self.status.setText(f"✅ Exported to {os.path.basename(file_path)}")
            
        except Exception as e:
            self.status.setText(f"❌ Export failed: {str(e)}")

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

    def start_vibration(self):
        if not self.vibration_timer.isActive():
            self.vibration_timer.start(50)  # ~20 FPS
            self.status.setText("🔊 Vibration started")
            self.sender().setText("Stop Vibration")

        else:
            self.vibration_timer.stop()
            self.status.setText("🔇 Vibration stopped")
            self.sender().setText("start Vibration")


    def stop_vibration(self):
        if self.vibration_timer.isActive():
            self.vibration_timer.stop()
            self.status.setText("🔇 Vibration stopped")

    def add_points_along_line(self):
        # Check if enough points are selected
        if len(self.selected_points) < 2:
            self.status.setText("❌ Select at least 2 points to define a line.")
            return

        pts = [self.points[i] for i in self.selected_points]

        # Check if points are collinear
        if not self.are_points_collinear(pts):
            self.status.setText("❌ Selected points are NOT in the same line.")
            return

        # Read n from input
        try:
            n = int(self.input_n.text())
            if n <= 0:
                raise ValueError
        except ValueError:
            self.status.setText("❌ Enter a valid positive integer for n.")
            return

        # Add n points along the line
        self.extend_points_along_line(pts, n)
        self.status.setText(f"✅ Added {n} points along the line.")
        self.update_plot()

    def are_points_collinear(self, pts):
        # At least 2 points needed
        if len(pts) <= 2:
            return True

        # Vector from first to second point
        p0 = pts[0]
        p1 = pts[1]
        v = [p1[i] - p0[i] for i in range(3)]

        # Check every other point lies on the line by verifying
        # that vector from p0 to pt is parallel to v
        for pt in pts[2:]:
            w = [pt[i] - p0[i] for i in range(3)]

            # Cross product of v and w should be zero vector if collinear
            cross = [
                v[1]*w[2] - v[2]*w[1],
                v[2]*w[0] - v[0]*w[2],
                v[0]*w[1] - v[1]*w[0]
            ]

            # If magnitude of cross product > small epsilon, not collinear
            if (cross[0]**2 + cross[1]**2 + cross[2]**2) > 1e-10:
                return False

        return True

    def extend_points_along_line(self, pts, n):
        # Use first two points to define line direction
        p0 = pts[0]
        p1 = pts[1]
        direction = [p1[i] - p0[i] for i in range(3)]

        # Normalize direction vector
        length = sum(d**2 for d in direction) ** 0.5
        if length == 0:
            return  # Avoid division by zero
        direction = [d / length for d in direction]

        # Find last point in the selected points along the line
        # We'll add points starting from the max projection point
        projections = [sum((pt[i] - p0[i]) * direction[i] for i in range(3)) for pt in pts]
        max_proj = max(projections)

        # Distance between two first points (step size)
        step = length

        # Add n points beyond max_proj in direction
        for i in range(1, n + 1):
            new_point = [p0[j] + (max_proj + i * step) * direction[j] for j in range(3)]
            self.points.append(new_point)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())