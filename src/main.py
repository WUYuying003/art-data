


# 海浪花朵艺术生成
# new generative art python project that utilizes tidal data to produce a beautiful, ocean-inspired, dynamic visualization using pygame

import pygame
import math
import sys
import imageio
import os

WIDTH, HEIGHT = 800, 800
BG_COLOR = (0, 0, 0)  # 纯黑色背景
FPS = 60

def get_tidal_data(t, freq=0.05, amp=100, phase=0):
    return amp + 60 * math.sin(freq * t + phase)

def gradient_color(start, end, ratio):
    return tuple([int(start[i] + (end[i] - start[i]) * ratio) for i in range(3)])

def get_multi_layered_color(t, layer_ratio, distance_from_center=0):
    # 整体色系循环：深海蓝系 -> 正蓝色系 -> 马尔代夫青系 -> 海泡沫系
    # 每个色系持续时间更长，变化更明显
    base_cycle = (t / 200) % 1  # 基础色系循环
    
    # 根据距离中心的位置调整过渡时机，从中心开始渐变
    color_system_cycle = (base_cycle + distance_from_center * 0.3) % 1
    
    # 定义四个色系，颜色差异更大，更容易区分
    color_systems = [
        {  # 深海蓝系 - 深海的蓝色调
            'main': (0, 60, 120),       # 深海蓝 80%
            'secondary': (0, 40, 90),   # 更深海蓝 10%
            'accent': (30, 90, 150),    # 中海蓝 7%
            'highlight': (60, 120, 180) # 浅海蓝 3%
        },
        {  # 正蓝色系 - 纯正的蓝色调
            'main': (0, 100, 255),      # 正蓝色 80%
            'secondary': (0, 80, 200),  # 深正蓝 10%
            'accent': (50, 130, 255),   # 浅正蓝 7%
            'highlight': (100, 160, 255) # 极浅正蓝 3%
        },
        {  # 马尔代夫青系 - 明艳科技风青蓝色调（偏蓝）
            'main': (0, 220, 255),      # 明艳青蓝 80%（偏蓝）
            'secondary': (0, 180, 220), # 深青蓝 10%
            'accent': (50, 240, 255),   # 浅青蓝 7%
            'highlight': (100, 250, 255) # 极浅青蓝 3%
        },
        {  # 海泡沫系 - 明亮的海泡沫白色调
            'main': (180, 220, 255),    # 海泡沫白 80%
            'secondary': (150, 200, 240), # 深海泡沫 10%
            'accent': (200, 230, 255),  # 浅海泡沫 7%
            'highlight': (220, 240, 255) # 极浅海泡沫 3%
        }
    ]
    
    weights = {
        'main': 0.8,
        'secondary': 0.1,
        'accent': 0.07,
        'highlight': 0.03
    }
    
    # 计算当前在哪个色系
    system_segment = color_system_cycle * 4
    system_index = int(system_segment)
    system_ratio = system_segment - system_index
    
    if system_index >= 3:
        system_index = 3
        system_ratio = 1
    
    # 更平滑均匀的渐变过渡，像大海波浪一样自然
    if system_ratio < 0.8:  # 80%时间保持纯色
        system_ratio = 0
    else:  # 20%时间进行渐变过渡
        transition_progress = (system_ratio - 0.8) / 0.2
        # 使用更自然的海浪般的S曲线，多次平滑处理
        system_ratio = transition_progress * transition_progress * (3.0 - 2.0 * transition_progress)  # 第一次平滑
        system_ratio = system_ratio * system_ratio * (3.0 - 2.0 * system_ratio)  # 第二次平滑，更像海浪
    
    # 获取当前色系和下一个色系
    current_system = color_systems[system_index]
    next_system = color_systems[(system_index + 1) % 4]
    
    # 每种颜色有不同的循环周期，但变化更缓慢和自然
    cycles = {
        'main': (t / 150) % 1,     # 更慢的变化
        'secondary': (t / 120) % 1,
        'accent': (t / 180) % 1,
        'highlight': (t / 140) % 1
    }
    
    # 为每种颜色添加循环强度变化
    intensities = {}
    for color_name, cycle in cycles.items():
        # 使用更自然的正弦波创造强度循环
        base_intensity = weights[color_name]
        # 减少变化幅度，使用更自然的曲线
        cycle_intensity = 0.05 * math.sin(2 * math.pi * cycle + layer_ratio * math.pi)
        intensities[color_name] = max(0.01, base_intensity + cycle_intensity)  # 确保最小值
    
    # 归一化强度
    total_intensity = sum(intensities.values())
    if total_intensity > 0:
        for color_name in intensities:
            intensities[color_name] /= total_intensity
    
    # 在当前色系和下一个色系之间插值
    final_color = [0, 0, 0]
    for color_name, intensity in intensities.items():
        current_color = current_system[color_name]
        next_color = next_system[color_name]
        
        # 在两个色系之间插值
        interpolated_color = gradient_color(current_color, next_color, system_ratio)
        
        for i in range(3):
            final_color[i] += interpolated_color[i] * intensity
    
    return tuple([int(c) for c in final_color])

def draw_flower(screen, t):
    cx, cy = WIDTH // 2, HEIGHT // 2
    num_petals = 24
    num_layers = 12
    scale = 0.6
    base_radius = int(80 * scale)
    
    # 增强动态变化，但保持花朵形状
    for layer in range(num_layers):
        layer_ratio = layer / (num_layers - 1)
        
        # 增大动态变化幅度，速度加快2倍
        dynamic_radius = base_radius + int(layer * 22 * scale)
        dynamic_radius += int(25 * math.sin(t * 0.12 + layer) * scale)  # 从0.06改为0.12
        dynamic_radius += int(15 * math.cos(t * 0.08 + layer * 0.5) * scale)  # 从0.04改为0.08
        
        # 获取多层混合颜色，考虑距离中心的位置
        base_color = get_multi_layered_color(t, layer_ratio, layer_ratio)
        
        for petal in range(num_petals):
            angle = 2 * math.pi * petal / num_petals + t * 0.03 + layer * 0.13  # 从0.015改为0.03
            
            # 花朵内部渐变：不同层使用不同的颜色混合，考虑距离中心的位置
            petal_color = get_multi_layered_color(t + petal * 10, layer_ratio + petal * 0.1, layer_ratio)
            
            points = []
            for i in range(180):
                theta = angle + math.pi * i / 180
                
                # 增强形状变化，但保持花朵特征，速度加快2倍
                r = dynamic_radius
                r += int(50 * math.sin(6 * theta + t * 0.10 + layer) * scale)  # 从0.05改为0.10
                r -= int(25 * math.cos(3 * theta + t * 0.06 + layer) * scale)  # 从0.03改为0.06
                r += int(20 * math.sin(9 * theta + t * 0.04) * scale)  # 从0.02改为0.04
                
                # 潮汐数据影响，增大变化幅度
                tidal_effect = get_tidal_data(t + i + layer * 12, freq=0.12 + layer*0.01, amp=25 + layer*15, phase=angle)
                r += int(tidal_effect * scale * 0.8)
                
                x = cx + r * math.cos(theta + layer * 0.04)
                y = cy + r * math.sin(theta + layer * 0.04)
                points.append((x, y))
                
            if len(points) > 2:
                pygame.draw.aalines(screen, petal_color, False, points)
    
    # 绘制中心渐变圆，循环变化，速度像大海一样自然
    center_base_cycle = (t * 3 / 200) % 1  # 适中的变化速度，像海浪节奏
    center_color = get_multi_layered_color(t * 3, 0, 0)  # 中心颜色速度快3倍，自然过渡
    for i in range(24):
        ratio = i / 23
        inner_color = center_color
        outer_color = get_multi_layered_color(t * 3, 0.3, ratio)  # 外圈颜色也快3倍
        color = gradient_color(inner_color, outer_color, ratio)
        pygame.draw.circle(screen, color, (cx, cy), int((32 - i) * scale), 0)

def draw_extra_shapes(screen, t):
    # 移除外围圆环和小点，保持简洁的花朵形状
    pass


def save_gif(filename="flower.gif", frames=60):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    images = []
    for t in range(frames):
        screen.fill(BG_COLOR)
        draw_flower(screen, t)
        draw_extra_shapes(screen, t)
        pygame.display.flip()
        # 保存帧为图片
        data = pygame.surfarray.array3d(screen)
        # 转换为imageio需要的格式
        img = data.transpose([1, 0, 2])
        images.append(img)
    pygame.quit()
    # 保存为GIF
    imageio.mimsave(filename, images, duration=0.08)
    print(f"GIF已保存为 {filename}")

def main():
    # 运行可视化
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
    # 生成GIF
    save_gif("ocean_flower.gif", frames=120)
    # 运行主程序（如需实时预览，取消下行注释）
    # main()
