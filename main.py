import pygame
from levels.tilemap import TileMap
from entities.player import Player
from systems.camera import Camera
from systems.collision import CollisionSystem
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, WORLD_WIDTH, WORLD_HEIGHT

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a tilemap
tilemap = TileMap()

# Create a player
player = Player(150, 150)

# Get the actual world dimensions based on the tilemap
map_width = len(tilemap.room[0]) * tilemap.tile_size
map_height = len(tilemap.room) * tilemap.tile_size

# Create a camera
camera = Camera(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    map_width,
    map_height
)

# Create a collision system using tilemap obstacles
collision_system = CollisionSystem(tilemap.obstacles)

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
    tilemap.draw(screen, camera)

    # Draw the player
    player.draw(screen, camera)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
