import pygame
import sys
import random
import DOTS

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

points = [(200, 400), (400, 200), (600, 400)]

# List to hold all dots
dots = []

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Create a new blue dot at mouse position
                new_boid = DOTS.Boid(mouse_x, mouse_y, BLUE)
                dots.append(new_boid)
            elif event.button == 3:  # Right mouse button
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Create a new green dot at mouse position
                new_boid = DOTS.Boid(mouse_x, mouse_y, GREEN)
                dots.append(new_boid)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Create a stationary red dot
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Create a new stationary red dot at mouse position
                dot_radius = random.uniform(10,50)
                new_obstacle = DOTS.Obstacle(mouse_x, mouse_y, PINK, dot_radius)
                dots.append(new_obstacle)
            elif event.key == pygame.K_b:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_small_obstacle = DOTS.Obstacle(mouse_x, mouse_y, PINK, 5)
                dots.append(new_small_obstacle)
            elif event.key == pygame.K_p:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_predator = DOTS.Predator(mouse_x, mouse_y, RED)
                dots.append(new_predator)


    # Update dots
    for dot in dots:
        dot.update(dots)

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
