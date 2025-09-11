import pygame
import math
import requests
import sys

WIDTH, HEIGHT = 800, 800
BG_COLOR = (10, 10, 30)
SPIRAL_COLOR = (0, 200, 255)
FPS = 60

# Placeholder: Simulate tidal data as a sine wave
# Replace with real API call if available
def get_tidal_data(t):
    # Example: amplitude varies with time
    return 100 + 50 * math.sin(t * 0.05)

def draw_spiral(screen, t):
    cx, cy = WIDTH // 2, HEIGHT // 2
    points = []
    for i in range(360):
        angle = math.radians(i * 2)
        radius = get_tidal_data(t + i)
        x = cx + radius * math.cos(angle + t * 0.01)
        y = cy + radius * math.sin(angle + t * 0.01)
        points.append((x, y))
    if len(points) > 1:
        pygame.draw.aalines(screen, SPIRAL_COLOR, False, points)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG_COLOR)
        draw_spiral(screen, t)
        pygame.display.flip()
        t += 1
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
