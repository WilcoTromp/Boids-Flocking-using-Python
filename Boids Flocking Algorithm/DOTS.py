import random
import math
import pygame

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

class Boid:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.uniform(0, math.pi*2)

    def update(self, dots):
        self.adjust_velocity(dots)
        self.x += 1.5 * math.cos(self.angle)
        self.y += 1.5 * math.sin(self.angle)

        # Bounce off the walls
        if self.x <= 0 or self.x >= screen_width:
            self.angle = math.pi - self.angle
        if self.y <= 0 or self.y >= screen_height:
            self.angle = -self.angle

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

    def adjust_velocity(self, dots):
        # Find neighboring dots
        same_color_dots = []
        different_color_dots = []
        for dot in dots:
            distance = math.sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)
            if 0 < distance <= 25 and dot.color == self.color:
                same_color_dots.append(dot)
            elif 0 < distance <= 50 and dot.color != self.color:
                different_color_dots.append(dot)

        # Adjust velocity based on neighboring dots
        if same_color_dots:
            average_angle = sum(dot.angle for dot in same_color_dots) / len(same_color_dots)
            self.angle = average_angle
        for dot in different_color_dots:
            angle_to_dot = math.atan2(dot.y - self.y, dot.x - self.x)
            avoidance_angle = angle_to_dot - math.pi
            self.angle += (avoidance_angle - self.angle) * 0.1

class Predator:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = random.uniform(0, math.pi*2)

    def update(self, dots):
        self.x += 2.5 * math.cos(self.angle)
        self.y += 2.5 * math.sin(self.angle)

        # Bounce off the walls
        if self.x <= 0 or self.x >= screen_width:
            self.angle = math.pi - self.angle
        if self.y <= 0 or self.y >= screen_height:
            self.angle = -self.angle

        for dot in dots:
            if dot != self:
                distance = math.sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)
                if distance < 50 and dot.color == (255, 192, 203):
                    # Calculate avoidance vector
                    dx = self.x - dot.x
                    dy = self.y - dot.y
                    length = math.sqrt(dx ** 2 + dy ** 2)
                    if length > 0:
                        dx /= length
                        dy /= length
                    angle_to_dot = math.atan2(dot.y - self.y, dot.x - self.x)
                    avoidance_angle = angle_to_dot - math.pi
                    self.angle += (avoidance_angle - self.angle) * 0.1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 7.5)

class Obstacle:
    def __init__(self, x, y, color, dot_radius):
        self.x = x
        self.y = y
        self.color = color
        self.dot_radius = dot_radius
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, other_dots):
        pass

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.dot_radius))