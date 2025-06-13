import sys
import numpy as np
import pyvista as pv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QSlider, 
                             QLabel, QComboBox)
from PyQt5.QtCore import QTimer, Qt
from pyvistaqt import QtInteractor


class SphereHeatmapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Sphere Heatmap")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create PyVista plotter widget
        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)
        
        # Create control panel
        self.create_controls(layout)
        
        # Initialize sphere and data
        self.setup_sphere()
        self.setup_animation()
        
        # Set up the scene
        self.setup_scene()
        
    def create_controls(self, layout):
        """Create control panel with buttons and sliders"""
        control_layout = QHBoxLayout()
        
        # Animation controls
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_animation)
        control_layout.addWidget(self.play_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_animation)
        control_layout.addWidget(self.reset_button)
        
        # Speed control
        control_layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(10)
        self.speed_slider.valueChanged.connect(self.update_speed)
        control_layout.addWidget(self.speed_slider)
        
        # Pattern selection
        control_layout.addWidget(QLabel("Pattern:"))
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(["Waves", "Spiral", "Random", "Gaussian Blobs"])
        self.pattern_combo.currentTextChanged.connect(self.change_pattern)
        control_layout.addWidget(self.pattern_combo)
        
        # Colormap selection
        control_layout.addWidget(QLabel("Colormap:"))
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(["viridis", "plasma", "inferno", "coolwarm", "jet"])
        self.colormap_combo.currentTextChanged.connect(self.change_colormap)
        control_layout.addWidget(self.colormap_combo)
        
        layout.addLayout(control_layout)
        
    def setup_sphere(self):
        """Create sphere mesh and initialize data"""
        # Create sphere with sufficient resolution for smooth heatmap
        self.sphere = pv.Sphere(radius=1.0, phi_resolution=60, theta_resolution=120)
        
        # Get sphere coordinates for data generation
        self.points = self.sphere.points
        self.n_points = len(self.points)
        
        # Convert to spherical coordinates for pattern generation
        x, y, z = self.points[:, 0], self.points[:, 1], self.points[:, 2]
        self.theta = np.arctan2(y, x)  # azimuthal angle
        self.phi = np.arccos(z)        # polar angle
        
        # Initialize data array
        self.data = np.zeros(self.n_points)
        
    def setup_animation(self):
        """Setup animation timer and parameters"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.time_step = 0
        self.is_playing = False
        self.current_pattern = "Waves"
        
    def setup_scene(self):
        """Setup the PyVista scene"""
        # Add sphere to plotter
        self.mesh_actor = self.plotter.add_mesh(
            self.sphere, 
            scalars=self.data,
            cmap='viridis',
            show_edges=False,
            smooth_shading=True,
            scalar_bar_args={'title': 'Temperature'}
        )
        
        # Set camera and lighting
        self.plotter.camera_position = 'iso'
        self.plotter.add_light(pv.Light(position=(2, 2, 2), intensity=0.8))
        self.plotter.add_light(pv.Light(position=(-2, -2, 2), intensity=0.3))
        
        # Initial data update
        self.update_data()
        
    def generate_wave_pattern(self, t):
        """Generate wave interference pattern"""
        # Multiple wave sources
        wave1 = np.sin(3 * self.theta + 2 * t) * np.cos(2 * self.phi)
        wave2 = np.cos(2 * self.theta - 1.5 * t) * np.sin(3 * self.phi)
        wave3 = np.sin(self.theta + self.phi + t)
        
        return wave1 + 0.7 * wave2 + 0.5 * wave3
        
    def generate_spiral_pattern(self, t):
        """Generate spiral pattern"""
        spiral = np.sin(5 * self.theta + 3 * self.phi + 2 * t)
        radial = np.cos(4 * self.phi + t)
        return spiral * radial
        
    def generate_random_pattern(self, t):
        """Generate random blob pattern"""
        np.random.seed(int(t * 10) % 1000)  # Semi-random but reproducible
        n_blobs = 8
        pattern = np.zeros(self.n_points)
        
        for i in range(n_blobs):
            # Random center on sphere
            center_theta = np.random.uniform(0, 2 * np.pi)
            center_phi = np.random.uniform(0, np.pi)
            intensity = np.random.uniform(0.5, 1.5)
            
            # Calculate distance on sphere surface
            dist = np.arccos(np.cos(self.phi) * np.cos(center_phi) + 
                           np.sin(self.phi) * np.sin(center_phi) * 
                           np.cos(self.theta - center_theta))
            
            # Add gaussian blob
            pattern += intensity * np.exp(-5 * dist**2) * np.sin(t + i)
            
        return pattern
        
    def generate_gaussian_blobs(self, t):
        """Generate moving Gaussian blobs"""
        pattern = np.zeros(self.n_points)
        
        # Define blob centers that move over time
        blob_centers = [
            (np.sin(t), np.cos(t), 0.5 * np.sin(2*t)),
            (np.cos(1.5*t), 0.5*np.sin(t), np.cos(0.8*t)),
            (0.3*np.sin(3*t), np.cos(2*t), np.sin(1.2*t))
        ]
        
        for center in blob_centers:
            # Normalize center to sphere surface
            center = np.array(center)
            center = center / np.linalg.norm(center)
            
            # Calculate distances from blob center
            distances = np.linalg.norm(self.points - center, axis=1)
            
            # Add gaussian blob
            pattern += 2 * np.exp(-8 * distances**2)
            
        return pattern
        
    def update_data(self):
        """Update the heatmap data based on current pattern and time"""
        t = self.time_step * 0.1
        
        if self.current_pattern == "Waves":
            self.data = self.generate_wave_pattern(t)
        elif self.current_pattern == "Spiral":
            self.data = self.generate_spiral_pattern(t)
        elif self.current_pattern == "Random":
            self.data = self.generate_random_pattern(t)
        elif self.current_pattern == "Gaussian Blobs":
            self.data = self.generate_gaussian_blobs(t)
            
        # Normalize data for better visualization
        self.data = (self.data - self.data.min()) / (self.data.max() - self.data.min())
        
        # Update mesh scalars
        self.sphere.point_data['temperature'] = self.data
        
    def update_animation(self):
        """Animation step function"""
        self.time_step += 1
        self.update_data()
        
        # Update the mesh display
        self.plotter.update_scalars(self.data, mesh=self.sphere, render=True)
        
    def toggle_animation(self):
        """Start/stop animation"""
        if self.is_playing:
            self.timer.stop()
            self.play_button.setText("Play")
            self.is_playing = False
        else:
            interval = max(20, 200 - self.speed_slider.value() * 10)
            self.timer.start(interval)
            self.play_button.setText("Pause")
            self.is_playing = True
            
    def reset_animation(self):
        """Reset animation to beginning"""
        self.timer.stop()
        self.time_step = 0
        self.update_data()
        self.plotter.update_scalars(self.data, mesh=self.sphere, render=True)
        self.play_button.setText("Play")
        self.is_playing = False
        
    def update_speed(self, value):
        """Update animation speed"""
        if self.is_playing:
            interval = max(20, 200 - value * 10)
            self.timer.start(interval)
            
    def change_pattern(self, pattern):
        """Change the heatmap pattern"""
        self.current_pattern = pattern
        self.update_data()
        self.plotter.update_scalars(self.data, mesh=self.sphere, render=True)
        
    def change_colormap(self, colormap):
        """Change the colormap"""
        # Remove current mesh and add with new colormap
        self.plotter.remove_actor(self.mesh_actor)
        self.mesh_actor = self.plotter.add_mesh(
            self.sphere, 
            scalars=self.data,
            cmap=colormap,
            show_edges=False,
            smooth_shading=True,
            scalar_bar_args={'title': 'Temperature'}
        )


def main():
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = SphereHeatmapViewer()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()