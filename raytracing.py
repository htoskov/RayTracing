# Python RayTracing App
import pygame
import math
from pygame.locals import *

# -------------- Definitions ---------------
background_color = (0, 0, 0)
WIDTH, HEIGHT = 1300, 700
circle_color = (255, 255, 0)
circle_radius = 50
circle_pos = (300, 300)
obstacleCircle_color = (5, 0 , 55)
obstacleCircle_pos = (800, 500)
obstacleCircle_radius = 80
ray_length = 1500
ray_color = (255, 255, 0)

# -------------- GUI initialization --------------
DISPLAY = pygame.display.set_mode(size=(WIDTH, HEIGHT), flags=0, depth=0, display=0, vsync=1)
DISPLAY.fill(background_color)
pygame.display.set_caption("Ray Tracing with Python")

# -------------- Rays intersection(Used ChatGPT for assistance due to mathematical complexity --------------
def circle_line_intersection(circle_center, circle_radius, line_start, line_end):
    cx, cy = circle_center
    x1, y1 = line_start
    x2, y2 = line_end

    dx, dy = x2 - x1, y2 - y1
    A = dx**2 + dy**2
    B = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    C = (x1 - cx)**2 + (y1 - cy)**2 - circle_radius**2

    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        return None

    sqrt_disc = math.sqrt(discriminant)
    t1 = (-B - sqrt_disc) / (2 * A)
    t2 = (-B + sqrt_disc) / (2 * A)

    valid_t = min(t for t in (t1, t2) if 0 <= t <= 1) if (0 <= t1 <= 1 or 0 <= t2 <= 1) else None

    if valid_t is None:
        return None

    ix = x1 + valid_t * dx
    iy = y1 + valid_t * dy
    return (ix, iy)

# --------------Rays drawing function --------------
def draw_rays():
    DISPLAY.fill(background_color)
    pygame.draw.circle(DISPLAY, obstacleCircle_color, obstacleCircle_pos, obstacleCircle_radius)
    pygame.draw.circle(DISPLAY, circle_color, circle_pos, circle_radius)

    for angle in range(0, 360, 2):
        radians = math.radians(angle)
        end_x = circle_pos[0] + ray_length * math.cos(radians)
        end_y = circle_pos[1] + ray_length * math.sin(radians)

        intersection = circle_line_intersection(obstacleCircle_pos, obstacleCircle_radius, circle_pos, (end_x, end_y))
        ray_end = intersection if intersection else (end_x, end_y)
        pygame.draw.line(DISPLAY, ray_color, circle_pos, ray_end, 2)

running = True
holding_mouse = False
while running:
    for event in pygame.event.get():
        pygame.display.update()

        for angle in range(0, 360, 2):
            radians = math.radians(angle)
            end_x = circle_pos[0] + ray_length * math.cos(radians)
            end_y = circle_pos[1] + ray_length * math.sin(radians)
            intersection = circle_line_intersection(obstacleCircle_pos, obstacleCircle_radius, circle_pos,(end_x, end_y))
            ray_end = intersection if intersection else (end_x, end_y)
            pygame.draw.line(DISPLAY, ray_color, circle_pos, ray_end, 2)

        pygame.draw.circle(DISPLAY, obstacleCircle_color, obstacleCircle_pos, obstacleCircle_radius)
        pygame.draw.circle(DISPLAY, circle_color, circle_pos, circle_radius)

        if event.type == pygame.MOUSEBUTTONDOWN:
            holding_mouse = True
        if event.type == pygame.MOUSEBUTTONUP:
            holding_mouse = False
        if holding_mouse:
            circle_pos = pygame.mouse.get_pos()
            draw_rays()
            pygame.display.update()
        if event.type == QUIT:
            running = False

pygame.quit()
