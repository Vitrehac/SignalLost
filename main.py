import pygame
from entities.player import Player
from settings import WIDTH, HEIGHT, FPS, TITLE

pygame.init()

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a player
player = Player(WIDTH // 2, HEIGHT // 2)

# Game loop
running = True
while running:

    # Update the player
    dt = clock.tick(FPS) / 1000
    player.update(dt, screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.fill((10, 10, 15))

    # Draw the player
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit FPS
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
