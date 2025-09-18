# 🌸 Data-Driven Ocean Flowers: Interactive Iris Dataset Visualization

An artistic and interactive visualization system that transforms the classic Iris dataset into beautiful, dynamic ocean-inspired flowers using Python and Pygame.

## ✨ Features

### Data-Driven Visualization
- **Real Data Integration**: Each flower is generated based on actual Iris dataset measurements
- **Visual Mapping Strategy**:
  - **Sepal Length** → Base flower radius (longer sepals create larger flowers)
  - **Sepal Width** → Number of petals (wider sepals create more petals)
  - **Petal Length** → Dynamic amplitude (longer petals create more dynamic shape variations)
  - **Petal Width** → Layer complexity (wider petals create more intricate layers)

### Species-Specific Aesthetics
- **Iris-setosa**: Ocean blue color scheme with elegant simplicity
- **Iris-versicolor**: Teal color scheme with moderate complexity
- **Iris-virginica**: Purple-magenta color scheme with maximum complexity

### Interactive Controls
- **Space**: Pause/Resume animation
- **←/→**: Navigate between different iris samples
- **↑/↓**: Switch between species filters
- **R**: Jump to random sample
- **A**: Toggle auto-advance mode
- **C**: Toggle between Auto color mode and Manual color selection
- **1/2**: Switch between color themes (when in Manual mode)
- **V**: Start/Stop video recording (5 seconds)

### Real-time Information Display
- Current sample ID and species
- Detailed feature measurements (sepal/petal dimensions)
- Interactive species filtering
- Control instructions
- Animation status indicators

## 🎨 Visual Effects

Each flower represents a unique iris sample with:
- **Dynamic ocean-wave motion** that reflects natural tidal patterns
- **Multi-layered petal structures** with gradient color transitions
- **Species-specific color schemes** inspired by ocean environments
- **Real-time animations** that bring static data to life
- **Responsive design** that adapts to actual measurement values

## 🚀 Getting Started

### Prerequisites
```bash
pip install pygame opencv-python numpy
```

### Running the Application
```bash
python src/main.py
```

### Data Requirements
The application expects an `Iris data.csv` file in the project root with the standard Iris dataset format:
- Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species

## 🎮 How to Use

1. **Launch** the application to see the first iris sample as a dynamic flower
2. **Explore samples** using arrow keys to see how different measurements create unique flower appearances
3. **Filter by species** to compare characteristics within each iris type
4. **Use auto-advance** to create a continuous slideshow of all samples
5. **Pause anytime** to examine specific flowers in detail

## 📊 Data Insights Through Art

This visualization makes data patterns visible through artistic representation:
- **Size variations** become immediately apparent through flower radius
- **Species clustering** is revealed through consistent color schemes
- **Feature relationships** are expressed through correlated visual elements
- **Outliers** stand out as unusually shaped or sized flowers

## 🛠 Technical Architecture

### Core Classes
- **`IrisData`**: Handles CSV loading, normalization, and data management
- **`FlowerVisualizer`**: Manages the mathematical flower generation and rendering
- **`InteractiveFlowerApp`**: Controls the main application loop and user interaction

### Rendering Pipeline
1. Load and normalize iris dataset
2. Map normalized features to visual parameters
3. Generate dynamic flower geometry using trigonometric functions
4. Apply species-specific color schemes with time-based transitions
5. Render multi-layered petals with ocean-wave effects

## 🌊 Mathematical Foundation

The flower generation combines:
- **Polar coordinate systems** for natural petal arrangements
- **Harmonic functions** for smooth, wave-like motion
- **Multi-frequency synthesis** for complex, organic shapes
- **Color interpolation** for seamless gradient transitions

## 📈 Educational Value

This project demonstrates:
- **Data visualization principles** through artistic interpretation
- **Mathematical modeling** of natural forms
- **Interactive design** for exploratory data analysis
- **Real-time graphics programming** with Python and Pygame

## 🎯 Future Enhancements

- ~~Export functionality for high-resolution flower images~~ ✅ **COMPLETED: Video Export**
- Comparative view showing multiple species simultaneously
- Statistical overlays showing distribution patterns
- 3D flower rendering for enhanced visual impact
- Sound generation based on data patterns

## 🎬 Video Export Feature

The application now includes a powerful video recording feature:

- **Press V** to start recording a 5-second video of the current flower animation
- **Recording Progress** is displayed in the status bar with a red indicator
- **Auto-stop** after 5 seconds (300 frames at 60 FPS, exported at 30 FPS)
- **Smart Naming**: Videos are automatically named with species, sample ID, and timestamp
- **Output Format**: MP4 videos saved in the `videos/` directory
- **Example filename**: `iris_flower_setosa_sample1_20250918_171234.mp4`

Perfect for:
- Creating presentations about data visualization
- Sharing specific flower animations on social media
- Building a library of all 150 unique iris flower animations
- Demonstrating the relationship between data and visual output

---

Transform your understanding of data through the beauty of generative art. Each iris sample tells its unique story through the language of dynamic, ocean-inspired flowers.