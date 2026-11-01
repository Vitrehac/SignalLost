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

# Initialize font
interaction_font = pygame.font.Font(None, 28)

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


def draw_interaction_prompt(screen, camera, door_rect, message):
    # Draw the interaction prompt above the door if the player is close enough
    text = interaction_font.render(message, True, (255, 255, 255))

    # Calculate the position of the prompt based on the door's position and the camera's offset
    x = door_rect.centerx - camera.offset.x
    y = door_rect.top - camera.offset.y - 40

    # Create a popup rectangle for the text with some padding
    popup_rect = pygame.Rect(0, 0, text.get_width() + 24, 34)
    popup_rect.center = (round(x), round(y))

    # Draw the popup rectangle and the text
    pygame.draw.rect(screen, (35, 40, 50), popup_rect, border_radius=6)
    screen.blit(text, text.get_rect(center=popup_rect.center))

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

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                tilemap.interact(player)

    # Draw background
    screen.fill((10, 10, 15))

    # Draw the world
    tilemap.draw(screen, camera)

    # Draw the player
    player.draw(screen, camera)

    # Check for nearby terminals & doors and draw interaction prompt if the player is close enough
    interaction = tilemap.get_nearby_interaction(player)

    if interaction is not None:
        draw_interaction_prompt(screen, camera, interaction["rect"], interaction["message"])
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
