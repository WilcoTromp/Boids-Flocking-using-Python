import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Dots")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)

# Define Dot class
class Dot:
    def __init__(self, x, y, color, dot_radius, stationary=False):
        self.x = x
        self.y = y
        self.color = color
        self.stationary = stationary
        self.dot_radius = dot_radius
        self.velocity_x = 0 if self.stationary else random.uniform(-1.5, 1.5)  # Random initial velocity in x-direction
        self.velocity_y = 0 if self.stationary else random.uniform(-1.5, 1.5)  # Random initial velocity in y-direction

    def update(self):
        if not self.stationary:
            self.x += self.velocity_x
            self.y += self.velocity_y

            # Bounce off the walls
            if self.x <= 0 or self.x >= screen_width:
                self.velocity_x *= -1
            if self.y <= 0 or self.y >= screen_height:
                self.velocity_y *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.dot_radius))


# List to hold all dots
dots = []

# Main loop
running = True
while running:
    dot_radius = 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Create a new blue dot at mouse position
                new_dot = Dot(mouse_x, mouse_y, BLUE, dot_radius)
                dots.append(new_dot)
            elif event.button == 3:  # Right mouse button
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Create a new green dot at mouse position
                new_dot = Dot(mouse_x, mouse_y, GREEN, dot_radius)
                dots.append(new_dot)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Create a stationary red dot
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Create a new stationary red dot at mouse position
                dot_radius = random.uniform(10,50)
                new_dot = Dot(mouse_x, mouse_y, RED, dot_radius, stationary=True)
                dots.append(new_dot)
            elif event.key == pygame.K_b:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_dot = Dot(mouse_x, mouse_y, RED, dot_radius, stationary=True)
                dots.append(new_dot)
            elif event.key == pygame.K_p:
                dot_radius = 7.5
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_dot = Dot(mouse_x, mouse_y, PINK, dot_radius)
                dots.append(new_dot)

    # Update dots
    for dot in dots:
        dot.update()

    # Draw everything
    screen.fill(BLACK)
    for dot in dots:
        dot.draw()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()
