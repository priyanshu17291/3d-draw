import numpy as np
import pyvista as pv
import random
import time
from warnings import filterwarnings
from scipy.spatial.distance import cdist

# Filter out PyVista deprecation warnings
filterwarnings("ignore", category=DeprecationWarning)

class DynamicBuildingHeatmap:
    def __init__(self):
        self.plotter = pv.Plotter(window_size=[1200, 900])
        self.building = None
        self.sensor_positions = []
        self.mesh_actors = {}
        
        # Animation control
        self.is_playing = False
        self.time_step = 0
        self.animation_speed = 1.0
        self.update_interval = 50  # Default update interval in ms
        
        # Heat simulation parameters
        self.heat_sources = []
        self.ambient_temperature = 22.0
        self.current_pattern = "Dynamic Sources"
        self.available_patterns = ["Dynamic Sources", "Wave Interference", "Thermal Plumes", "HVAC Cycles"]
        
        # Thermal properties
        self.thermal_diffusivity = 0.03
        self.heat_loss_rate = 0.015

    def create_building(self, floors=5, width=20, depth=15, floor_height=3, shape='rectangular'):
        """Create a building structure with specified parameters"""
        self.building = pv.MultiBlock()
        self.floor_params = {
            'floors': floors,
            'width': width,
            'depth': depth,
            'floor_height': floor_height,
            'shape': shape
        }
        
        for floor in range(floors):
            z = floor * floor_height
            if shape == 'rectangular':
                floor_surface = pv.Plane(
                    center=(width/2, depth/2, z),
                    direction=(0, 0, 1),
                    i_size=width,
                    j_size=depth,
                    i_resolution=40,  # Higher resolution for smoother patterns
                    j_resolution=35
                )
            elif shape == 'circular':
                floor_surface = pv.Disc(center=(0, 0, z), normal=(0, 0, 1), 
                                      inner=0, outer=width/2, r_res=40, c_res=80)
            else:
                raise ValueError("Supported shapes: 'rectangular' or 'circular'")
                
            # Initialize with ambient temperature
            floor_surface["Heat"] = np.full(floor_surface.n_points, self.ambient_temperature)
            floor_surface["previous_heat"] = np.full(floor_surface.n_points, self.ambient_temperature)
            
            # Store normalized coordinates for pattern generation
            points = floor_surface.points
            if shape == 'rectangular':
                # Normalize to [0, 1] range for pattern generation
                floor_surface["norm_x"] = (points[:, 0] - points[:, 0].min()) / (points[:, 0].max() - points[:, 0].min())
                floor_surface["norm_y"] = (points[:, 1] - points[:, 1].min()) / (points[:, 1].max() - points[:, 1].min())
            else:
                # For circular, use polar coordinates
                center_x, center_y = 0, 0
                r = np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2)
                theta = np.arctan2(points[:, 1] - center_y, points[:, 0] - center_x)
                floor_surface["norm_r"] = r / np.max(r)
                floor_surface["norm_theta"] = (theta + np.pi) / (2 * np.pi)
            
            self.building[f"Floor_{floor+1}"] = floor_surface
            
        # Initialize heat sources
        self._initialize_heat_sources()
        return self.building
    
    def _initialize_heat_sources(self):
        """Initialize heat sources for pattern generation"""
        self.heat_sources = []
        for floor in range(self.floor_params['floors']):
            floor_surface = self.building[f"Floor_{floor+1}"]
            points = floor_surface.points
            
            # Create 3-5 heat sources per floor
            n_sources = random.randint(3, 5)
            for i in range(n_sources):
                source_type = random.choice(['hvac', 'equipment', 'solar', 'people'])
                position = points[random.randint(0, len(points)-1)]
                
                self.heat_sources.append({
                    'floor': floor,
                    'position': position,
                    'type': source_type,
                    'base_intensity': random.uniform(5, 25) if source_type != 'hvac' else random.uniform(-15, 15),
                    'frequency': random.uniform(0.5, 3.0),  # Pattern frequency
                    'phase': random.uniform(0, 2*np.pi),    # Phase offset
                    'influence_radius': random.uniform(3, 8),
                    'active': True
                })
    
    def generate_wave_interference_pattern(self, floor_surface, t):
        """Generate wave interference pattern similar to sphere code"""
        if self.floor_params['shape'] == 'rectangular':
            norm_x = floor_surface["norm_x"]
            norm_y = floor_surface["norm_y"]
            
            # Multiple wave sources with different frequencies
            wave1 = np.sin(4 * np.pi * norm_x + 2 * t) * np.cos(3 * np.pi * norm_y)
            wave2 = np.cos(3 * np.pi * norm_x - 1.5 * t) * np.sin(4 * np.pi * norm_y)
            wave3 = np.sin(2 * np.pi * (norm_x + norm_y) + t)
            
            pattern = wave1 + 0.7 * wave2 + 0.5 * wave3
        else:
            # Circular building - use polar coordinates
            norm_r = floor_surface["norm_r"]
            norm_theta = floor_surface["norm_theta"]
            
            # Radial and angular wave patterns
            radial_wave = np.sin(5 * np.pi * norm_r + t)
            angular_wave = np.cos(8 * np.pi * norm_theta - 2 * t)
            spiral_wave = np.sin(3 * np.pi * norm_r + 6 * np.pi * norm_theta + 1.5 * t)
            
            pattern = radial_wave + 0.8 * angular_wave + 0.6 * spiral_wave
        
        # Scale and offset to temperature range
        pattern = self.ambient_temperature + 8 * pattern
        return pattern
    
    def generate_thermal_plumes_pattern(self, floor_surface, t):
        """Generate rising thermal plume pattern"""
        points = floor_surface.points
        pattern = np.full(len(points), self.ambient_temperature)
        
        # Create moving thermal plumes
        n_plumes = 4
        for i in range(n_plumes):
            # Plume center moves over time
            center_x = self.floor_params['width'] * (0.2 + 0.6 * (i / n_plumes))
            center_y = self.floor_params['depth'] * (0.3 + 0.4 * np.sin(t + i * np.pi/2))
            center_z = points[0, 2]  # Floor level
            
            plume_center = np.array([center_x, center_y, center_z])
            
            # Calculate distances from plume center
            distances = np.linalg.norm(points - plume_center, axis=1)
            
            # Thermal plume with realistic decay
            intensity = 15 * (1 + 0.5 * np.sin(2 * t + i))
            radius = 4 + 2 * np.sin(t * 0.7 + i)
            
            # Gaussian-like thermal distribution
            plume_contribution = intensity * np.exp(-0.5 * (distances / radius) ** 2)
            pattern += plume_contribution
        
        return pattern
    
    def generate_hvac_cycles_pattern(self, floor_surface, t):
        """Generate HVAC cycling pattern"""
        points = floor_surface.points
        pattern = np.full(len(points), self.ambient_temperature)
        
        # HVAC zones with different cycling patterns
        zones = [
            {'center': [self.floor_params['width'] * 0.25, self.floor_params['depth'] * 0.25], 
             'radius': 8, 'cycle_freq': 0.3, 'intensity': -10},  # Cooling zone
            {'center': [self.floor_params['width'] * 0.75, self.floor_params['depth'] * 0.25], 
             'radius': 6, 'cycle_freq': 0.5, 'intensity': 12},   # Heating zone
            {'center': [self.floor_params['width'] * 0.5, self.floor_params['depth'] * 0.75], 
             'radius': 7, 'cycle_freq': 0.4, 'intensity': -8},   # Another cooling zone
        ]
        
        for zone in zones:
            center_2d = np.array([zone['center'][0], zone['center'][1], points[0, 2]])
            distances = np.linalg.norm(points - center_2d, axis=1)
            
            # HVAC cycling with on/off behavior
            cycle_value = np.sin(2 * np.pi * zone['cycle_freq'] * t)
            if cycle_value > 0.3:  # HVAC is on
                zone_influence = np.exp(-distances / zone['radius'])
                pattern += zone['intensity'] * zone_influence * (0.7 + 0.3 * cycle_value)
        
        return pattern
    
    def generate_dynamic_sources_pattern(self, floor_surface, t):
        """Generate pattern based on dynamic heat sources"""
        points = floor_surface.points
        pattern = np.full(len(points), self.ambient_temperature)
        
        floor_idx = int(floor_surface.points[0, 2] / self.floor_params['floor_height'])
        
        for source in self.heat_sources:
            if source['floor'] == floor_idx and source['active']:
                # Dynamic intensity based on time and source characteristics
                intensity_factor = np.sin(source['frequency'] * t + source['phase'])
                
                if source['type'] == 'hvac':
                    # HVAC with on/off cycles
                    current_intensity = source['base_intensity'] * (intensity_factor > 0.2)
                elif source['type'] == 'equipment':
                    # Equipment with variable load
                    current_intensity = source['base_intensity'] * (0.5 + 0.5 * abs(intensity_factor))
                elif source['type'] == 'solar':
                    # Solar with time-of-day variation
                    current_intensity = source['base_intensity'] * max(0, intensity_factor)
                else:  # people
                    # Intermittent human presence
                    current_intensity = source['base_intensity'] * (intensity_factor > 0.5)
                
                # Apply heat influence
                distances = np.linalg.norm(points - source['position'], axis=1)
                influence = np.exp(-distances / source['influence_radius'])
                pattern += current_intensity * influence
        
        return pattern
    
    def update_heat_data(self):
        """Update heat data using sphere-style pattern generation"""
        t = self.time_step * 0.05 * self.animation_speed  # Time parameter
        
        for floor in range(self.floor_params['floors']):
            floor_surface = self.building[f"Floor_{floor+1}"]
            
            # Generate pattern based on current pattern type
            if self.current_pattern == "Wave Interference":
                new_heat = self.generate_wave_interference_pattern(floor_surface, t)
            elif self.current_pattern == "Thermal Plumes":
                new_heat = self.generate_thermal_plumes_pattern(floor_surface, t)
            elif self.current_pattern == "HVAC Cycles":
                new_heat = self.generate_hvac_cycles_pattern(floor_surface, t)
            else:  # Dynamic Sources
                new_heat = self.generate_dynamic_sources_pattern(floor_surface, t)
            
            # Apply thermal diffusion (simplified)
            current_heat = floor_surface["Heat"]
            previous_heat = floor_surface["previous_heat"]
            
            # Simple heat diffusion
            diffused_heat = self._apply_heat_diffusion(floor_surface, new_heat, current_heat)
            
            # Normalize to reasonable temperature range
            diffused_heat = np.clip(diffused_heat, 5, 50)
            
            # Update mesh data
            floor_surface["previous_heat"] = current_heat.copy()
            floor_surface["Heat"] = diffused_heat
    
    def _apply_heat_diffusion(self, floor_surface, target_heat, current_heat):
        """Apply simplified heat diffusion"""
        # Blend between current and target heat with diffusion
        diffusion_rate = 0.1 * self.animation_speed
        diffused = current_heat + diffusion_rate * (target_heat - current_heat)
        
        # Add some spatial smoothing
        points = floor_surface.points
        smoothed = diffused.copy()
        
        for i in range(len(points)):
            # Find nearby points
            distances = np.linalg.norm(points - points[i], axis=1)
            nearby_mask = (distances < 2.0) & (distances > 0)
            
            if np.any(nearby_mask):
                nearby_temps = diffused[nearby_mask]
                avg_nearby = np.mean(nearby_temps)
                # Blend with nearby average
                smoothed[i] = 0.9 * diffused[i] + 0.1 * avg_nearby
        
        return smoothed
    
    def _update_visualization(self):
        """Force update the visualization"""
        try:
            # Update all floor meshes
            for i in range(self.building.n_blocks):
                name = self.building.get_block_name(i)
                mesh = self.building[name]
                actor = self.mesh_actors[name]
                
                # Update the mesh data
                mesh["Heat"] = mesh["Heat"]  # Forces array to update
                actor.mapper.dataset.point_data["Heat"] = mesh["Heat"]
                
                # Update scalar range if needed
                actor.mapper.scalar_range = [mesh["Heat"].min(), mesh["Heat"].max()]
                
                # Force updates
                actor.mapper.dataset.modified()
                actor.mapper.update()
            
            # Force render
            self.plotter.render()
            
        except Exception as e:
            print(f"Visualization update error: {str(e)}")
    
    def _animation_callback(self, obj, event):
        """Animation callback function (similar to sphere code)"""
        if self.is_playing:
            self.time_step += 1
            self.update_heat_data()
            self._update_visualization()
    
    def toggle_animation(self):
        """Toggle animation play/pause"""
        if self.is_playing:
            self.is_playing = False
            print("⏸️ Animation PAUSED")
        else:
            self.is_playing = True
            print("▶️ Animation RESUMED")
    
    def reset_animation(self):
        """Reset animation to beginning"""
        self.time_step = 0
        self.is_playing = False
        
        # Reset all temperatures to ambient
        for i in range(self.building.n_blocks):
            mesh = self.building[i]
            mesh["Heat"] = np.full(mesh.n_points, self.ambient_temperature)
            mesh["previous_heat"] = np.full(mesh.n_points, self.ambient_temperature)
        
        self.update_heat_data()
        self._update_visualization()
        print("🔄 Animation RESET")
    
    def change_pattern(self, pattern_name):
        """Change the heat pattern"""
        if pattern_name in self.available_patterns:
            self.current_pattern = pattern_name
            print(f"🎨 Pattern changed to: {pattern_name}")
        else:
            print(f"❌ Unknown pattern: {pattern_name}")
            print(f"Available patterns: {self.available_patterns}")
    
    def set_animation_speed(self, speed):
        """Set animation speed (0.1 to 5.0)"""
        self.animation_speed = max(0.1, min(5.0, speed))
        print(f"⚡ Animation speed set to: {self.animation_speed:.1f}x")
    
    def visualize(self, auto_start=True, update_interval=40):
        """Visualize the building with automatic updates"""
        if self.building is None:
            raise ValueError("Building not created yet. Call create_building() first.")
        
        # Initial heat data update
        self.update_heat_data()
        
        # Calculate initial temperature range
        all_temps = []
        for i in range(self.building.n_blocks):
            mesh = self.building[i]
            all_temps.extend(mesh["Heat"])
        temp_min, temp_max = np.min(all_temps), np.max(all_temps)
        
        # Add meshes to plotter
        for i in range(self.building.n_blocks):
            floor = self.building[i]
            name = self.building.get_block_name(i)
            actor = self.plotter.add_mesh(
                floor,
                scalars="Heat",
                cmap="coolwarm",
                clim=[temp_min, temp_max],
                show_edges=False,
                opacity=0.85,
                smooth_shading=True,
                label=name
            )
            self.mesh_actors[name] = actor
        
        # Add UI elements
        self.plotter.add_scalar_bar(
            title="Temperature (°C)",
            interactive=True,
            vertical=True,
            position_x=0.87,
            position_y=0.2,
            width=0.08,
            height=0.6
        )
        
        self.plotter.add_title("Dynamic Building Thermal Analysis", font_size=18, color='white')
        
        # Add keyboard controls
        self.plotter.add_key_event('space', lambda: self.toggle_animation())
        self.plotter.add_key_event('r', lambda: self.reset_animation())
        self.plotter.add_key_event('1', lambda: self.change_pattern("Dynamic Sources"))
        self.plotter.add_key_event('2', lambda: self.change_pattern("Wave Interference"))
        self.plotter.add_key_event('3', lambda: self.change_pattern("Thermal Plumes"))
        self.plotter.add_key_event('4', lambda: self.change_pattern("HVAC Cycles"))
        
        # Enhanced camera and lighting
        self.plotter.camera.elevation = 45
        self.plotter.camera.azimuth = 45
        self.plotter.add_light(pv.Light(position=(10, 10, 10), focal_point=(0, 0, 0)))
        
        # Add control instructions
        instructions = """
    Controls:
    SPACE - Play/Pause animation
    R - Reset animation
    1 - Dynamic Sources pattern
    2 - Wave Interference pattern  
    3 - Thermal Plumes pattern
    4 - HVAC Cycles pattern
    """
        self.plotter.add_text(instructions, position='upper_left', font_size=10, color='white')
        
        # Auto-start animation
        if auto_start:
            self.is_playing = True
        
        # VTK timer callback approach
        def vtk_callback(obj, event):
            if self.is_playing:
                self.time_step += 1
                self.update_heat_data()
                self._update_visualization()
        
        # Add the observer
        self.plotter.iren.add_observer('TimerEvent', vtk_callback)
        self.plotter.iren.create_timer(update_interval)
        
        print("🚀 Animation started automatically!")
        print("💡 Use keyboard controls to interact with the animation")
        print(f"🎨 Available patterns: {', '.join(self.available_patterns)}")
        
        self.plotter.show()

# Example usage
if __name__ == "__main__":
    print("🌡️ Enhanced Dynamic Building Heatmap")
    print("🎯 Using sphere animation logic for smooth patterns")
    print("⚡ Multiple pattern types available")
    
    # Create the heatmap system
    heatmap = DynamicBuildingHeatmap()
    
    # Create building
    heatmap.create_building(
        floors=4, 
        width=25, 
        depth=20, 
        floor_height=3.5, 
        shape='rectangular'
    )
    
    print("\n🚀 Starting enhanced visualization...")
    print("🎮 Use keyboard controls for interaction")
    print("🎨 Press number keys (1-4) to change patterns")
    
    # Start visualization with automatic animation
    heatmap.visualize(auto_start=True, update_interval=40)
    
    # Clean up
    heatmap.stop_updates()