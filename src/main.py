


# Data-Driven Ocean Flower Art Generator
# Interactive visualization of Iris dataset as beautiful, ocean-inspired flowers using pygame

import pygame
import math
import sys
import csv
import random
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
                'primary': (0, 120, 200),    # Ocean blue
                'secondary': (20, 140, 220),  # Light ocean blue
                'accent': (40, 160, 240),     # Bright blue
                'highlight': (100, 200, 255)  # Bright blue-white
            },
            'Iris-versicolor': {
                'primary': (0, 180, 140),     # Teal
                'secondary': (20, 200, 160),  # Light teal
                'accent': (40, 220, 180),     # Bright teal
                'highlight': (100, 240, 200)  # Bright teal-white
            },
            'Iris-virginica': {
                'primary': (160, 0, 120),     # Purple-magenta
                'secondary': (180, 20, 140),  # Light purple-magenta
                'accent': (200, 40, 160),     # Bright purple-magenta
                'highlight': (220, 100, 200)  # Bright purple-white
            }
        }
        return color_schemes.get(species, color_schemes['Iris-setosa'])
    
    def map_data_to_visual(self, iris_sample: Dict) -> Dict:
        """Map iris data to visual parameters"""
        normalized = iris_sample['normalized']
        
        # Data mapping strategy
        visual_params = {
            'base_radius': 40 + int(normalized['sepal_length'] * 120),  # Sepal length → Base radius
            'num_petals': 16 + int(normalized['sepal_width'] * 16),     # Sepal width → Number of petals
            'amplitude': 20 + int(normalized['petal_length'] * 60),     # Petal length → Dynamic amplitude
            'num_layers': 6 + int(normalized['petal_width'] * 12),      # Petal width → Number of layers
            'species': iris_sample['species']
        }
        
        return visual_params

        return visual_params
    
    def get_dynamic_color(self, colors: Dict, t: int, layer_ratio: float) -> Tuple[int, int, int]:
        """Get dynamically changing color"""
        # Color blending based on time and layer
        time_cycle = (t * 0.01) % 1
        
        # Cycle through different colors over time
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
        
        # Add layer variation
        layer_intensity = 1.0 - layer_ratio * 0.3
        color = tuple([int(c * layer_intensity) for c in color])
        
        return color
    
    def gradient_color(self, start: Tuple[int, int, int], end: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Color gradient interpolation"""
        return tuple([int(start[i] + (end[i] - start[i]) * ratio) for i in range(3)])
    
    def draw_data_driven_flower(self, screen, iris_sample: Dict, t: int, x_offset: int = 0, y_offset: int = 0):
        """Draw flower based on iris data"""
        if not iris_sample:
            return
        
        visual_params = self.map_data_to_visual(iris_sample)
        colors = self.get_species_color_scheme(visual_params['species'])
        
        cx = self.center_x + x_offset
        cy = self.center_y + y_offset
        
        num_petals = visual_params['num_petals']
        num_layers = visual_params['num_layers']
        base_radius = visual_params['base_radius']
        amplitude = visual_params['amplitude']
        
        # Draw multi-layer petals
        for layer in range(num_layers):
            layer_ratio = layer / (num_layers - 1) if num_layers > 1 else 0
            
            # Dynamic radius calculation
            dynamic_radius = base_radius + layer * 15
            dynamic_radius += int(amplitude * 0.3 * math.sin(t * 0.08 + layer))
            dynamic_radius += int(amplitude * 0.2 * math.cos(t * 0.06 + layer * 0.5))
            
            # Get current layer color
            current_color = self.get_dynamic_color(colors, t + layer * 10, layer_ratio)
            
            # Draw petals
            for petal in range(num_petals):
                angle = 2 * math.pi * petal / num_petals + t * 0.02 + layer * 0.1
                
                points = []
                for i in range(120):  # Reduced points for better performance
                    theta = angle + math.pi * i / 120
                    
                    # Petal shape calculation
                    r = dynamic_radius
                    r += int(amplitude * 0.4 * math.sin(6 * theta + t * 0.05 + layer))
                    r -= int(amplitude * 0.2 * math.cos(3 * theta + t * 0.03 + layer))
                    r += int(amplitude * 0.3 * math.sin(9 * theta + t * 0.02))
                    
                    # Tidal effect (data-based dynamic variation)
                    tidal_phase = t * 0.05 + layer * 0.02 + angle
                    tidal_effect = amplitude * 0.5 * math.sin(tidal_phase)
                    r += int(tidal_effect)
                    
                    x = cx + r * math.cos(theta + layer * 0.03)
                    y = cy + r * math.sin(theta + layer * 0.03)
                    points.append((x, y))
                
                if len(points) > 2:
                    try:
                        pygame.draw.aalines(screen, current_color, False, points, 1)
                    except:
                        # Fallback to regular lines if antialiasing fails
                        pygame.draw.lines(screen, current_color, False, points, 1)
        
        # Draw center core
        self.draw_center_core(screen, colors, t, cx, cy, base_radius // 4)
    
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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Space: pause/resume
                    self.is_playing = not self.is_playing
                
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
        
        return True
    
    def previous_sample(self):
        """Switch to previous sample"""
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

                self.auto_advance_timer = 0
    
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
            
            # Control instructions
            controls = [
                "Controls:",
                "Space: Pause/Resume",
                "←/→: Switch Sample",
                "↑/↓: Switch Species",
                "R: Random Sample",
                "A: Auto Advance"
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
            
            if status_items:
                status_text = " | ".join(status_items)
                status_surface = self.font.render(status_text, True, (255, 255, 0))
                screen.blit(status_surface, (WIDTH - 290, y_offset))
    
    def run(self):
        """主运行循环"""
        running = True
        
        while running:
            # 处理事件
            running = self.handle_events()
            
            # 更新状态
            if self.is_playing:
                self.t += 1
            
            self.update_auto_advance()
            
            # 绘制
            self.screen.fill(BG_COLOR)
            
            # 绘制当前花朵
            current_sample = self.iris_data.get_sample_by_index(self.current_sample_index)
            if current_sample:
                self.visualizer.draw_data_driven_flower(self.screen, current_sample, self.t)
            
            # 绘制UI
            self.draw_ui(self.screen)
            
            # 更新显示
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    try:
        app = InteractiveFlowerApp()
        app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
