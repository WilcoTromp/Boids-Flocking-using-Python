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
        self.velocity_x = random.uniform(-1, 1)
        self.velocity_y = random.uniform(-1, 1)

    def update(self, dots):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off the walls
        if self.x <= 0 or self.x >= screen_width:
            self.velocity_x *= -1
        if self.y <= 0 or self.y >= screen_height:
            self.velocity_y *= -1

        for dot in dots:
            if dot != self:
                distance = math.sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)
                if distance < 50 and dot.color != self.color:
                    # Calculate avoidance vector
                    dx = self.x - dot.x
                    dy = self.y - dot.y
                    length = math.sqrt(dx ** 2 + dy ** 2)
                    if length > 0:
                        dx /= length
                        dy /= length
                    # Adjust velocity based on avoidance vector
                    self.velocity_x += dx * 0.1
                    self.velocity_y += dy * 0.1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

class Predator:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = random.uniform(-1.5, 1.5)
        self.velocity_y = random.uniform(-1.5, 1.5)

    def update(self, dots):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off the walls
        if self.x <= 0 or self.x >= screen_width:
            self.velocity_x *= -1
        if self.y <= 0 or self.y >= screen_height:
            self.velocity_y *= -1

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
                    # Adjust velocity based on avoidance vector
                    self.velocity_x += dx * 0.1
                    self.velocity_y += dy * 0.1

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