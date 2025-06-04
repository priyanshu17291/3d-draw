# python -m pip install -r requirements.txt
import sys
import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, 
    QWidget, QLabel, QHBoxLayout, QLineEdit, QFileDialog,
    QMenuBar, QAction, QMessageBox, QInputDialog, QListWidget,
    QSplitter, QGroupBox, QTextEdit
)
from PyQt5.QtCore import QTimer, Qt
import trimesh
import os
import json
import pickle
from datetime import datetime

class ProjectManager:
    """Handles project creation, saving, and loading."""
    
    def __init__(self):
        self.projects_dir = "projects"
        self.ensure_projects_directory()
    
    def ensure_projects_directory(self):
        """Create projects directory if it doesn't exist."""
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)
    
    def create_project(self, name, description=""):
        """Create a new project."""
        project_data = {
            'name': name,
            'description': description,
            'created_date': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat(),
            'points': [],
            'edges': [],
            'surfaces': [],
            'selected_points': []
        }
        return project_data
    
    def save_project(self, project_data, filename=None):
        """Save project to file."""
        if not filename:
            filename = f"{project_data['name']}.proj"
        
        filepath = os.path.join(self.projects_dir, filename)
        project_data['last_modified'] = datetime.now().isoformat()
        
        try:
            with open(filepath, 'w') as f:
                json.dump(project_data, f, indent=2)
            return True, filepath
        except Exception as e:
            return False, str(e)
    
    def load_project(self, filepath):
        """Load project from file."""
        try:
            with open(filepath, 'r') as f:
                project_data = json.load(f)
            return True, project_data
        except Exception as e:
            return False, str(e)
    
    def list_projects(self):
        """List all available projects."""
        projects = []
        for filename in os.listdir(self.projects_dir):
            if filename.endswith('.proj'):
                filepath = os.path.join(self.projects_dir, filename)
                success, project_data = self.load_project(filepath)
                if success:
                    project_data['filepath'] = filepath
                    projects.append(project_data)
        return projects
    
    def delete_project(self, filepath):
        """Delete a project file."""
        try:
            os.remove(filepath)
            return True
        except Exception as e:
            return False

class ProjectDialog(QWidget):
    """Dialog for project management."""
    
    def __init__(self, project_manager, parent=None):
        super().__init__()
        self.project_manager = project_manager
        self.parent_window = parent
        self.selected_project = None
        self.init_ui()
        self.load_projects()
    
    def init_ui(self):
        self.setWindowTitle("Project Manager")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        # Project list
        self.project_list = QListWidget()
        self.project_list.itemClicked.connect(self.on_project_selected)
        layout.addWidget(QLabel("Available Projects:"))
        layout.addWidget(self.project_list)
        
        # Project details
        details_group = QGroupBox("Project Details")
        details_layout = QVBoxLayout()
        
        self.name_label = QLabel("Name: ")
        self.description_label = QLabel("Description: ")
        self.created_label = QLabel("Created: ")
        self.modified_label = QLabel("Last Modified: ")
        
        details_layout.addWidget(self.name_label)
        details_layout.addWidget(self.description_label)
        details_layout.addWidget(self.created_label)
        details_layout.addWidget(self.modified_label)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        new_btn = QPushButton("New Project")
        new_btn.clicked.connect(self.new_project)
        button_layout.addWidget(new_btn)
        
        open_btn = QPushButton("Open Project")
        open_btn.clicked.connect(self.open_project)
        button_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("Delete Project")
        delete_btn.clicked.connect(self.delete_project)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_projects)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_projects(self):
        """Load and display available projects."""
        self.project_list.clear()
        projects = self.project_manager.list_projects()
        
        for project in projects:
            item_text = f"{project['name']} - {project['last_modified'][:10]}"
            self.project_list.addItem(item_text)
            # Store project data in item
            item = self.project_list.item(self.project_list.count() - 1)
            item.setData(Qt.UserRole, project)
    
    def on_project_selected(self, item):
        """Handle project selection."""
        project_data = item.data(Qt.UserRole)
        self.selected_project = project_data
        
        # Update details
        self.name_label.setText(f"Name: {project_data['name']}")
        self.description_label.setText(f"Description: {project_data.get('description', 'No description')}")
        self.created_label.setText(f"Created: {project_data['created_date'][:19]}")
        self.modified_label.setText(f"Last Modified: {project_data['last_modified'][:19]}")
    
    def new_project(self):
        """Create a new project."""
        name, ok = QInputDialog.getText(self, 'New Project', 'Enter project name:')
        if ok and name:
            description, ok = QInputDialog.getText(self, 'New Project', 'Enter project description (optional):')
            if ok:
                project_data = self.project_manager.create_project(name, description)
                success, filepath = self.project_manager.save_project(project_data)
                
                if success:
                    self.load_projects()
                    if self.parent_window:
                        self.parent_window.load_project_data(project_data)
                        self.parent_window.current_project = project_data
                        self.parent_window.current_project_file = filepath
                    QMessageBox.information(self, "Success", f"Project '{name}' created successfully!")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to create project: {filepath}")
    
    def open_project(self):
        """Open selected project."""
        if not self.selected_project:
            QMessageBox.warning(self, "Warning", "Please select a project to open.")
            return
        
        if self.parent_window:
            self.parent_window.load_project_data(self.selected_project)
            self.parent_window.current_project = self.selected_project
            self.parent_window.current_project_file = self.selected_project['filepath']
            self.close()
    
    def delete_project(self):
        """Delete selected project."""
        if not self.selected_project:
            QMessageBox.warning(self, "Warning", "Please select a project to delete.")
            return
        
        reply = QMessageBox.question(
            self, 'Confirm Delete', 
            f"Are you sure you want to delete project '{self.selected_project['name']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.project_manager.delete_project(self.selected_project['filepath']):
                QMessageBox.information(self, "Success", "Project deleted successfully!")
                self.load_projects()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete project.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive 3D Editor - PyVista + Qt")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize project management
        self.project_manager = ProjectManager()
        self.current_project = None
        self.current_project_file = None

        # Initialize data
        self.points = []
        self.edges = []
        self.selected_points = []
        self.surfaces = []

        # UI and 3D setup
        self.create_menu_bar()
        self.init_ui()

        # Animation setup
        self.surface_mesh = None
        self.surface_actor = None
        self.original_surface_points = None
        self.vibration_timer = QTimer()
        self.vibration_timer.timeout.connect(self.animate_surface)
        self.vibration_phase = 0.0

        # Show project manager on startup
        self.show_project_manager()

    def create_menu_bar(self):
        """Create menu bar with project management options."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Project', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open Project', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.show_project_manager)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save Project', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_current_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('Export to GLTF', self)
        export_action.triggered.connect(self.export_to_gltf)
        file_menu.addAction(export_action)

    def init_ui(self):
        """Create and lay out widgets."""
        self.frame = QWidget()
        self.layout = QHBoxLayout(self.frame)
        self.setCentralWidget(self.frame)

        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(splitter)

        # Plotter widget
        self.plotter = QtInteractor(self.frame)
        self.plotter.enable_terrain_style()
        self.plotter.add_axes(interactive=True)
        splitter.addWidget(self.plotter.interactor)

        # Right-side controls
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Project info
        project_group = QGroupBox("Current Project")
        project_layout = QVBoxLayout()
        self.project_info = QLabel("No project loaded")
        project_layout.addWidget(self.project_info)
        project_group.setLayout(project_layout)
        control_layout.addWidget(project_group)

        # Coordinate input fields
        coords_group = QGroupBox("Add Point")
        coords_layout = QVBoxLayout()
        self.input_fields = [QLineEdit() for _ in range(3)]
        for i, field in enumerate(self.input_fields):
            field.setPlaceholderText(f"Coord {['X', 'Y', 'Z'][i]}")
            coords_layout.addWidget(field)
        coords_group.setLayout(coords_layout)
        control_layout.addWidget(coords_group)

        # Buttons and their handlers
        buttons_group = QGroupBox("Tools")
        buttons_layout = QVBoxLayout()
        
        buttons = [
            ("Add Point", self.add_point),
            ("Connect Selected Points", self.connect_points),
            ("Generate Surface", self.generate_surface),
            ("Clear Selection", self.clear_selection),
            ("Clear All", self.clear_all),
            ("Test Select First Point", self.test_select_first_point),
        ]
        for label, handler in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            buttons_layout.addWidget(btn)
        
        buttons_group.setLayout(buttons_layout)
        control_layout.addWidget(buttons_group)

        # Animation controls
        animation_group = QGroupBox("Animation")
        animation_layout = QVBoxLayout()
        
        start_vibration_btn = QPushButton("Start Vibration")
        start_vibration_btn.clicked.connect(self.start_vibration)
        animation_layout.addWidget(start_vibration_btn)

        stop_vibration_btn = QPushButton("Stop Vibration")
        stop_vibration_btn.clicked.connect(self.stop_vibration)
        animation_layout.addWidget(stop_vibration_btn)
        
        animation_group.setLayout(animation_layout)
        control_layout.addWidget(animation_group)

        # Status label
        self.status = QLabel("Status: Ready")
        control_layout.addWidget(self.status)

        splitter.addWidget(control_widget)
        splitter.setSizes([800, 400])  # Set initial sizes

        # Enable point picking
        self.plotter.enable_point_picking(
            callback=self.pick_point,
            use_mesh=False,
            show_point=False,
            tolerance=0.15,
            left_clicking=True
        )

    def show_project_manager(self):
        """Show project manager dialog."""
        self.project_dialog = ProjectDialog(self.project_manager, self)
        self.project_dialog.show()

    def new_project(self):
        """Create a new project."""
        name, ok = QInputDialog.getText(self, 'New Project', 'Enter project name:')
        if ok and name:
            description, ok = QInputDialog.getText(self, 'New Project', 'Enter project description (optional):')
            if ok:
                # Check if current project needs saving
                if self.current_project and self.has_unsaved_changes():
                    reply = QMessageBox.question(
                        self, 'Unsaved Changes', 
                        'Current project has unsaved changes. Save before creating new project?',
                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                    )
                    if reply == QMessageBox.Yes:
                        self.save_current_project()
                    elif reply == QMessageBox.Cancel:
                        return
                
                # Create new project
                project_data = self.project_manager.create_project(name, description)
                success, filepath = self.project_manager.save_project(project_data)
                
                if success:
                    self.load_project_data(project_data)
                    self.current_project = project_data
                    self.current_project_file = filepath
                    QMessageBox.information(self, "Success", f"Project '{name}' created successfully!")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to create project: {filepath}")

    def save_current_project(self):
        """Save the current project."""
        if not self.current_project:
            QMessageBox.warning(self, "Warning", "No project loaded to save.")
            return
        
        # Update project data with current state
        self.current_project['points'] = self.points
        self.current_project['edges'] = self.edges
        self.current_project['selected_points'] = self.selected_points
        # Note: surfaces are not easily serializable, so we skip them for now
        
        success, result = self.project_manager.save_project(self.current_project)
        if success:
            self.status.setText("✅ Project saved successfully!")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save project: {result}")

    def save_project_as(self):
        """Save project with a new name."""
        if not self.current_project:
            QMessageBox.warning(self, "Warning", "No project loaded to save.")
            return
        
        name, ok = QInputDialog.getText(self, 'Save As', 'Enter new project name:')
        if ok and name:
            # Update project data
            self.current_project['name'] = name
            self.current_project['points'] = self.points
            self.current_project['edges'] = self.edges
            self.current_project['selected_points'] = self.selected_points
            
            success, filepath = self.project_manager.save_project(self.current_project, f"{name}.proj")
            if success:
                self.current_project_file = filepath
                self.update_project_info()
                self.status.setText("✅ Project saved successfully!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to save project: {filepath}")

    def load_project_data(self, project_data):
        """Load project data into the application."""
        self.points = project_data.get('points', [])
        self.edges = project_data.get('edges', [])
        self.selected_points = project_data.get('selected_points', [])
        self.surfaces = []  # Reset surfaces as they're not serialized
        
        self.update_project_info()
        self.update_plot()
        self.status.setText(f"✅ Loaded project: {project_data['name']}")

    def update_project_info(self):
        """Update project information display."""
        if self.current_project:
            info_text = f"Name: {self.current_project['name']}\n"
            info_text += f"Description: {self.current_project.get('description', 'No description')}\n"
            info_text += f"Points: {len(self.points)}, Edges: {len(self.edges)}, Surfaces: {len(self.surfaces)}"
            self.project_info.setText(info_text)
        else:
            self.project_info.setText("No project loaded")

    def has_unsaved_changes(self):
        """Check if there are unsaved changes."""
        if not self.current_project:
            return False
        
        return (self.points != self.current_project.get('points', []) or
                self.edges != self.current_project.get('edges', []) or
                self.selected_points != self.current_project.get('selected_points', []))

    # ... (rest of the methods remain the same as in the original code)
    def generate_surface(self):
        if len(self.selected_points) < 3:
            self.status.setText("❌ Select at least 3 points to generate a surface.")
            return

        pts = np.array([self.points[i] for i in self.selected_points])
        surface = pv.PolyData(pts).delaunay_2d()
        self.surfaces.append(surface)

        self.plotter.add_mesh(
            surface,
            color='lightgreen',
            opacity=0.6,
            name=f'surface_{len(self.surfaces)}',
            pickable=False
        )

        self.status.setText("✅ Surface generated.")
        self.selected_points.clear()
        self.update_plot(redraw_surfaces=False)
        self.update_project_info()

    def update_plot(self, redraw_surfaces=True):
        self.plotter.remove_actor("points_mesh", reset_camera=False)

        if not self.points:
            return

        mesh = pv.PolyData(np.array(self.points, dtype=np.float32))
        if self.edges:
            lines = np.array([[2, *edge] for edge in self.edges])
            mesh.lines = lines

        colors = np.array([
            [255, 0, 0] if i in self.selected_points else [0, 0, 255]
            for i in range(len(self.points))
        ])
        mesh["colors"] = colors

        self.plotter.add_mesh(
            mesh,
            scalars="colors",
            rgb=True,
            name="points_mesh",
            point_size=15,
            render_points_as_spheres=True,
            line_width=5
        )

        if redraw_surfaces and hasattr(self, "surfaces"):
            for i, surface in enumerate(self.surfaces):
                self.plotter.add_mesh(
                    surface,
                    color="lightgray",
                    opacity=0.6,
                    name=f"surface_{i}",
                    show_edges=True
                )

        self.plotter.reset_camera()

    def animate_surface(self):
        if not self.surfaces:
            return
        current_surface = self.surfaces[-1]
        amp = 0.1
        freq = 2.0
        t = self.vibration_phase
        points = current_surface.points.copy()

        phase_shift = np.linspace(0, 2 * np.pi, len(points))
        points[:, 2] += amp * np.sin(2 * np.pi * freq * t + phase_shift)

        current_surface.points = points
        self.surface_modified = True
        self.vibration_phase += 0.05
        self.plotter.update()

    def export_to_gltf(self):
        if not self.points and not self.surfaces:
            self.status.setText("❌ No geometry to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to GLTF", "scene.gltf", "GLTF Files (*.gltf);;All Files (*)"
        )
        
        if not file_path:
            return

        try:
            scene = trimesh.Scene()

            if self.points:
                for i, point in enumerate(self.points):
                    sphere = trimesh.creation.icosphere(subdivisions=1, radius=0.05)
                    sphere.apply_translation(point)
                    
                    if i in self.selected_points:
                        sphere.visual.face_colors = [255, 0, 0, 255]
                    else:
                        sphere.visual.face_colors = [0, 0, 255, 255]
                    
                    scene.add_geometry(sphere, node_name=f'point_{i}')

            if self.edges:
                for i, edge in enumerate(self.edges):
                    p1 = np.array(self.points[edge[0]])
                    p2 = np.array(self.points[edge[1]])
                    
                    direction = p2 - p1
                    length = np.linalg.norm(direction)
                    center = (p1 + p2) / 2
                    
                    if length > 0:
                        cylinder = trimesh.creation.cylinder(radius=0.02, height=length)
                        
                        if not np.allclose(direction, [0, 0, length]):
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
                        cylinder.visual.face_colors = [0, 255, 0, 255]
                        scene.add_geometry(cylinder, node_name=f'edge_{i}')

            if self.surfaces:
                for i, surface in enumerate(self.surfaces):
                    vertices = surface.points
                    faces = surface.faces.reshape(-1, 4)[:, 1:4]
                    
                    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
                    mesh.visual.face_colors = [0, 255, 0, 128]
                    scene.add_geometry(mesh, node_name=f'surface_{i}')

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
            self.update_project_info()
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
        self.update_project_info()

    def clear_selection(self):
        self.selected_points.clear()
        self.status.setText("Selection cleared")
        self.update_plot()

    def clear_all(self):
        self.points.clear()
        self.edges.clear()
        self.selected_points.clear()
        self.surfaces.clear()
        self.status.setText("All cleared")
        self.update_plot()
        self.update_project_info()

    def test_select_first_point(self):
        if self.points:
            self.selected_points = [0]
            self.status.setText("Selected point 0")
            self.update_plot()
        else:
            self.status.setText("No points to select")

    def start_vibration(self):
        if not self.vibration_timer.isActive():
            self.vibration_timer.start(50)
            self.status.setText("🔊 Vibration started")

    def stop_vibration(self):
        if self.vibration_timer.isActive():
            self.vibration_timer.stop()
            self.status.setText("🔇 Vibration stopped")

    def closeEvent(self, event):
        """Handle application close event."""
        if self.current_project and self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 'Unsaved Changes', 
                'Current project has unsaved changes. Save before closing?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Yes:
                self.save_current_project()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

#hello git test comment
#gahsdgdalsfg