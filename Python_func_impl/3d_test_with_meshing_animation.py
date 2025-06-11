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
import json
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QInputDialog, QScrollArea, QDialogButtonBox
from PyQt5.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel

class Sensor:
    def __init__(self, sensor_id, location, sensor_type=None, status="active"):
        self.id = sensor_id
        self.location = location  # [x, y, z]
        self.type = sensor_type
        self.status = status


class PointsInputDialog(QDialog):
    def __init__(self, num_points, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Points")
        self.input_fields = []

        # Scrollable widget setup
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        form_layout = QVBoxLayout(container)

        # Add coordinate input fields
        for i in range(num_points):
            coord_layout = QHBoxLayout()
            x_input = QLineEdit()
            y_input = QLineEdit()
            z_input = QLineEdit()
            x_input.setPlaceholderText(f"X{i+1}")
            y_input.setPlaceholderText(f"Y{i+1}")
            z_input.setPlaceholderText(f"Z{i+1}")
            coord_layout.addWidget(QLabel(f"Point {i+1}:"))
            coord_layout.addWidget(x_input)
            coord_layout.addWidget(y_input)
            coord_layout.addWidget(z_input)
            form_layout.addLayout(coord_layout)
            self.input_fields.append((x_input, y_input, z_input))

        scroll.setWidget(container)

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Final layout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        layout.addWidget(button_box)

    def get_points(self):
        points = []
        try:
            for x_input, y_input, z_input in self.input_fields:
                x = float(x_input.text())
                y = float(y_input.text())
                z = float(z_input.text())
                points.append([x, y, z])
            return points
        except ValueError:
            return None

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
        self.surfaces_stores = []  # Store original surface points for animation
        self.sensors = []  # List to store Sensor objects

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

        #directory tracing
        self.current_file_path = None



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
            ("Open File", self.open_file_dialog),
            ("Save", self.save),
            ("Save As", self.save_as),
            ("Add Point", self.add_point),
            ("Connect Selected Points", self.connect_points),
            ("Generate Surface", self.generate_surface),
            ("Clear Selection", self.clear_selection),
            ("Clear All", self.clear_all),
            ("Test Select First Point", self.test_select_first_point),
            ("Export to GLTF", self.export_to_gltf),
            ("Add Points Along Line", self.add_points_along_line),  # NEW button added here
            ("Add Multiple Points", self.ask_number_of_points),
            ("Show Active Elements", self.show_active_elements_panel),  # <-- Add the button here!
            ("Add Sensor", self.add_sensor),  # Add sensor button
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

    
    def open_points_input_dialog(self, num_points):
        dialog = PointsInputDialog(num_points, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            points = dialog.get_points()
            if points is None:
                self.status.setText("Invalid coordinates entered.")
                return
            # Add points to your structure
            self.points.extend(points)
            self.update_plot()
            self.status.setText(f"Added {len(points)} points.")

    def add_sensor(self):
        try:
            coords = [float(f.text()) for f in self.input_fields]
            self.sensors.append(coords)

            for f in self.input_fields:
                f.clear()

            self.status.setText(f"✅ Added Sensor at {coords}")
            self.update_plot()

        except ValueError:
            self.status.setText("❌ Enter valid X, Y, Z coordinates")


    def show_active_elements_panel(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel

        dialog = QDialog(self)
        dialog.setWindowTitle("Active Elements")
        dialog.resize(400, 700)
        layout = QVBoxLayout(dialog)

        points_list = QListWidget()
        lines_list = QListWidget()
        surfaces_list = QListWidget()
        sensors_list = QListWidget()  # New: Sensor list widget

        layout.addWidget(QLabel("Points"))
        layout.addWidget(points_list)
        layout.addWidget(QLabel("Lines"))
        layout.addWidget(lines_list)
        layout.addWidget(QLabel("Surfaces"))
        layout.addWidget(surfaces_list)
        layout.addWidget(QLabel("Sensors"))  # New: Sensor label
        layout.addWidget(sensors_list)

        # Populate all lists
        for idx, point in enumerate(self.points):
            points_list.addItem(f"Point {idx}: {point}")

        for idx, edge in enumerate(self.edges):
            lines_list.addItem(f"Line {idx}: {edge}")

        for idx, surface in enumerate(self.surfaces_stores):
            surfaces_list.addItem(f"Surface {idx}: {len(surface)} points")

        for idx, sensor in enumerate(self.sensors):  # New: Add sensors
            sensors_list.addItem(f"Sensor {idx}: {sensor}")

        # Optional: connect signals to highlight functions
        points_list.currentRowChanged.connect(self.highlight_point)
        lines_list.currentRowChanged.connect(self.highlight_line)
        surfaces_list.currentRowChanged.connect(self.highlight_surface)
        sensors_list.currentRowChanged.connect(self.highlight_sensor)  # New

        dialog.exec_()



    def highlight_element_from_tree(self, item, column):
        element_type, index = item.data(0, Qt.UserRole)
        self.plotter.clear()  # Clear previous highlights

        if element_type == "point":
            point = self.points[index]
            self.plotter.add_mesh(pv.Sphere(center=point, radius=0.2), color='red', name="highlight_point")
            self.status.setText(f"🔵 Highlighted Point {index}: {point}")

        elif element_type == "edge":
            pt1 = self.points[self.edges[index][0]]
            pt2 = self.points[self.edges[index][1]]
            line = pv.Line(pt1, pt2)
            self.plotter.add_mesh(line, color='blue', line_width=5, name="highlight_edge")
            self.status.setText(f"🟢 Highlighted Edge {index}: {pt1} -> {pt2}")

        elif element_type == "surface":
            pts = np.array(self.surfaces_stores[index])
            surface = pv.PolyData(pts).delaunay_2d()
            self.plotter.add_mesh(surface, color='green', opacity=0.7, name="highlight_surface")
            self.status.setText(f"🟡 Highlighted Surface {index} with {len(pts)} points")

        self.update_plot(redraw_surfaces=False)

    def highlight_sensor(self, idx):
        self.clear_highlights()
        if idx < 0 or idx >= len(self.sensors):
            return

        # Simulate selection by tracking selected sensor index
        self.selected_sensor = idx  # You need to define this in __init__

        self.status.setText(f"Selected Sensor {idx}: {self.sensors[idx]}")
        self.update_plot()  # Will trigger color update based on selected_sensor


    def ask_number_of_points(self):
        num, ok = QInputDialog.getInt(self, "Number of points", "Enter number of points:", min=1, max=100)
        if ok:
            self.open_points_input_dialog(num)

    def save_structure(self, file_path):
        if not file_path.endswith('.json'):
            file_path += '.json'

        try:
            surfaces = [
                [[int(coord) for coord in point] for point in surface]
                for surface in self.surfaces_stores
            ]

            structure_data = {
                "points": self.points,
                "edges": self.edges,
                "surfaces": surfaces,
                "meta": {
                    "created_by": "Dhruv",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "filename": os.path.basename(file_path)
                }
            }

            with open(file_path, 'w') as f:
                json.dump(structure_data, f, indent=2)

            self.current_file_path = file_path
            self.status.setText(f"Saved to {file_path}")
        except Exception as e:
            self.status.setText(f"Failed to save: {e}")


    def show_active_elements_panel(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Active Elements")
        dialog.resize(400, 700)
        layout = QVBoxLayout(dialog)

        points_list = QListWidget()
        lines_list = QListWidget()
        surfaces_list = QListWidget()
        sensors_list = QListWidget()  # New: Sensor list widget

        layout.addWidget(QLabel("Points"))
        layout.addWidget(points_list)
        layout.addWidget(QLabel("Lines"))
        layout.addWidget(lines_list)
        layout.addWidget(QLabel("Surfaces"))
        layout.addWidget(surfaces_list)
        layout.addWidget(QLabel("Sensors"))  # New: Sensor label
        layout.addWidget(sensors_list)

        # Populate all lists
        for idx, point in enumerate(self.points):
            points_list.addItem(f"Point {idx}: {point}")

        for idx, edge in enumerate(self.edges):
            lines_list.addItem(f"Line {idx}: {edge}")

        for idx, surface in enumerate(self.surfaces_stores):
            surfaces_list.addItem(f"Surface {idx}: {len(surface)} points")

        for idx, sensor in enumerate(self.sensors):  # New: Add sensors
            sensors_list.addItem(f"Sensor {idx}: {sensor}")

        # Optional: connect signals to highlight functions
        points_list.currentRowChanged.connect(self.highlight_point)
        lines_list.currentRowChanged.connect(self.highlight_line)
        surfaces_list.currentRowChanged.connect(self.highlight_surface)
        sensors_list.currentRowChanged.connect(self.highlight_sensor)  # New

        dialog.exec_()


    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            if not file_path.endswith(".json"):
                file_path += ".json"
            self.save_structure(file_path)
        else:
            self.status.setText("Save file cancelled.")
    
    def save(self):
        if self.current_file_path:
            self.save_structure(self.current_file_path)
        else:
            self.save_as()


    def load_structure_from_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self.points = data["points"]
            self.edges = data["edges"]
            self.surfaces = []  # clear current surfaces
            self.surfaces_stores = []
            self.current_file_path = file_path

            self.loaded_mesh = None  # No mesh; reconstructing

            self.plotter.clear()

            # For each stored surface (array of points), generate surface mesh
            for surface_points in data.get("surfaces", []):
                self.generate_surface_from_points(surface_points)

            self.update_plot()

            self.status.setText(f"Loaded structure from JSON: {file_path}")
        except Exception as e:
            self.status.setText(f"Failed to load JSON: {e}")

    
    def generate_surface_from_points(self, points):
        pts = np.array(points)
        self.surfaces_stores.append(pts.copy())

        surface = pv.PolyData(pts).delaunay_2d()
        surface = surface.subdivide(nsub=3, subfilter="linear")
        surface = surface.smooth(n_iter=100, relaxation_factor=0.1)
        self.surfaces.append(surface)

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


    def generate_surface(self):
        if len(self.selected_points) < 3:
            self.status.setText("❌ Select at least 3 points to generate a surface.")
            return

        points = [self.points[i] for i in self.selected_points]
        self.generate_surface_from_points(points)
        self.status.setText("✅ Surface generated.")
        self.selected_points.clear()
        self.update_plot(redraw_surfaces=False)



    def update_plot(self, redraw_surfaces=True):
        """Refresh 3D scene, optionally skipping surface re-addition."""

        # Remove old meshes
        self.plotter.remove_actor("points_mesh", reset_camera=False)
        self.plotter.remove_actor("sensors_mesh", reset_camera=False)  # <--- REMOVE sensor actors

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

        # === Draw sensors (as regular points) ===
        if self.sensors:
            sensor_coords = np.array(self.sensors, dtype=np.float32)
            sensor_mesh = pv.PolyData(sensor_coords)

            sensor_colors = np.array([
                [0, 0, 255] if i == getattr(self, "selected_sensor", -1) else [0, 255, 0]
                for i in range(len(self.sensors))
            ])
            sensor_mesh["colors"] = sensor_colors

            self.plotter.add_mesh(
                sensor_mesh,
                scalars="colors",
                rgb=True,
                name="sensor_mesh",
                point_size=15,
                render_points_as_spheres=True
    )


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

        # ✅ NEW: Plot sensors if any
        if hasattr(self, "sensors") and self.sensors:
            sensor_mesh = pv.PolyData(np.array(self.sensors, dtype=np.float32))
            self.plotter.add_mesh(
                sensor_mesh,
                color="green",
                point_size=15,
                render_points_as_spheres=True,
                name="sensors_mesh"
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

        # Reset camera to include all points
        self.plotter.reset_camera()


    def clear_highlights(self):
        # Clear selections
        self.selected_points.clear()
        self.selected_sensor = -1  # Deselect any highlighted sensor

        # Remove highlight actors
        for name in ['highlight_point', 'highlight_line', 'highlight_surface', 'highlight_sensor']:
            try:
                self.plotter.remove_actor(name)
            except Exception:
                pass


    def highlight_point(self, idx):
        self.clear_highlights()
        if idx < 0 or idx >= len(self.points):
            return
        # Use a single point mesh with larger point size and red color
        mesh = pv.PolyData([self.points[idx]])
        colors = np.array([[255, 0, 0]])  # red
        mesh["colors"] = colors
        self.plotter.add_mesh(
            mesh,
            scalars="colors",
            rgb=True,
            name="highlight_point",
            point_size=15,  # same size as normal points
            render_points_as_spheres=True,
        )
        self.status.setText(f"Selected Point {idx}: {self.points[idx]}")
        self.plotter.render()


    def highlight_line(self, idx):
        self.clear_highlights()
        if idx < 0 or idx >= len(self.edges):
            return
        p1_idx, p2_idx = self.edges[idx]
        p1 = self.points[p1_idx]
        p2 = self.points[p2_idx]
        line = pv.Line(p1, p2)
        self.plotter.add_mesh(line, color='red', line_width=5, name='highlight_line')
        self.status.setText(f"Selected Line {idx}: Points {p1_idx} to {p2_idx}")
        self.plotter.render()

    def highlight_surface(self, idx):
        self.clear_highlights()
        if idx < 0 or idx >= len(self.surfaces_stores):
            return
        surface_points = np.array(self.surfaces_stores[idx], dtype=np.float32)
        if len(surface_points) < 3:
            # Can't create surface mesh with fewer than 3 points, just highlight points instead
            for pt in surface_points:
                sphere = pv.Sphere(center=pt, radius=0.1)
                self.plotter.add_mesh(sphere, color='orange', name='highlight_surface')
        else:
            surface = pv.PolyData(surface_points).delaunay_2d()
            self.plotter.add_mesh(surface, color='orange', opacity=0.6, name='highlight_surface', show_edges=True)
        point_indices = ", ".join(str(i) for i in range(len(surface_points)))   
        self.status.setText(f"Selected Surface {idx}: Points indices [{point_indices}]")
        self.plotter.render()



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

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Mesh Files (*.vtk *.ply *.obj *.stl *.gltf *.glb);;All Files (*)"
        )
        if file_path:
            self.load_structure_from_json(file_path)
            self.status.setText(f"Loaded file: {file_path}")
        else:
            self.status.setText("Open file cancelled.")


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
        self.surfaces.clear()
        self.surfaces_stores.clear()
        self.plotter.clear()
        self.plotter.reset_camera()
        self.loaded_mesh = None
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