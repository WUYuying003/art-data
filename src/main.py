

# 花朵艺术生成
# new generative art python project that utilizes tidal data to produce a beautiful, colorful, flower-like dynamic visualization using pygame
import pygame
import math
import random
import sys

WIDTH, HEIGHT = 800, 800
BG_COLOR = (20, 10, 40)
FPS = 60

# 彩色花瓣配色
PETAL_COLORS = [
    (255, 80, 80),    # 红
    (255, 200, 0),    # 黄
    (80, 255, 80),    # 绿
    (80, 180, 255),   # 蓝
    (180, 80, 255),   # 紫
    (255, 80, 200),   # 粉
    (255, 255, 255),  # 白
]

# 模拟潮汐数据
def get_tidal_data(t, freq=0.05, amp=100, phase=0):
    return amp + 60 * math.sin(freq * t + phase)

def draw_flower(screen, t):
    cx, cy = WIDTH // 2, HEIGHT // 2
    num_petals = 8
    num_layers = 5
    for layer in range(num_layers):
        layer_radius = 80 + layer * 40 + 20 * math.sin(t * 0.02 + layer)
        for petal in range(num_petals):
            angle = 2 * math.pi * petal / num_petals + t * 0.01 + layer * 0.2
            color = PETAL_COLORS[(petal + layer + int(t/30)) % len(PETAL_COLORS)]
            points = []
            for i in range(60):
                theta = angle + math.pi * i / 60
                r = layer_radius + 30 * math.sin(3 * theta + t * 0.03 + layer)
                r += get_tidal_data(t + i + layer * 20, freq=0.07 + layer*0.01, amp=30 + layer*20, phase=angle)
                x = cx + r * math.cos(theta)
                y = cy + r * math.sin(theta)
                points.append((x, y))
            if len(points) > 2:
                pygame.draw.aalines(screen, color, False, points)
    # 绘制中心
    pygame.draw.circle(screen, (255, 255, 180), (cx, cy), 40 + 10 * math.sin(t * 0.05), 0)

def draw_extra_shapes(screen, t):
    cx, cy = WIDTH // 2, HEIGHT // 2
    # 绘制动态圆环
    for i in range(3):
        radius = 200 + 30 * math.sin(t * 0.03 + i)
        color = PETAL_COLORS[(i + int(t/20)) % len(PETAL_COLORS)]
        pygame.draw.circle(screen, color, (cx, cy), int(radius), 2)
    # 绘制动态小点
    for i in range(30):
        angle = 2 * math.pi * i / 30 + t * 0.02
        r = 300 + 40 * math.sin(t * 0.01 + i)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        color = PETAL_COLORS[i % len(PETAL_COLORS)]
        pygame.draw.circle(screen, color, (int(x), int(y)), 6)

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
        draw_flower(screen, t)
        draw_extra_shapes(screen, t)
        pygame.display.flip()
        t += 1
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
