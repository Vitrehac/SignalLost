import pygame
from entities.player import Player
from systems.camera import Camera
from systems.collision import CollisionSystem

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, WORLD_WIDTH, WORLD_HEIGHT

pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Create a camera
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)

# Create obstacles for collision detection
obstacles = [
    pygame.Rect(400, 200, 300, 40),
    pygame.Rect(400, 240, 40, 200),
    pygame.Rect(700, 400, 300, 40)
]

collision_system = CollisionSystem(obstacles)


def draw_world(screen, camera):
    tile_size = 64

    # Draw the world grid
    for x in range(0, WORLD_WIDTH, tile_size):

        for y in range(0, WORLD_HEIGHT, tile_size):
            
            # Create a temporary entity to represent the tile's position in the world
            world_rect = pygame.Rect(x, y, tile_size, tile_size)
            screen_rect = camera.apply(
                type("Entity", (), {"rect": world_rect})
            )

            pygame.draw.rect(screen, (25, 25, 32), screen_rect)
            pygame.draw.rect(screen, (35, 35, 42), screen_rect, 1)

# Game loop
running = True
while running:

    # Update the player
    dt = clock.tick(FPS) / 1000
    player.update(dt, collision_system)

    # Update the camera
    camera.update(player)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.fill((10, 10, 15))

    # Draw the world
    draw_world(screen, camera)

    # Draw the player
    player.draw(screen, camera)

    # Draw obstacles
    for obstacle in obstacles:
        screen_rect = obstacle.move(-camera.offset.x, -camera.offset.y)
        pygame.draw.rect(screen, (100, 100, 110), screen_rect)

    # Update the display
    pygame.display.flip()

    # Limit FPS
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
