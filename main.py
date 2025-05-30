# import sys
# import json
# import os
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
#                             QLabel, QLineEdit, QPushButton, QColorDialog, QGroupBox, QGridLayout,
#                             QSpinBox, QDoubleSpinBox, QFileDialog)
# from PyQt5.QtCore import Qt, QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtGui import QColor

# class ModelingTool(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("3D Model Drawing Tool")
#         self.setGeometry(100, 100, 1200, 800)
        
#         # Store all objects in a list for exporting
#         self.objects = []
#         self.object_counter = 0
        
#         # Setup main layout
#         self.main_widget = QWidget()
#         self.setCentralWidget(self.main_widget)
#         self.main_layout = QHBoxLayout(self.main_widget)
        
#         # Left panel - Controls
#         self.controls_panel = QWidget()
#         self.controls_layout = QVBoxLayout(self.controls_panel)
        
#         # Create control groups
#         self.create_vertical_beam_controls()
#         self.create_horizontal_beam_controls()
#         self.create_sphere_controls()
#         self.create_export_controls()
        
#         self.main_layout.addWidget(self.controls_panel, 1)
        
#         # Right panel - 3D view
#         self.view_panel = QWebEngineView()
#         self.init_three_js_view()
#         self.main_layout.addWidget(self.view_panel, 2)
    
#     def create_vertical_beam_controls(self):
#         group_box = QGroupBox("Add Vertical Beam (Z axis)")
#         layout = QGridLayout()
        
#         # Radius
#         layout.addWidget(QLabel("Radius:"), 0, 0)
#         self.vert_radius = QDoubleSpinBox()
#         self.vert_radius.setRange(0.1, 100.0)
#         self.vert_radius.setValue(1.0)
#         self.vert_radius.setSingleStep(0.1)
#         layout.addWidget(self.vert_radius, 0, 1)
        
#         # Length
#         layout.addWidget(QLabel("Length:"), 1, 0)
#         self.vert_length = QDoubleSpinBox()
#         self.vert_length.setRange(0.1, 1000.0)
#         self.vert_length.setValue(10.0)
#         self.vert_length.setSingleStep(0.1)
#         layout.addWidget(self.vert_length, 1, 1)
        
#         # Color
#         layout.addWidget(QLabel("Color:"), 2, 0)
#         self.vert_color_btn = QPushButton()
#         self.vert_color_btn.setStyleSheet("background-color: #ff0000")
#         self.vert_color = "#ff0000"
#         self.vert_color_btn.clicked.connect(lambda: self.select_color("vert"))
#         layout.addWidget(self.vert_color_btn, 2, 1)
        
#         # Position
#         layout.addWidget(QLabel("Position X:"), 3, 0)
#         self.vert_pos_x = QDoubleSpinBox()
#         self.vert_pos_x.setRange(-1000.0, 1000.0)
#         self.vert_pos_x.setValue(0.0)
#         self.vert_pos_x.setSingleStep(0.5)
#         layout.addWidget(self.vert_pos_x, 3, 1)
        
#         layout.addWidget(QLabel("Position Y:"), 4, 0)
#         self.vert_pos_y = QDoubleSpinBox()
#         self.vert_pos_y.setRange(-1000.0, 1000.0)
#         self.vert_pos_y.setValue(0.0)
#         self.vert_pos_y.setSingleStep(0.5)
#         layout.addWidget(self.vert_pos_y, 4, 1)
        
#         layout.addWidget(QLabel("Position Z:"), 5, 0)
#         self.vert_pos_z = QDoubleSpinBox()
#         self.vert_pos_z.setRange(-1000.0, 1000.0)
#         self.vert_pos_z.setValue(0.0)
#         self.vert_pos_z.setSingleStep(0.5)
#         layout.addWidget(self.vert_pos_z, 5, 1)
        
#         # Rotation
#         layout.addWidget(QLabel("Rotate X (deg):"), 6, 0)
#         self.vert_rot_x = QDoubleSpinBox()
#         self.vert_rot_x.setRange(-180.0, 180.0)
#         self.vert_rot_x.setValue(0.0)
#         self.vert_rot_x.setSingleStep(5.0)
#         layout.addWidget(self.vert_rot_x, 6, 1)
        
#         layout.addWidget(QLabel("Rotate Y (deg):"), 7, 0)
#         self.vert_rot_y = QDoubleSpinBox()
#         self.vert_rot_y.setRange(-180.0, 180.0)
#         self.vert_rot_y.setValue(0.0)
#         self.vert_rot_y.setSingleStep(5.0)
#         layout.addWidget(self.vert_rot_y, 7, 1)
        
#         # Add Button
#         self.add_vert_beam_btn = QPushButton("Add Vertical Beam")
#         self.add_vert_beam_btn.clicked.connect(self.add_vertical_beam)
#         layout.addWidget(self.add_vert_beam_btn, 8, 0, 1, 2)
        
#         group_box.setLayout(layout)
#         self.controls_layout.addWidget(group_box)
    
#     def create_horizontal_beam_controls(self):
#         group_box = QGroupBox("Add Horizontal Beam (X axis)")
#         layout = QGridLayout()
        
#         # Radius
#         layout.addWidget(QLabel("Radius:"), 0, 0)
#         self.horz_radius = QDoubleSpinBox()
#         self.horz_radius.setRange(0.1, 100.0)
#         self.horz_radius.setValue(1.0)
#         self.horz_radius.setSingleStep(0.1)
#         layout.addWidget(self.horz_radius, 0, 1)
        
#         # Length
#         layout.addWidget(QLabel("Length:"), 1, 0)
#         self.horz_length = QDoubleSpinBox()
#         self.horz_length.setRange(0.1, 100.0)
#         self.horz_length.setValue(10.0)
#         self.horz_length.setSingleStep(0.1)
#         layout.addWidget(self.horz_length, 1, 1)
        
#         # Color
#         layout.addWidget(QLabel("Color:"), 2, 0)
#         self.horz_color_btn = QPushButton()
#         self.horz_color_btn.setStyleSheet("background-color: #00ff00")
#         self.horz_color = "#00ff00"
#         self.horz_color_btn.clicked.connect(lambda: self.select_color("horz"))
#         layout.addWidget(self.horz_color_btn, 2, 1)
        
#         # Position
#         layout.addWidget(QLabel("Position X:"), 3, 0)
#         self.horz_pos_x = QDoubleSpinBox()
#         self.horz_pos_x.setRange(-100.0, 100.0)
#         self.horz_pos_x.setValue(0.0)
#         self.horz_pos_x.setSingleStep(0.5)
#         layout.addWidget(self.horz_pos_x, 3, 1)
        
#         layout.addWidget(QLabel("Position Y:"), 4, 0)
#         self.horz_pos_y = QDoubleSpinBox()
#         self.horz_pos_y.setRange(-100.0, 100.0)
#         self.horz_pos_y.setValue(0.0)
#         self.horz_pos_y.setSingleStep(0.5)
#         layout.addWidget(self.horz_pos_y, 4, 1)
        
#         layout.addWidget(QLabel("Position Z:"), 5, 0)
#         self.horz_pos_z = QDoubleSpinBox()
#         self.horz_pos_z.setRange(-100.0, 100.0)
#         self.horz_pos_z.setValue(0.0)
#         self.horz_pos_z.setSingleStep(0.5)
#         layout.addWidget(self.horz_pos_z, 5, 1)
        
#         # Rotation
#         layout.addWidget(QLabel("Rotate Y (deg):"), 6, 0)
#         self.horz_rot_y = QDoubleSpinBox()
#         self.horz_rot_y.setRange(-180.0, 180.0)
#         self.horz_rot_y.setValue(0.0)
#         self.horz_rot_y.setSingleStep(5.0)
#         layout.addWidget(self.horz_rot_y, 6, 1)
        
#         layout.addWidget(QLabel("Rotate Z (deg):"), 7, 0)
#         self.horz_rot_z = QDoubleSpinBox()
#         self.horz_rot_z.setRange(-180.0, 180.0)
#         self.horz_rot_z.setValue(0.0)
#         self.horz_rot_z.setSingleStep(5.0)
#         layout.addWidget(self.horz_rot_z, 7, 1)
        
#         # Add Button
#         self.add_horz_beam_btn = QPushButton("Add Horizontal Beam")
#         self.add_horz_beam_btn.clicked.connect(self.add_horizontal_beam)
#         layout.addWidget(self.add_horz_beam_btn, 8, 0, 1, 2)
        
#         group_box.setLayout(layout)
#         self.controls_layout.addWidget(group_box)
    
#     def create_sphere_controls(self):
#         group_box = QGroupBox("Add Sphere")
#         layout = QGridLayout()
        
#         # Radius
#         layout.addWidget(QLabel("Radius:"), 0, 0)
#         self.sphere_radius = QDoubleSpinBox()
#         self.sphere_radius.setRange(0.1, 100.0)
#         self.sphere_radius.setValue(2.0)
#         self.sphere_radius.setSingleStep(0.1)
#         layout.addWidget(self.sphere_radius, 0, 1)
        
#         # Color
#         layout.addWidget(QLabel("Color:"), 1, 0)
#         self.sphere_color_btn = QPushButton()
#         self.sphere_color_btn.setStyleSheet("background-color: #0000ff")
#         self.sphere_color = "#0000ff"
#         self.sphere_color_btn.clicked.connect(lambda: self.select_color("sphere"))
#         layout.addWidget(self.sphere_color_btn, 1, 1)
        
#         # Position
#         layout.addWidget(QLabel("Position X:"), 2, 0)
#         self.sphere_pos_x = QDoubleSpinBox()
#         self.sphere_pos_x.setRange(-100.0, 100.0)
#         self.sphere_pos_x.setValue(0.0)
#         self.sphere_pos_x.setSingleStep(0.5)
#         layout.addWidget(self.sphere_pos_x, 2, 1)
        
#         layout.addWidget(QLabel("Position Y:"), 3, 0)
#         self.sphere_pos_y = QDoubleSpinBox()
#         self.sphere_pos_y.setRange(-100.0, 100.0)
#         self.sphere_pos_y.setValue(0.0)
#         self.sphere_pos_y.setSingleStep(0.5)
#         layout.addWidget(self.sphere_pos_y, 3, 1)
        
#         layout.addWidget(QLabel("Position Z:"), 4, 0)
#         self.sphere_pos_z = QDoubleSpinBox()
#         self.sphere_pos_z.setRange(-100.0, 100.0)
#         self.sphere_pos_z.setValue(0.0)
#         self.sphere_pos_z.setSingleStep(0.5)
#         layout.addWidget(self.sphere_pos_z, 4, 1)
        
#         # Add Button
#         self.add_sphere_btn = QPushButton("Add Sphere")
#         self.add_sphere_btn.clicked.connect(self.add_sphere)
#         layout.addWidget(self.add_sphere_btn, 5, 0, 1, 2)
        
#         group_box.setLayout(layout)
#         self.controls_layout.addWidget(group_box)
    
#     def create_export_controls(self):
#         group_box = QGroupBox("Export")
#         layout = QVBoxLayout()
        
#         self.export_btn = QPushButton("Export 3D Model as HTML")
#         self.export_btn.clicked.connect(self.export_model)
#         layout.addWidget(self.export_btn)
        
#         group_box.setLayout(layout)
#         self.controls_layout.addWidget(group_box)
    
#     def select_color(self, element_type):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             hex_color = color.name()
#             if element_type == "vert":
#                 self.vert_color = hex_color
#                 self.vert_color_btn.setStyleSheet(f"background-color: {hex_color}")
#             elif element_type == "horz":
#                 self.horz_color = hex_color
#                 self.horz_color_btn.setStyleSheet(f"background-color: {hex_color}")
#             elif element_type == "sphere":
#                 self.sphere_color = hex_color
#                 self.sphere_color_btn.setStyleSheet(f"background-color: {hex_color}")
    
#     def init_three_js_view(self):
#         # Create HTML with embedded Three.js
#         html_content = self.get_threejs_html()
        
#         # Create a temporary file with the HTML content
#         temp_file = "temp_threejs_view.html"
#         with open(temp_file, "w") as f:
#             f.write(html_content)
        
#         # Load the HTML file into the QWebEngineView
#         self.view_panel.load(QUrl.fromLocalFile(os.path.abspath(temp_file)))
    
#     def add_vertical_beam(self):
#         # Get values from inputs
#         radius = self.vert_radius.value()
#         length = self.vert_length.value()
#         color = self.vert_color
#         pos_x = self.vert_pos_x.value()
#         pos_y = self.vert_pos_y.value()
#         pos_z = self.vert_pos_z.value()
#         rot_x = self.vert_rot_x.value()
#         rot_y = self.vert_rot_y.value()
        
#         # Create object data
#         obj_id = f"obj_{self.object_counter}"
#         self.object_counter += 1
        
#         obj_data = {
#             "id": obj_id,
#             "type": "vertical_beam",
#             "radius": radius,
#             "length": length,
#             "color": color,
#             "position": [pos_x, pos_y, pos_z],
#             "rotation": [rot_x, rot_y, 0]
#         }
        
#         self.objects.append(obj_data)
#         self.update_threejs_view()
    
#     def add_horizontal_beam(self):
#         # Get values from inputs
#         radius = self.horz_radius.value()
#         length = self.horz_length.value()
#         color = self.horz_color
#         pos_x = self.horz_pos_x.value()
#         pos_y = self.horz_pos_y.value()
#         pos_z = self.horz_pos_z.value()
#         rot_y = self.horz_rot_y.value()
#         rot_z = self.horz_rot_z.value()
        
#         # Create object data
#         obj_id = f"obj_{self.object_counter}"
#         self.object_counter += 1
        
#         obj_data = {
#             "id": obj_id,
#             "type": "horizontal_beam",
#             "radius": radius,
#             "length": length,
#             "color": color,
#             "position": [pos_x, pos_y, pos_z],
#             "rotation": [0, rot_y, rot_z]
#         }
        
#         self.objects.append(obj_data)
#         self.update_threejs_view()
    
#     def add_sphere(self):
#         # Get values from inputs
#         radius = self.sphere_radius.value()
#         color = self.sphere_color
#         pos_x = self.sphere_pos_x.value()
#         pos_y = self.sphere_pos_y.value()
#         pos_z = self.sphere_pos_z.value()
        
#         # Create object data
#         obj_id = f"obj_{self.object_counter}"
#         self.object_counter += 1
        
#         obj_data = {
#             "id": obj_id,
#             "type": "sphere",
#             "radius": radius,
#             "color": color,
#             "position": [pos_x, pos_y, pos_z]
#         }
        
#         self.objects.append(obj_data)
#         self.update_threejs_view()
    
#     def update_threejs_view(self):
#         # Generate updated HTML with current objects
#         html_content = self.get_threejs_html()
        
#         # Update the temporary file
#         temp_file = "temp_threejs_view.html"
#         with open(temp_file, "w") as f:
#             f.write(html_content)
        
#         # Reload the view
#         self.view_panel.load(QUrl.fromLocalFile(os.path.abspath(temp_file)))
    
#     def export_model(self):
#         # Ask for file location to save
#         file_path, _ = QFileDialog.getSaveFileName(self, "Save 3D Model", "", "HTML Files (*.html)")
        
#         if file_path:
#             # Generate HTML with the export flag set to True
#             html_content = self.get_threejs_html(is_export=True)
            
#             # Save to file
#             with open(file_path, "w") as f:
#                 f.write(html_content)
    
#     def get_threejs_html(self, is_export=False):
#         # Convert objects to JSON
#         objects_json = json.dumps(self.objects)
        
#         # Create HTML with Three.js
#         html = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="utf-8">
#             <title>3D Model Viewer</title>
#             <style>
#                 body {{ margin: 0; overflow: hidden; }}
#                 canvas {{ width: 100%; height: 100%; display: block; }}
#                 #isometric-view-btn {{
#                     position: absolute;
#                     bottom: 20px;
#                     right: 20px;
#                     z-index: 100;
#                     padding: 10px;
#                     background-color: rgba(0, 0, 0, 0.5);
#                     color: white;
#                     border: none;
#                     border-radius: 5px;
#                     cursor: pointer;
#                 }}
#             </style>
#             <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
#             <script src="https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.7/dat.gui.min.js"></script>
#             <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.min.js"></script>
#         </head>
#         <body>
#             <button id="isometric-view-btn">Set Isometric View</button>
#             <script>
#                 const objects = {objects_json};
                
#                 // Scene setup
#                 const scene = new THREE.Scene();
#                 scene.background = new THREE.Color(0xf0f0f0);
                
#                 // Camera setup
#                 const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
#                 camera.position.set(30, 30, 30);
#                 camera.lookAt(0, 0, 0);
                
#                 // Renderer setup
#                 const renderer = new THREE.WebGLRenderer({{ antialias: true }});
#                 renderer.setSize(window.innerWidth, window.innerHeight);
#                 document.body.appendChild(renderer.domElement);
                
#                 // Controls setup
#                 const controls = new THREE.OrbitControls(camera, renderer.domElement);
#                 controls.enableDamping = true;
#                 controls.dampingFactor = 0.25;
                
#                 // Grid helper
#                 const gridHelper = new THREE.GridHelper(50, 50);
#                 scene.add(gridHelper);
                
#                 // Axes helper
#                 const axesHelper = new THREE.AxesHelper(20);
#                 scene.add(axesHelper);
                
#                 // Add ambient light
#                 const ambientLight = new THREE.AmbientLight(0x404040);
#                 scene.add(ambientLight);
                
#                 // Add directional light
#                 const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
#                 directionalLight.position.set(1, 1, 1);
#                 scene.add(directionalLight);
                
#                 // Create all objects
#                 function createObjects() {{
#                     // Remove all existing objects (except grid and axes)
#                     scene.children.forEach(child => {{
#                         if (!(child instanceof THREE.GridHelper) && 
#                             !(child instanceof THREE.AxesHelper) &&
#                             !(child instanceof THREE.Light)) {{
#                             scene.remove(child);
#                         }}
#                     }});
                    
#                     // Add new objects
#                     objects.forEach(obj => {{
#                         if (obj.type === 'vertical_beam') {{
#                             createCylinder(
#                                 obj.id,
#                                 obj.radius, 
#                                 obj.length, 
#                                 obj.color, 
#                                 obj.position,
#                                 obj.rotation,
#                                 [0, 0, 1]  // Align with Z axis
#                             );
#                         }} else if (obj.type === 'horizontal_beam') {{
#                             createCylinder(
#                                 obj.id,
#                                 obj.radius, 
#                                 obj.length, 
#                                 obj.color, 
#                                 obj.position,
#                                 obj.rotation,
#                                 [1, 0, 0]  // Align with X axis
#                             );
#                         }} else if (obj.type === 'sphere') {{
#                             createSphere(
#                                 obj.id,
#                                 obj.radius,
#                                 obj.color,
#                                 obj.position
#                             );
#                         }}
#                     }});
#                 }}
                
#                 function createCylinder(id, radius, length, color, position, rotation, axis) {{
#                     const geometry = new THREE.CylinderGeometry(radius, radius, length, 32);
#                     const material = new THREE.MeshPhongMaterial({{ color: color }});
#                     const cylinder = new THREE.Mesh(geometry, material);
                    
#                     // Set name/id
#                     cylinder.name = id;
                    
#                     // Rotate cylinder to align with specified axis
#                     if (axis[0] === 1) {{  // X axis
#                         cylinder.rotation.z = Math.PI / 2;
#                     }} else if (axis[1] === 1) {{  // Y axis
#                         cylinder.rotation.x = Math.PI / 2;
#                     }}
                    
#                     // Apply additional rotation
#                     const rotRad = rotation.map(deg => deg * Math.PI / 180);
#                     cylinder.rotateX(rotRad[0]);
#                     cylinder.rotateY(rotRad[1]);
#                     cylinder.rotateZ(rotRad[2]);
                    
#                     // Set position
#                     cylinder.position.set(position[0], position[1], position[2]);
                    
#                     scene.add(cylinder);
#                 }}
                
#                 function createSphere(id, radius, color, position) {{
#                     const geometry = new THREE.SphereGeometry(radius, 32, 32);
#                     const material = new THREE.MeshPhongMaterial({{ color: color }});
#                     const sphere = new THREE.Mesh(geometry, material);
                    
#                     // Set name/id
#                     sphere.name = id;
                    
#                     // Set position
#                     sphere.position.set(position[0], position[1], position[2]);
                    
#                     scene.add(sphere);
#                 }}
                
#                 // Set isometric view
#                 document.getElementById('isometric-view-btn').addEventListener('click', function() {{
#                     camera.position.set(20, 20, 20);
#                     camera.lookAt(0, 0, 0);
#                     controls.update();
#                 }});
                
#                 // Handle window resize
#                 window.addEventListener('resize', function() {{
#                     camera.aspect = window.innerWidth / window.innerHeight;
#                     camera.updateProjectionMatrix();
#                     renderer.setSize(window.innerWidth, window.innerHeight);
#                 }});
                
#                 // Animation loop
#                 function animate() {{
#                     requestAnimationFrame(animate);
#                     controls.update();
#                     renderer.render(scene, camera);
#                 }}
                
#                 // Initial setup
#                 createObjects();
#                 animate();
                
#                 // Communication with Python (not needed in export)
#                 {"" if is_export else """
#                 // Function to communicate with PyQt
#                 function receiveFromPython(jsonData) {
#                     const data = JSON.parse(jsonData);
#                     if (data.command === 'update_objects') {
#                         objects = data.objects;
#                         createObjects();
#                     }
#                 }
#                 """}
#             </script>
#         </body>
#         </html>
#         """
#         return html


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ModelingTool()
#     window.show()
#     sys.exit(app.exec_())



import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QColorDialog, QGroupBox, QGridLayout,
                            QSpinBox, QDoubleSpinBox, QFileDialog)
from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QColor

class Bridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
    
    @pyqtSlot(str)
    def objectSelected(self, object_id):
        # This method is called from JavaScript when an object is selected
        self.main_window.handle_object_selected(object_id)

class ModelingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Model Drawing Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Store all objects in a list for exporting
        self.objects = []
        self.object_counter = 0
        self.selected_object_id = None
        
        # Setup main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        
        # Left panel - Controls
        self.controls_panel = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_panel)
        
        # Create control groups
        self.create_vertical_beam_controls()
        self.create_horizontal_beam_controls()
        self.create_sphere_controls()
        self.create_delete_controls()  # New control section for deletion
        self.create_export_controls()
        
        self.main_layout.addWidget(self.controls_panel, 1)
        
        # Right panel - 3D view
        self.view_panel = QWebEngineView()
        
        # Setup web channel for JavaScript-Python communication
        self.channel = QWebChannel()
        self.bridge = Bridge(self)
        self.channel.registerObject('bridge', self.bridge)
        
        self.init_three_js_view()
        
        # Set the web channel to the view's page
        self.view_panel.page().setWebChannel(self.channel)
        
        self.main_layout.addWidget(self.view_panel, 2)
    
    def create_vertical_beam_controls(self):
        # Existing code unchanged
        group_box = QGroupBox("Add Vertical Beam (Z axis)")
        layout = QGridLayout()
        
        # Radius
        layout.addWidget(QLabel("Radius:"), 0, 0)
        self.vert_radius = QDoubleSpinBox()
        self.vert_radius.setRange(0.1, 100.0)
        self.vert_radius.setValue(1.0)
        self.vert_radius.setSingleStep(0.1)
        layout.addWidget(self.vert_radius, 0, 1)
        
        # Length
        layout.addWidget(QLabel("Length:"), 1, 0)
        self.vert_length = QDoubleSpinBox()
        self.vert_length.setRange(0.1, 1000.0)
        self.vert_length.setValue(10.0)
        self.vert_length.setSingleStep(0.1)
        layout.addWidget(self.vert_length, 1, 1)
        
        # Color
        layout.addWidget(QLabel("Color:"), 2, 0)
        self.vert_color_btn = QPushButton()
        self.vert_color_btn.setStyleSheet("background-color: #ff0000")
        self.vert_color = "#ff0000"
        self.vert_color_btn.clicked.connect(lambda: self.select_color("vert"))
        layout.addWidget(self.vert_color_btn, 2, 1)
        
        # Position
        layout.addWidget(QLabel("Position X:"), 3, 0)
        self.vert_pos_x = QDoubleSpinBox()
        self.vert_pos_x.setRange(-1000.0, 1000.0)
        self.vert_pos_x.setValue(0.0)
        self.vert_pos_x.setSingleStep(0.5)
        layout.addWidget(self.vert_pos_x, 3, 1)
        
        layout.addWidget(QLabel("Position Y:"), 4, 0)
        self.vert_pos_y = QDoubleSpinBox()
        self.vert_pos_y.setRange(-1000.0, 1000.0)
        self.vert_pos_y.setValue(0.0)
        self.vert_pos_y.setSingleStep(0.5)
        layout.addWidget(self.vert_pos_y, 4, 1)
        
        layout.addWidget(QLabel("Position Z:"), 5, 0)
        self.vert_pos_z = QDoubleSpinBox()
        self.vert_pos_z.setRange(-1000.0, 1000.0)
        self.vert_pos_z.setValue(0.0)
        self.vert_pos_z.setSingleStep(0.5)
        layout.addWidget(self.vert_pos_z, 5, 1)
        
        # Rotation
        layout.addWidget(QLabel("Rotate X (deg):"), 6, 0)
        self.vert_rot_x = QDoubleSpinBox()
        self.vert_rot_x.setRange(-180.0, 180.0)
        self.vert_rot_x.setValue(0.0)
        self.vert_rot_x.setSingleStep(5.0)
        layout.addWidget(self.vert_rot_x, 6, 1)
        
        layout.addWidget(QLabel("Rotate Y (deg):"), 7, 0)
        self.vert_rot_y = QDoubleSpinBox()
        self.vert_rot_y.setRange(-180.0, 180.0)
        self.vert_rot_y.setValue(0.0)
        self.vert_rot_y.setSingleStep(5.0)
        layout.addWidget(self.vert_rot_y, 7, 1)
        
        # Add Button
        self.add_vert_beam_btn = QPushButton("Add Vertical Beam")
        self.add_vert_beam_btn.clicked.connect(self.add_vertical_beam)
        layout.addWidget(self.add_vert_beam_btn, 8, 0, 1, 2)
        
        group_box.setLayout(layout)
        self.controls_layout.addWidget(group_box)
    
    def create_horizontal_beam_controls(self):
        # Existing code unchanged
        group_box = QGroupBox("Add Horizontal Beam (X axis)")
        layout = QGridLayout()
        
        # Radius
        layout.addWidget(QLabel("Radius:"), 0, 0)
        self.horz_radius = QDoubleSpinBox()
        self.horz_radius.setRange(0.1, 100.0)
        self.horz_radius.setValue(1.0)
        self.horz_radius.setSingleStep(0.1)
        layout.addWidget(self.horz_radius, 0, 1)
        
        # Length
        layout.addWidget(QLabel("Length:"), 1, 0)
        self.horz_length = QDoubleSpinBox()
        self.horz_length.setRange(0.1, 100.0)
        self.horz_length.setValue(10.0)
        self.horz_length.setSingleStep(0.1)
        layout.addWidget(self.horz_length, 1, 1)
        
        # Color
        layout.addWidget(QLabel("Color:"), 2, 0)
        self.horz_color_btn = QPushButton()
        self.horz_color_btn.setStyleSheet("background-color: #00ff00")
        self.horz_color = "#00ff00"
        self.horz_color_btn.clicked.connect(lambda: self.select_color("horz"))
        layout.addWidget(self.horz_color_btn, 2, 1)
        
        # Position
        layout.addWidget(QLabel("Position X:"), 3, 0)
        self.horz_pos_x = QDoubleSpinBox()
        self.horz_pos_x.setRange(-100.0, 100.0)
        self.horz_pos_x.setValue(0.0)
        self.horz_pos_x.setSingleStep(0.5)
        layout.addWidget(self.horz_pos_x, 3, 1)
        
        layout.addWidget(QLabel("Position Y:"), 4, 0)
        self.horz_pos_y = QDoubleSpinBox()
        self.horz_pos_y.setRange(-100.0, 100.0)
        self.horz_pos_y.setValue(0.0)
        self.horz_pos_y.setSingleStep(0.5)
        layout.addWidget(self.horz_pos_y, 4, 1)
        
        layout.addWidget(QLabel("Position Z:"), 5, 0)
        self.horz_pos_z = QDoubleSpinBox()
        self.horz_pos_z.setRange(-100.0, 100.0)
        self.horz_pos_z.setValue(0.0)
        self.horz_pos_z.setSingleStep(0.5)
        layout.addWidget(self.horz_pos_z, 5, 1)
        
        # Rotation
        layout.addWidget(QLabel("Rotate Y (deg):"), 6, 0)
        self.horz_rot_y = QDoubleSpinBox()
        self.horz_rot_y.setRange(-180.0, 180.0)
        self.horz_rot_y.setValue(0.0)
        self.horz_rot_y.setSingleStep(5.0)
        layout.addWidget(self.horz_rot_y, 6, 1)
        
        layout.addWidget(QLabel("Rotate Z (deg):"), 7, 0)
        self.horz_rot_z = QDoubleSpinBox()
        self.horz_rot_z.setRange(-180.0, 180.0)
        self.horz_rot_z.setValue(0.0)
        self.horz_rot_z.setSingleStep(5.0)
        layout.addWidget(self.horz_rot_z, 7, 1)
        
        # Add Button
        self.add_horz_beam_btn = QPushButton("Add Horizontal Beam")
        self.add_horz_beam_btn.clicked.connect(self.add_horizontal_beam)
        layout.addWidget(self.add_horz_beam_btn, 8, 0, 1, 2)
        
        group_box.setLayout(layout)
        self.controls_layout.addWidget(group_box)
    
    def create_sphere_controls(self):
        # Existing code unchanged
        group_box = QGroupBox("Add Sphere")
        layout = QGridLayout()
        
        # Radius
        layout.addWidget(QLabel("Radius:"), 0, 0)
        self.sphere_radius = QDoubleSpinBox()
        self.sphere_radius.setRange(0.1, 100.0)
        self.sphere_radius.setValue(2.0)
        self.sphere_radius.setSingleStep(0.1)
        layout.addWidget(self.sphere_radius, 0, 1)
        
        # Color
        layout.addWidget(QLabel("Color:"), 1, 0)
        self.sphere_color_btn = QPushButton()
        self.sphere_color_btn.setStyleSheet("background-color: #0000ff")
        self.sphere_color = "#0000ff"
        self.sphere_color_btn.clicked.connect(lambda: self.select_color("sphere"))
        layout.addWidget(self.sphere_color_btn, 1, 1)
        
        # Position
        layout.addWidget(QLabel("Position X:"), 2, 0)
        self.sphere_pos_x = QDoubleSpinBox()
        self.sphere_pos_x.setRange(-100.0, 100.0)
        self.sphere_pos_x.setValue(0.0)
        self.sphere_pos_x.setSingleStep(0.5)
        layout.addWidget(self.sphere_pos_x, 2, 1)
        
        layout.addWidget(QLabel("Position Y:"), 3, 0)
        self.sphere_pos_y = QDoubleSpinBox()
        self.sphere_pos_y.setRange(-100.0, 100.0)
        self.sphere_pos_y.setValue(0.0)
        self.sphere_pos_y.setSingleStep(0.5)
        layout.addWidget(self.sphere_pos_y, 3, 1)
        
        layout.addWidget(QLabel("Position Z:"), 4, 0)
        self.sphere_pos_z = QDoubleSpinBox()
        self.sphere_pos_z.setRange(-100.0, 100.0)
        self.sphere_pos_z.setValue(0.0)
        self.sphere_pos_z.setSingleStep(0.5)
        layout.addWidget(self.sphere_pos_z, 4, 1)
        
        # Add Button
        self.add_sphere_btn = QPushButton("Add Sphere")
        self.add_sphere_btn.clicked.connect(self.add_sphere)
        layout.addWidget(self.add_sphere_btn, 5, 0, 1, 2)
        
        group_box.setLayout(layout)
        self.controls_layout.addWidget(group_box)
        
    def create_delete_controls(self):
        # New control section for object deletion
        group_box = QGroupBox("Delete Object")
        layout = QVBoxLayout()
        
        # Label to show selected object
        self.selected_object_label = QLabel("No object selected")
        layout.addWidget(self.selected_object_label)
        
        # Delete button (disabled by default)
        self.delete_btn = QPushButton("Delete Selected Object")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_selected_object)
        layout.addWidget(self.delete_btn)
        
        group_box.setLayout(layout)
        self.controls_layout.addWidget(group_box)
    
    def create_export_controls(self):
        # Existing code unchanged
        group_box = QGroupBox("Export")
        layout = QVBoxLayout()
        
        self.export_btn = QPushButton("Export 3D Model as HTML")
        self.export_btn.clicked.connect(self.export_model)
        layout.addWidget(self.export_btn)
        
        group_box.setLayout(layout)
        self.controls_layout.addWidget(group_box)
    
    def handle_object_selected(self, object_id):
        # Update UI based on selected object
        self.selected_object_id = object_id
        
        if object_id:
            # Find object details
            selected_obj = next((obj for obj in self.objects if obj["id"] == object_id), None)
            if selected_obj:
                obj_type = selected_obj["type"]
                self.selected_object_label.setText(f"Selected: {obj_type} (ID: {object_id})")
                self.delete_btn.setEnabled(True)
            else:
                self.selected_object_label.setText("No object selected")
                self.delete_btn.setEnabled(False)
        else:
            self.selected_object_label.setText("No object selected")
            self.delete_btn.setEnabled(False)
    
    def delete_selected_object(self):
        if self.selected_object_id:
            # Find and remove the selected object
            self.objects = [obj for obj in self.objects if obj["id"] != self.selected_object_id]
            
            # Update the view
            self.update_threejs_view()
            
            # Reset selection
            self.selected_object_id = None
            self.selected_object_label.setText("No object selected")
            self.delete_btn.setEnabled(False)
    
    def select_color(self, element_type):
        # Existing code unchanged
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            if element_type == "vert":
                self.vert_color = hex_color
                self.vert_color_btn.setStyleSheet(f"background-color: {hex_color}")
            elif element_type == "horz":
                self.horz_color = hex_color
                self.horz_color_btn.setStyleSheet(f"background-color: {hex_color}")
            elif element_type == "sphere":
                self.sphere_color = hex_color
                self.sphere_color_btn.setStyleSheet(f"background-color: {hex_color}")
    
    def init_three_js_view(self):
        # Create HTML with embedded Three.js
        html_content = self.get_threejs_html()
        
        # Create a temporary file with the HTML content
        temp_file = "temp_threejs_view.html"
        with open(temp_file, "w") as f:
            f.write(html_content)
        
        # Load the HTML file into the QWebEngineView
        self.view_panel.load(QUrl.fromLocalFile(os.path.abspath(temp_file)))
    
    def add_vertical_beam(self):
        # Existing code unchanged
        # Get values from inputs
        radius = self.vert_radius.value()
        length = self.vert_length.value()
        color = self.vert_color
        pos_x = self.vert_pos_x.value()
        pos_y = self.vert_pos_y.value()
        pos_z = self.vert_pos_z.value()
        rot_x = self.vert_rot_x.value()
        rot_y = self.vert_rot_y.value()
        
        # Create object data
        obj_id = f"obj_{self.object_counter}"
        self.object_counter += 1
        
        obj_data = {
            "id": obj_id,
            "type": "vertical_beam",
            "radius": radius,
            "length": length,
            "color": color,
            "position": [pos_x, pos_y, pos_z],
            "rotation": [rot_x, rot_y, 0]
        }
        
        self.objects.append(obj_data)
        self.update_threejs_view()
    
    def add_horizontal_beam(self):
        # Existing code unchanged
        # Get values from inputs
        radius = self.horz_radius.value()
        length = self.horz_length.value()
        color = self.horz_color
        pos_x = self.horz_pos_x.value()
        pos_y = self.horz_pos_y.value()
        pos_z = self.horz_pos_z.value()
        rot_y = self.horz_rot_y.value()
        rot_z = self.horz_rot_z.value()
        
        # Create object data
        obj_id = f"obj_{self.object_counter}"
        self.object_counter += 1
        
        obj_data = {
            "id": obj_id,
            "type": "horizontal_beam",
            "radius": radius,
            "length": length,
            "color": color,
            "position": [pos_x, pos_y, pos_z],
            "rotation": [0, rot_y, rot_z]
        }
        
        self.objects.append(obj_data)
        self.update_threejs_view()
    
    def add_sphere(self):
        # Existing code unchanged
        # Get values from inputs
        radius = self.sphere_radius.value()
        color = self.sphere_color
        pos_x = self.sphere_pos_x.value()
        pos_y = self.sphere_pos_y.value()
        pos_z = self.sphere_pos_z.value()
        
        # Create object data
        obj_id = f"obj_{self.object_counter}"
        self.object_counter += 1
        
        obj_data = {
            "id": obj_id,
            "type": "sphere",
            "radius": radius,
            "color": color,
            "position": [pos_x, pos_y, pos_z]
        }
        
        self.objects.append(obj_data)
        self.update_threejs_view()
    
    def update_threejs_view(self):
        # Generate updated HTML with current objects
        html_content = self.get_threejs_html()
        
        # Update the temporary file
        temp_file = "temp_threejs_view.html"
        with open(temp_file, "w") as f:
            f.write(html_content)
        
        # Reload the view
        self.view_panel.load(QUrl.fromLocalFile(os.path.abspath(temp_file)))
    
    def export_model(self):
        # Existing code unchanged
        # Ask for file location to save
        file_path, _ = QFileDialog.getSaveFileName(self, "Save 3D Model", "", "HTML Files (*.html)")
        
        if file_path:
            # Generate HTML with the export flag set to True
            html_content = self.get_threejs_html(is_export=True)
            
            # Save to file
            with open(file_path, "w") as f:
                f.write(html_content)
    
    def get_threejs_html(self, is_export=False):
        # Convert objects to JSON
        objects_json = json.dumps(self.objects)
        
        # Create HTML with Three.js including new selection functionality
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>3D Model Viewer</title>
            <style>
                body {{ margin: 0; overflow: hidden; }}
                canvas {{ width: 100%; height: 100%; display: block; }}
                #isometric-view-btn {{
                    position: absolute;
                    bottom: 20px;
                    right: 20px;
                    z-index: 100;
                    padding: 10px;
                    background-color: rgba(0, 0, 0, 0.5);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.7/dat.gui.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.min.js"></script>
            {"" if is_export else '<script src="qrc:///qtwebchannel/qwebchannel.js"></script>'}
        </head>
        <body>
            <button id="isometric-view-btn">Set Isometric View</button>
            <script>
                const objects = {objects_json};
                
                // Scene setup
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0xf0f0f0);
                
                // Camera setup
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                camera.position.set(30, 30, 30);
                camera.lookAt(0, 0, 0);
                
                // Renderer setup
                const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);
                
                // Controls setup
                const controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.25;
                
                // Grid helper
                const gridHelper = new THREE.GridHelper(50, 50);
                scene.add(gridHelper);
                
                // Axes helper
                const axesHelper = new THREE.AxesHelper(20);
                scene.add(axesHelper);
                
                // Add ambient light
                const ambientLight = new THREE.AmbientLight(0x404040);
                scene.add(ambientLight);
                
                // Add directional light
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
                directionalLight.position.set(1, 1, 1);
                scene.add(directionalLight);
                
                // Setup for object selection
                const raycaster = new THREE.Raycaster();
                const pointer = new THREE.Vector2();
                let selectedObject = null;
                
                // Create all objects
                function createObjects() {{
                    // Remove all existing objects (except grid and axes)
                    scene.children.forEach(child => {{
                        if (!(child instanceof THREE.GridHelper) && 
                            !(child instanceof THREE.AxesHelper) &&
                            !(child instanceof THREE.Light)) {{
                            scene.remove(child);
                        }}
                    }});
                    
                    // Add new objects
                    objects.forEach(obj => {{
                        if (obj.type === 'vertical_beam') {{
                            createCylinder(
                                obj.id,
                                obj.radius, 
                                obj.length, 
                                obj.color, 
                                obj.position,
                                obj.rotation,
                                [0, 0, 1]  // Align with Z axis
                            );
                        }} else if (obj.type === 'horizontal_beam') {{
                            createCylinder(
                                obj.id,
                                obj.radius, 
                                obj.length, 
                                obj.color, 
                                obj.position,
                                obj.rotation,
                                [1, 0, 0]  // Align with X axis
                            );
                        }} else if (obj.type === 'sphere') {{
                            createSphere(
                                obj.id,
                                obj.radius,
                                obj.color,
                                obj.position
                            );
                        }}
                    }});
                }}
                
                function createCylinder(id, radius, length, color, position, rotation, axis) {{
                    const geometry = new THREE.CylinderGeometry(radius, radius, length, 32);
                    const material = new THREE.MeshPhongMaterial({{ color: color }});
                    const cylinder = new THREE.Mesh(geometry, material);
                    
                    // Set name/id
                    cylinder.name = id;
                    
                    // Rotate cylinder to align with specified axis
                    if (axis[0] === 1) {{  // X axis
                        cylinder.rotation.z = Math.PI / 2;
                    }} else if (axis[1] === 1) {{  // Y axis
                        cylinder.rotation.x = Math.PI / 2;
                    }}
                    
                    // Apply additional rotation
                    const rotRad = rotation.map(deg => deg * Math.PI / 180);
                    cylinder.rotateX(rotRad[0]);
                    cylinder.rotateY(rotRad[1]);
                    cylinder.rotateZ(rotRad[2]);
                    
                    // Set position
                    cylinder.position.set(position[0], position[1], position[2]);
                    
                    scene.add(cylinder);
                }}
                
                function createSphere(id, radius, color, position) {{
                    const geometry = new THREE.SphereGeometry(radius, 32, 32);
                    const material = new THREE.MeshPhongMaterial({{ color: color }});
                    const sphere = new THREE.Mesh(geometry, material);
                    
                    // Set name/id
                    sphere.name = id;
                    
                    // Set position
                    sphere.position.set(position[0], position[1], position[2]);
                    
                    scene.add(sphere);
                }}
                
                // Object selection handling
                function onClick(event) {{
                    // Calculate mouse position in normalized device coordinates
                    pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
                    pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
                    
                    // Update the picking ray with the camera and pointer position
                    raycaster.setFromCamera(pointer, camera);
                    
                    // Find all selectable objects (those with names starting with "obj_")
                    const selectableObjects = scene.children.filter(obj => {{
                        return obj.name && obj.name.startsWith('obj_');
                    }});
                    
                    // Find intersections
                    const intersects = raycaster.intersectObjects(selectableObjects);
                    
                    if (intersects.length > 0) {{
                        selectObject(intersects[0].object);
                    }} else {{
                        clearSelection();
                    }}
                }}
                
                function selectObject(object) {{
                    // Clear previous selection
                    clearSelection();
                    
                    // Store reference to selected object
                    selectedObject = object;
                    
                    // Highlight the object
                    if (selectedObject.material) {{
                        // Store original material properties
                        if (!selectedObject.userData.originalEmissive) {{
                            selectedObject.userData.originalEmissive = 
                                selectedObject.material.emissive ? 
                                selectedObject.material.emissive.clone() : 
                                new THREE.Color(0x000000);
                        }}
                        
                        // Set emissive color for highlight
                        selectedObject.material.emissive = new THREE.Color(0x555555);
                    }}
                    
                    // Communicate selection to Python
                    if (typeof bridge !== 'undefined') {{
                        bridge.objectSelected(selectedObject.name);
                    }}
                }}
                
                function clearSelection() {{
                    if (selectedObject) {{
                        // Restore original material properties
                        if (selectedObject.material && selectedObject.userData.originalEmissive) {{
                            selectedObject.material.emissive = selectedObject.userData.originalEmissive;
                        }}
                        
                        selectedObject = null;
                        
                        // Communicate deselection to Python
                        if (typeof bridge !== 'undefined') {{
                            bridge.objectSelected("");
                        }}
                    }}
                }}
                
                // Set isometric view
                document.getElementById('isometric-view-btn').addEventListener('click', function() {{
                    camera.position.set(20, 20, 20);
                    camera.lookAt(0, 0, 0);
                    controls.update();
                }});
                
                // Handle window resize
                window.addEventListener('resize', function() {{
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }});
                
                // Add click event listener for object selection
                renderer.domElement.addEventListener('click', onClick, false);
                
                // Animation loop
                function animate() {{
                    requestAnimationFrame(animate);
                    controls.update();
                    renderer.render(scene, camera);
                }}
                
                // Initial setup
                createObjects();
                animate();
                
                // Setup connection to Python (not needed in export)
                {"" if is_export else """
                // Connect to QWebChannel
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.bridge = channel.objects.bridge;
                });
                """}
            </script>
        </body>
        </html>
        """
        return html


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModelingTool()
    window.show()
    sys.exit(app.exec_())
