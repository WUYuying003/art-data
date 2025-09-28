


# Data-Driven Ocean Flower Art Generator
# Interactive visualization of Iris dataset as beautiful, ocean-inspired flowers using pygame

import pygame
import math
import sys
import csv
import random
import cv2
import numpy as np
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Global settings
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (0, 0, 0)  # Pure black background
FPS = 60
FONT_SIZE = 24

# Color constants
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# 颜色常量
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class IrisData:
    """Iris dataset processing class"""
    
    def __init__(self, csv_file_path: str):
        self.data = []
        self.species_data = {'Iris-setosa': [], 'Iris-versicolor': [], 'Iris-virginica': []}
        self.load_data(csv_file_path)
        self.normalize_data()
    
    def load_data(self, csv_file_path: str):
        """Load CSV data"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    iris_sample = {
                        'id': int(row['Id']),
                        'sepal_length': float(row['SepalLengthCm']),
                        'sepal_width': float(row['SepalWidthCm']),
                        'petal_length': float(row['PetalLengthCm']),
                        'petal_width': float(row['PetalWidthCm']),
                        'species': row['Species']
                    }
                    self.data.append(iris_sample)
                    self.species_data[iris_sample['species']].append(iris_sample)
        except FileNotFoundError:
            print(f"Data file {csv_file_path} not found")
            sys.exit(1)
    
    def normalize_data(self):
        """Normalize data to 0-1 range"""
        if not self.data:
            return
        
        # Get min and max values for each feature
        features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        min_max = {}
        
        for feature in features:
            values = [sample[feature] for sample in self.data]
            min_max[feature] = {'min': min(values), 'max': max(values)}
        
        # Normalize each sample
        for sample in self.data:
            sample['normalized'] = {}
            for feature in features:
                min_val = min_max[feature]['min']
                max_val = min_max[feature]['max']
                normalized_val = (sample[feature] - min_val) / (max_val - min_val)
                sample['normalized'][feature] = normalized_val
    
    def get_sample_by_index(self, index: int) -> Optional[Dict]:
        """Get sample by index"""
        if 0 <= index < len(self.data):
            return self.data[index]
        return None
    
    def get_species_samples(self, species: str) -> List[Dict]:
        """Get all samples of a specific species"""
        return self.species_data.get(species, [])
    
    def get_random_sample(self, species: Optional[str] = None) -> Dict:
        """Get random sample"""
        if species:
            samples = self.species_data.get(species, [])
            return random.choice(samples) if samples else self.data[0]
        return random.choice(self.data)

class FlowerVisualizer:
    """Flower visualization class"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
    
    def get_species_color_scheme(self, species: str) -> Dict[str, Tuple[int, int, int]]:
        """Get color scheme based on iris species"""
        color_schemes = {
            'Iris-setosa': {
                'primary': (30, 144, 255),    # Dodger blue
                'secondary': (0, 191, 255),   # Deep sky blue
                'accent': (135, 206, 250),    # Light sky blue
                'highlight': (173, 216, 230)  # Light blue
            },
            'Iris-versicolor': {
                'primary': (0, 206, 209),     # Dark turquoise
                'secondary': (64, 224, 208),  # Turquoise
                'accent': (72, 209, 204),     # Medium turquoise
                'highlight': (175, 238, 238)  # Pale turquoise
            },
            'Iris-virginica': {
                'primary': (138, 43, 226),    # Blue violet
                'secondary': (148, 0, 211),   # Dark violet
                'accent': (186, 85, 211),     # Medium orchid
                'highlight': (221, 160, 221)  # Plum
            }
        }
        return color_schemes.get(species, color_schemes['Iris-setosa'])
    
    def get_enhanced_color_schemes(self) -> Dict[str, Dict[str, Tuple[int, int, int]]]:
        """Get all enhanced color schemes for UI selection"""
        return {
            'Ocean Blues': {
                'primary': (30, 144, 255),    # Dodger blue
                'secondary': (0, 191, 255),   # Deep sky blue
                'accent': (135, 206, 250),    # Light sky blue
                'highlight': (173, 216, 230)  # Light blue
            },
            'Sunset Orange': {
                'primary': (255, 69, 0),      # Red orange
                'secondary': (255, 140, 0),   # Dark orange
                'accent': (255, 165, 0),      # Orange
                'highlight': (255, 218, 185)  # Peach puff
            },
            'Forest Green': {
                'primary': (34, 139, 34),     # Forest green
                'secondary': (0, 128, 0),     # Green
                'accent': (144, 238, 144),    # Light green
                'highlight': (240, 255, 240)  # Honeydew
            },
            'Royal Purple': {
                'primary': (75, 0, 130),      # Indigo
                'secondary': (138, 43, 226),  # Blue violet
                'accent': (186, 85, 211),     # Medium orchid
                'highlight': (238, 130, 238)  # Violet
            },
            'Rose Pink': {
                'primary': (220, 20, 60),     # Crimson
                'secondary': (255, 20, 147),  # Deep pink
                'accent': (255, 105, 180),    # Hot pink
                'highlight': (255, 182, 193)  # Light pink
            },
            'Golden Yellow': {
                'primary': (255, 215, 0),     # Gold
                'secondary': (255, 165, 0),   # Orange
                'accent': (255, 255, 0),      # Yellow
                'highlight': (255, 255, 224)  # Light yellow
            },
            'Deep Teal': {
                'primary': (0, 128, 128),     # Teal
                'secondary': (0, 206, 209),   # Dark turquoise
                'accent': (64, 224, 208),     # Turquoise
                'highlight': (175, 238, 238)  # Pale turquoise
            },
            'Cosmic Purple': {
                'primary': (72, 61, 139),     # Dark slate blue
                'secondary': (123, 104, 238), # Medium slate blue
                'accent': (147, 112, 219),    # Medium purple
                'highlight': (230, 230, 250)  # Lavender
            }
        }
    
    def map_data_to_visual(self, sample):
        """Map iris data to visual parameters with beautiful variation"""
        # Extract features from sample dict
        if isinstance(sample, dict):
            sepal_length = sample['sepal_length']
            sepal_width = sample['sepal_width']
            petal_length = sample['petal_length']
            petal_width = sample['petal_width']
        else:
            sepal_length, sepal_width, petal_length, petal_width = sample
        
        # Beautiful parameter mapping (restored to original elegant ranges)
        base_radius = int(80 + sepal_length * 8)  # Range: 80-140 (elegant size)
        num_petals = max(16, min(24, int(16 + petal_length * 2)))  # Range: 16-24 (balanced)
        amplitude = int(40 + petal_width * 20)  # Range: 40-80 (smooth waves)
        num_layers = max(6, min(12, int(6 + sepal_width * 2)))  # Range: 6-12 (layered beauty)
        
        # Add random seed for variety while keeping elegant shapes
        import random
        sample_seed = hash(str(sample)) % 1000  # Consistent seed per sample
        random.seed(sample_seed)
        
        # Small random variations for uniqueness (but keeping elegance)
        radius_variation = random.randint(-10, 10)
        petal_variation = random.randint(-2, 2)
        amplitude_variation = random.randint(-5, 5)
        
        return {
            'base_radius': max(60, base_radius + radius_variation),
            'num_petals': max(12, min(28, num_petals + petal_variation)),
            'amplitude': max(30, amplitude + amplitude_variation),
            'num_layers': num_layers
        }
    
    def get_sample_color_scheme(self, iris_sample: Dict, custom_scheme: str = None) -> Dict[str, Tuple[int, int, int]]:
        """Get color scheme for a specific sample, with optional custom scheme override"""
        if custom_scheme:
            schemes = self.get_enhanced_color_schemes()
            return schemes.get(custom_scheme, schemes['Ocean Blues'])
        
        # Use sample-specific color variation
        visual_params = self.map_data_to_visual(iris_sample)
        color_variation = visual_params['color_variation']
        
        all_schemes = list(self.get_enhanced_color_schemes().values())
        return all_schemes[color_variation]

        return visual_params
    
    def get_dynamic_color(self, colors: Dict, t: int, layer_ratio: float) -> Tuple[int, int, int]:
        """Get dynamically changing color within the current color scheme"""
        # Color blending based on time and layer - restored beautiful color cycling
        time_cycle = (t * 0.01) % 1
        
        # Cycle through different colors over time within the current color scheme
        if time_cycle < 0.25:
            # Primary to secondary
            ratio = time_cycle * 4
            color = self.gradient_color(colors['primary'], colors['secondary'], ratio)
        elif time_cycle < 0.5:
            # Secondary to accent
            ratio = (time_cycle - 0.25) * 4
            color = self.gradient_color(colors['secondary'], colors['accent'], ratio)
        elif time_cycle < 0.75:
            # Accent to highlight
            ratio = (time_cycle - 0.5) * 4
            color = self.gradient_color(colors['accent'], colors['highlight'], ratio)
        else:
            # Highlight back to primary
            ratio = (time_cycle - 0.75) * 4
            color = self.gradient_color(colors['highlight'], colors['primary'], ratio)
        
        # Add layer variation for depth
        layer_intensity = 1.0 - layer_ratio * 0.3
        color = tuple([int(c * layer_intensity) for c in color])
        
        return color
    
    def gradient_color(self, start: Tuple[int, int, int], end: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Color gradient interpolation"""
        return tuple([int(start[i] + (end[i] - start[i]) * ratio) for i in range(3)])
    
    def blend_color_schemes(self, scheme1: Dict, scheme2: Dict, ratio: float) -> Dict:
        """Blend two color schemes smoothly with easing"""
        # Apply smooth easing function for more natural color transitions
        eased_ratio = ratio * ratio * (3.0 - 2.0 * ratio)  # Smoothstep function
        
        blended_scheme = {}
        for key in scheme1:
            if key in scheme2:
                blended_scheme[key] = self.gradient_color(scheme1[key], scheme2[key], eased_ratio)
            else:
                blended_scheme[key] = scheme1[key]
        return blended_scheme
    
    def draw_data_driven_flower(self, surface, x, y, params, colors, t, mouse_clicks=None, scale_factor=1.0):
        """Draw beautiful iris flower with elegant patterns (restored original beauty)"""
        base_radius = int(params['base_radius'] * scale_factor)
        num_petals = params['num_petals']
        amplitude = int(params['amplitude'] * scale_factor)
        num_layers = params['num_layers']
        
        # Draw multi-layer petals with original beautiful patterns
        for layer in range(num_layers):
            layer_ratio = layer / (num_layers - 1) if num_layers > 1 else 0
            
            # Elegant dynamic radius calculation (restored)
            dynamic_radius = base_radius + layer * 15
            dynamic_radius += int(amplitude * 0.3 * math.sin(t * 0.08 + layer))
            dynamic_radius += int(amplitude * 0.2 * math.cos(t * 0.06 + layer * 0.5))
            
            # Get current layer color with enhanced mouse interaction effects
            color_time_offset = t + layer * 10  # Restore layer-based color variation
            
            # Add mouse click color effects with enhanced visual feedback
            if mouse_clicks:
                for click in mouse_clicks:
                    # Calculate distance from flower center to click
                    center_dist = math.sqrt((x - click['x'])**2 + (y - click['y'])**2)
                    if center_dist < 300:  # Color effect radius
                        # Add time-based color shift based on click - enhanced effect
                        click_color_offset = click['strength'] * 15 * math.sin((t - click['time']) * 0.08)
                        color_time_offset += click_color_offset
            
            current_color = self.get_dynamic_color(colors, color_time_offset, layer_ratio)
            
            # Draw beautiful petals (restored original elegance)
            for petal in range(num_petals):
                angle = 2 * math.pi * petal / num_petals + t * 0.02 + layer * 0.1
                
                points = []
                for i in range(120):
                    theta = angle + math.pi * i / 120
                    
                    # Beautiful petal shape calculation (restored)
                    r = dynamic_radius
                    r += int(amplitude * 0.4 * math.sin(6 * theta + t * 0.05 + layer))
                    r -= int(amplitude * 0.2 * math.cos(3 * theta + t * 0.03 + layer))
                    r += int(amplitude * 0.3 * math.sin(9 * theta + t * 0.02))
                    
                    # Elegant tidal effect (restored)
                    tidal_phase = t * 0.05 + layer * 0.02 + angle
                    tidal_effect = amplitude * 0.5 * math.sin(tidal_phase)
                    r += int(tidal_effect)
                    
                    # Mouse interaction effects
                    if mouse_clicks:
                        for click in mouse_clicks:
                            # Calculate position for this point
                            point_x = x + r * math.cos(theta + layer * 0.03)
                            point_y = y + r * math.sin(theta + layer * 0.03)
                            
                            # Calculate distance from click
                            dist = math.sqrt((point_x - click['x'])**2 + (point_y - click['y'])**2)
                            
                            # Apply deformation based on distance and click strength
                            if dist < 200:  # Effect radius
                                effect_strength = click['strength'] * (1 - dist / 200)
                                
                                # Create more dramatic ripple effect with faster animation
                                ripple_speed = 5  # Faster ripple propagation
                                ripple = math.sin((dist - (t - click['time']) * ripple_speed) * 0.15) * effect_strength
                                r += int(50 * ripple)  # Stronger ripple effect
                                
                                # Add more pronounced spiral distortion with faster decay
                                spiral_speed = 0.15  # Faster spiral animation
                                spiral_offset = effect_strength * 0.5 * math.sin(theta * 4 + (t - click['time']) * spiral_speed)
                                r += int(35 * spiral_offset)  # Stronger spiral effect
                                
                                # Add pulsing effect for more dynamic appearance
                                pulse = effect_strength * 0.3 * math.sin((t - click['time']) * 0.2)
                                r += int(25 * pulse)
                    
                    px = x + r * math.cos(theta + layer * 0.03)
                    py = y + r * math.sin(theta + layer * 0.03)
                    points.append((px, py))
                
                if len(points) > 2:
                    try:
                        pygame.draw.aalines(surface, current_color, False, points, 1)
                    except:
                        # Fallback to regular lines if antialiasing fails
                        pygame.draw.lines(surface, current_color, False, points, 1)
        
        # Remove the center core drawing - no more center circle!
    
    def draw_center_core(self, screen, colors: Dict, t: int, cx: int, cy: int, radius: int):
        """Draw flower center core"""
        for i in range(radius, 0, -2):
            ratio = (radius - i) / radius
            center_color = self.get_dynamic_color(colors, t * 2, ratio)
            pygame.draw.circle(screen, center_color, (cx, cy), i)

class InteractiveFlowerApp:
    """Interactive flower application main class"""
    
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Data-Driven Ocean Flowers - Iris Dataset Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        
        # Load data
        self.iris_data = IrisData("Iris data.csv")
        self.visualizer = FlowerVisualizer(WIDTH - 300, HEIGHT)  # Reserve space for UI
        
        # Application state
        self.current_sample_index = 0
        self.current_species_filter = None  # None means show all species
        self.is_playing = True
        self.t = 0
        self.auto_advance = False
        self.auto_advance_timer = 0
        self.auto_advance_delay = 120  # 2 seconds (60 FPS * 2)
        
        # UI state
        self.species_list = ['All', 'Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
        self.selected_species_index = 0
        
        # Color scheme selection
        self.color_schemes = list(self.visualizer.get_enhanced_color_schemes().keys())
        self.selected_color_index = 0
        self.custom_color_mode = True  # Start in manual mode so users can see color switching
        self.color_change_offset = 0  # Color animation offset for smooth transitions
        
        # Video recording
        self.is_recording = False
        self.video_writer = None
        self.video_frames = []
        self.recording_duration = 3600  # 60 seconds at 60 FPS (1 minute)
        self.recording_frame_count = 0
        
        # Mouse interaction
        self.mouse_clicks = []  # Store recent mouse clicks
        self.click_effects = []  # Store active click effects
        self.max_click_history = 10  # Maximum number of clicks to remember
        self.click_effect_duration = 60  # 1 second at 60 FPS (faster visual effect)
        self.click_deform_duration = 120  # 2 seconds at 60 FPS (faster deformation recovery)
        
        # Color transition system triggered by mouse clicks
        self.color_transition_active = False
        self.color_transition_progress = 0.0
        self.color_transition_speed = 0.015  # Slower for smoother gradient
        self.current_colors = None
        self.target_colors = None
        self.color_transition_duration = 180  # 3 seconds at 60 FPS for gradual color change
        
        # Auto scaling animation
        self.scale_animation_speed = 0.06  # Slightly slower for smoother breathing (was 0.08)
        self.scale_range = 0.25  # Slightly smaller range for more natural breathing (was 0.3)
        
        # Initialize color system
        self.initialize_color_system()
    
    def initialize_color_system(self):
        """Initialize the color system with starting colors"""
        all_schemes = self.visualizer.get_enhanced_color_schemes()
        current_scheme_name = self.color_schemes[self.selected_color_index]
        self.current_colors = all_schemes[current_scheme_name].copy()
        self.target_colors = self.current_colors.copy()
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Space: switch to next color scheme
                    self.next_color_scheme()
                
                elif event.key == pygame.K_LEFT:
                    # Left arrow: previous sample
                    self.previous_sample()
                
                elif event.key == pygame.K_RIGHT:
                    # Right arrow: next sample  
                    self.next_sample()
                
                elif event.key == pygame.K_UP:
                    # Up arrow: previous species
                    self.previous_species()
                
                elif event.key == pygame.K_DOWN:
                    # Down arrow: next species
                    self.next_species()
                
                elif event.key == pygame.K_r:
                    # R key: random sample
                    self.random_sample()
                
                elif event.key == pygame.K_a:
                    # A key: toggle auto advance
                    self.auto_advance = not self.auto_advance
                    self.auto_advance_timer = 0
                
                elif event.key == pygame.K_c:
                    # C key: toggle color mode
                    self.custom_color_mode = not self.custom_color_mode
                
                elif event.key == pygame.K_1:
                    # 1 key: previous color scheme
                    if self.custom_color_mode:
                        self.previous_color_scheme()
                
                elif event.key == pygame.K_2:
                    # 2 key: next color scheme
                    if self.custom_color_mode:
                        self.next_color_scheme()
                
                elif event.key == pygame.K_v:
                    # V key: start/stop video recording
                    self.toggle_video_recording()
                
                elif event.key == pygame.K_x:
                    # X key: clear all mouse effects
                    self.clear_mouse_effects()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_mouse_click(event.pos)
        
        return True
    
    def previous_sample(self):
        """Switch to previous sample"""
        # Clear mouse interaction effects when switching samples
        self.clear_mouse_effects()
        
        if self.current_species_filter:
            samples = self.iris_data.get_species_samples(self.current_species_filter)
            if samples:
                current_sample = self.iris_data.get_sample_by_index(self.current_sample_index)
                current_index_in_species = samples.index(current_sample) if current_sample in samples else 0
                new_index = (current_index_in_species - 1) % len(samples)
                self.current_sample_index = samples[new_index]['id'] - 1
        else:
            self.current_sample_index = (self.current_sample_index - 1) % len(self.iris_data.data)
    
    def next_sample(self):
        """Switch to next sample"""
        # Clear mouse interaction effects when switching samples
        self.clear_mouse_effects()
        
        if self.current_species_filter:
            samples = self.iris_data.get_species_samples(self.current_species_filter)
            if samples:
                current_sample = self.iris_data.get_sample_by_index(self.current_sample_index)
                current_index_in_species = samples.index(current_sample) if current_sample in samples else 0
                new_index = (current_index_in_species + 1) % len(samples)
                self.current_sample_index = samples[new_index]['id'] - 1
        else:
            self.current_sample_index = (self.current_sample_index + 1) % len(self.iris_data.data)
    
    def previous_species(self):
        """Switch to previous species"""
        self.selected_species_index = (self.selected_species_index - 1) % len(self.species_list)
        self.update_species_filter()
    
    def next_species(self):
        """Switch to next species"""
        self.selected_species_index = (self.selected_species_index + 1) % len(self.species_list)
        self.update_species_filter()
    
    def update_species_filter(self):
        """Update species filter"""
        # Clear mouse interaction effects when switching species
        self.clear_mouse_effects()
        
        selected_species = self.species_list[self.selected_species_index]
        if selected_species == 'All':
            self.current_species_filter = None
        else:
            self.current_species_filter = selected_species
            # Switch to first sample of this species
            samples = self.iris_data.get_species_samples(selected_species)
            if samples:
                self.current_sample_index = samples[0]['id'] - 1
    
    def random_sample(self):
        """Randomly select sample"""
        # Clear mouse interaction effects when switching to random sample
        self.clear_mouse_effects()
        
        if self.current_species_filter:
            sample = self.iris_data.get_random_sample(self.current_species_filter)
        else:
            sample = self.iris_data.get_random_sample()
        self.current_sample_index = sample['id'] - 1
    
    def update_auto_advance(self):
        """Update auto advance"""
        if self.auto_advance and self.is_playing:
            self.auto_advance_timer += 1
            if self.auto_advance_timer >= self.auto_advance_delay:
                self.next_sample()
                self.auto_advance_timer = 0
    
    def previous_color_scheme(self):
        """Switch to previous color scheme"""
        self.selected_color_index = (self.selected_color_index - 1) % len(self.color_schemes)
        # Enable custom color mode when manually switching
        self.custom_color_mode = True
        # Start color transition to the selected scheme
        self.start_color_transition(target_index=self.selected_color_index)
    
    def next_color_scheme(self):
        """Switch to next color scheme"""
        self.selected_color_index = (self.selected_color_index + 1) % len(self.color_schemes)
        # Enable custom color mode when manually switching
        self.custom_color_mode = True
        # Start color transition to the selected scheme
        self.start_color_transition(target_index=self.selected_color_index)
    
    def get_current_color_scheme_name(self):
        """Get current color scheme name"""
        if self.custom_color_mode:
            return self.color_schemes[self.selected_color_index]
        else:
            # In auto mode, use the first color scheme as default
            return self.color_schemes[0] if self.color_schemes else "Ocean Depths"
    
    def toggle_video_recording(self):
        """Start or stop video recording"""
        if not self.is_recording:
            self.start_video_recording()
        else:
            self.stop_video_recording()
    
    def start_video_recording(self):
        """Start recording video"""
        self.is_recording = True
        self.video_frames = []
        self.recording_frame_count = 0
        print("Video recording started...")
    
    def stop_video_recording(self):
        """Stop recording and save video"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        if len(self.video_frames) == 0:
            print("No frames to save")
            return
        
        # Create videos directory if it doesn't exist
        if not os.path.exists("videos"):
            os.makedirs("videos")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_sample = self.iris_data.get_sample_by_index(self.current_sample_index)
        species_name = current_sample['species'].replace('Iris-', '') if current_sample else "unknown"
        sample_id = current_sample['id'] if current_sample else 0
        
        filename = f"videos/iris_flower_{species_name}_sample{sample_id}_{timestamp}.mp4"
        
        # Video settings
        fps = 30  # Reduce to 30 FPS for better compatibility
        height, width = self.video_frames[0].shape[:2]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        
        # Write frames
        for frame in self.video_frames:
            # Convert from RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video_writer.write(frame_bgr)
        
        video_writer.release()
        print(f"Video saved as: {filename}")
        print(f"Recorded {len(self.video_frames)} frames ({len(self.video_frames)/fps:.1f} seconds)")
    
    def capture_frame(self):
        """Capture current frame for video recording"""
        if self.is_recording:
            # Convert pygame surface to numpy array
            frame_data = pygame.surfarray.array3d(self.screen)
            # Transpose to get correct orientation (pygame uses (width, height, channels))
            frame_data = np.transpose(frame_data, (1, 0, 2))
            self.video_frames.append(frame_data)
            self.recording_frame_count += 1
            
            # Auto-stop after recording_duration frames
            if self.recording_frame_count >= self.recording_duration:
                self.stop_video_recording()
    
    def handle_mouse_click(self, pos):
        """Handle mouse click and create visual effect with color transition"""
        x, y = pos
        
        # Only respond to clicks in the main visualization area (not UI)
        if x < WIDTH - 300:
            click_effect = {
                'x': x,
                'y': y,
                'age': 0,
                'intensity': 1.0,
                'radius': 0
            }
            self.click_effects.append(click_effect)
            
            # Store click for flower deformation
            click_data = {
                'x': x,
                'y': y,
                'time': self.t,
                'strength': 1.0
            }
            self.mouse_clicks.append(click_data)
            
            # Trigger color transition to next color scheme
            self.start_color_transition()
            
            # Remove old clicks
            if len(self.mouse_clicks) > self.max_click_history:
                self.mouse_clicks.pop(0)
    
    def start_color_transition(self, target_index=None):
        """Start a smooth color transition to the next color scheme or specified index"""
        if not self.color_transition_active:  # Don't start new transition if one is already in progress
            if target_index is None:
                # Move to next color scheme (for mouse clicks)
                self.selected_color_index = (self.selected_color_index + 1) % len(self.color_schemes)
            # If target_index is specified, use current selected_color_index (for manual switches)
            
            # Set up transition
            all_schemes = self.visualizer.get_enhanced_color_schemes()
            new_scheme_name = self.color_schemes[self.selected_color_index]
            self.target_colors = all_schemes[new_scheme_name].copy()
            
            # Start transition
            self.color_transition_active = True
            self.color_transition_progress = 0.0
    
    def update_color_transition(self):
        """Update the gradual color transition between color schemes"""
        if self.color_transition_active:
            self.color_transition_progress += self.color_transition_speed
            
            # Apply easing function for smoother transition
            eased_progress = self.color_transition_progress * self.color_transition_progress * (3.0 - 2.0 * self.color_transition_progress)
            
            # Blend color schemes (not individual colors, but entire schemes)
            blended_colors = {}
            for key in self.current_colors:
                if key in self.target_colors:
                    start_color = self.current_colors[key]
                    end_color = self.target_colors[key]
                    blended_colors[key] = self.visualizer.gradient_color(start_color, end_color, eased_progress)
                else:
                    blended_colors[key] = self.current_colors[key]
            
            # Update current colors with blended result - this becomes the base color scheme
            self.current_colors = blended_colors
            
            # Check if transition is complete
            if self.color_transition_progress >= 1.0:
                self.color_transition_active = False
                self.color_transition_progress = 0.0
                self.current_colors = self.target_colors.copy()
    
    def update_click_effects(self):
        """Update and age click effects"""
        for effect in self.click_effects[:]:  # Copy list to safely modify during iteration
            effect['age'] += 1
            effect['intensity'] = 1.0 - (effect['age'] / self.click_effect_duration)
            effect['radius'] = effect['age'] * 2
            
            # Remove expired effects
            if effect['age'] >= self.click_effect_duration:
                self.click_effects.remove(effect)
        
        # Age mouse clicks
        for click in self.mouse_clicks[:]:
            click['strength'] = max(0, 1.0 - (self.t - click['time']) / self.click_deform_duration)  # Faster decay
            if click['strength'] <= 0:
                self.mouse_clicks.remove(click)
    
    def clear_mouse_effects(self):
        """Clear all mouse interaction effects"""
        self.mouse_clicks.clear()
        self.click_effects.clear()
    
    def draw_click_effects(self, screen):
        """Draw visual effects from mouse clicks"""
        for effect in self.click_effects:
            if effect['intensity'] > 0:
                # Draw expanding circle
                alpha = int(255 * effect['intensity'])
                color = (255, 255, 255, alpha)
                
                # Create a surface with per-pixel alpha
                effect_surface = pygame.Surface((effect['radius'] * 2, effect['radius'] * 2), pygame.SRCALPHA)
                
                # Draw outer ring
                if effect['radius'] > 5:
                    pygame.draw.circle(effect_surface, (*color[:3], alpha//2), 
                                     (effect['radius'], effect['radius']), 
                                     int(effect['radius']), 3)
                
                # Draw inner glow
                if effect['radius'] > 2:
                    pygame.draw.circle(effect_surface, (*color[:3], alpha//4), 
                                     (effect['radius'], effect['radius']), 
                                     int(effect['radius']//2))
                
                # Blit to screen
                screen.blit(effect_surface, (effect['x'] - effect['radius'], effect['y'] - effect['radius']))
    
    def draw_ui(self, screen):
        """Draw user interface"""
        # UI background area
        ui_rect = pygame.Rect(WIDTH - 300, 0, 300, HEIGHT)
        pygame.draw.rect(screen, (20, 20, 20), ui_rect)
        pygame.draw.line(screen, WHITE, (WIDTH - 300, 0), (WIDTH - 300, HEIGHT), 2)
        
        # Current sample information
        current_sample = self.iris_data.get_sample_by_index(self.current_sample_index)
        if current_sample:
            y_offset = 20
            
            # Title
            title_text = self.font.render("Iris Data Visualization", True, WHITE)
            screen.blit(title_text, (WIDTH - 290, y_offset))
            y_offset += 40
            
            # Sample ID and species
            sample_info = f"Sample #{current_sample['id']}"
            species_name = current_sample['species'].replace('Iris-', '')
            
            sample_text = self.font.render(sample_info, True, WHITE)
            screen.blit(sample_text, (WIDTH - 290, y_offset))
            y_offset += 25
            
            species_text = self.font.render(f"Species: {species_name}", True, LIGHT_GRAY)
            screen.blit(species_text, (WIDTH - 290, y_offset))
            y_offset += 35
            
            # Feature data
            features = [
                ("Sepal Length", f"{current_sample['sepal_length']:.1f} cm"),
                ("Sepal Width", f"{current_sample['sepal_width']:.1f} cm"),
                ("Petal Length", f"{current_sample['petal_length']:.1f} cm"),
                ("Petal Width", f"{current_sample['petal_width']:.1f} cm")
            ]
            
            for feature_name, value in features:
                feature_text = self.font.render(f"{feature_name}: {value}", True, GRAY)
                screen.blit(feature_text, (WIDTH - 290, y_offset))
                y_offset += 25
            
            y_offset += 20
            
            # Species filter
            filter_title = self.font.render("Species Filter:", True, WHITE)
            screen.blit(filter_title, (WIDTH - 290, y_offset))
            y_offset += 30
            
            for i, species in enumerate(self.species_list):
                color = WHITE if i == self.selected_species_index else GRAY
                display_name = species if species == 'All' else species.replace('Iris-', '')
                species_text = self.font.render(f"{'>' if i == self.selected_species_index else ' '} {display_name}", True, color)
                screen.blit(species_text, (WIDTH - 280, y_offset))
                y_offset += 25
            
            y_offset += 20
            
            # Color scheme controls
            color_title = self.font.render("Color Controls:", True, WHITE)
            screen.blit(color_title, (WIDTH - 290, y_offset))
            y_offset += 25
            
            mode_text = "Manual" if self.custom_color_mode else "Auto"
            mode_color = (0, 255, 0) if self.custom_color_mode else (255, 165, 0)
            mode_surface = self.font.render(f"Mode: {mode_text}", True, mode_color)
            screen.blit(mode_surface, (WIDTH - 290, y_offset))
            y_offset += 25
            
            if self.custom_color_mode:
                current_scheme = self.color_schemes[self.selected_color_index]
                scheme_surface = self.font.render(f"Theme: {current_scheme}", True, LIGHT_GRAY)
                screen.blit(scheme_surface, (WIDTH - 290, y_offset))
                y_offset += 25
                
                # Draw color preview squares
                scheme_colors = self.visualizer.get_enhanced_color_schemes()[current_scheme]
                preview_y = y_offset
                for i, (color_name, color) in enumerate(scheme_colors.items()):
                    rect_x = WIDTH - 290 + i * 35
                    rect = pygame.Rect(rect_x, preview_y, 30, 15)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
                y_offset += 25
            else:
                auto_text = self.font.render("Auto: Each sample has", True, GRAY)
                screen.blit(auto_text, (WIDTH - 290, y_offset))
                y_offset += 20
                auto_text2 = self.font.render("unique colors", True, GRAY)
                screen.blit(auto_text2, (WIDTH - 290, y_offset))
                y_offset += 20
            
            y_offset += 10
            
            # Control instructions
            controls = [
                "Controls:",
                "Space: Pause/Resume",
                "←/→: Switch Sample",
                "↑/↓: Switch Species",
                "R: Random Sample",
                "A: Auto Advance",
                "C: Toggle Color Mode",
                "1/2: Change Color Theme",
                "V: Record Video (5s)",
                "Click: Switch color scheme",
                "Mouse: Click to deform",
                "X: Clear deformations"
            ]
            
            for i, control in enumerate(controls):
                color = WHITE if i == 0 else GRAY
                control_text = self.font.render(control, True, color)
                screen.blit(control_text, (WIDTH - 290, y_offset))
                y_offset += 25
            
            # Status indicators
            y_offset += 20
            status_items = []
            if not self.is_playing:
                status_items.append("PAUSED")
            if self.auto_advance:
                status_items.append("AUTO")
            if self.is_recording:
                progress = (self.recording_frame_count / self.recording_duration) * 100
                status_items.append(f"RECORDING {progress:.0f}%")
            
            if status_items:
                status_text = " | ".join(status_items)
                status_color = (255, 0, 0) if self.is_recording else (255, 255, 0)
                status_surface = self.font.render(status_text, True, status_color)
                screen.blit(status_surface, (WIDTH - 290, y_offset))
    
    def run(self):
        """Main execution loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update state
            if self.is_playing:
                self.t += 1
            
            # Update color transition system
            self.update_color_transition()
            
            self.update_auto_advance()
            
            # Update click effects
            self.update_click_effects()
            
            # Render
            self.screen.fill(BG_COLOR)
            
            # Draw current flower with mouse interaction
            current_sample = self.iris_data.get_sample_by_index(self.current_sample_index)
            if current_sample:
                # Use current transitioning colors as the base color scheme
                # The get_dynamic_color method will create color variations within this scheme
                colors = self.current_colors
                
                # Map sample data to visual parameters
                visual_params = self.visualizer.map_data_to_visual(current_sample)
                
                # Center the flower in the left display area (not entire screen)
                display_area_width = self.width - 300  # Left area excluding UI panel
                center_x = display_area_width // 2
                center_y = self.height // 2
                
                # Calculate smoother auto scaling factor (breathing effect using cosine for smoothness)
                breathing_cycle = self.t * self.scale_animation_speed
                # Use cosine for smoother breathing, with easing function
                raw_scale = math.cos(breathing_cycle)
                # Apply easing function for even smoother transitions
                eased_scale = raw_scale * raw_scale * raw_scale  # Cubic easing
                scale_factor = 1.0 + self.scale_range * eased_scale
                
                # Pass mouse data and scale factor for animation
                self.visualizer.draw_data_driven_flower(self.screen, center_x, center_y, visual_params, colors, self.t, self.mouse_clicks, scale_factor)
            
            # Draw click effects
            self.draw_click_effects(self.screen)
            
            # Draw UI
            self.draw_ui(self.screen)
            
            # Capture frame for video recording if recording
            self.capture_frame()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        
        # Clean up any ongoing recording
        if self.is_recording:
            self.stop_video_recording()
        
        sys.exit()

def main():
    """Main function"""
    try:
        app = InteractiveFlowerApp()
        app.run()
    except Exception as e:
        import traceback
        print(f"Program error: {e}")
        print("Detailed traceback:")
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
