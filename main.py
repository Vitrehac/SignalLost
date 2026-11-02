import pygame
from levels.tilemap import TileMap
from entities.player import Player
from puzzles.power_puzzle import PowerPuzzle
from systems.camera import Camera
from systems.collision import CollisionSystem
from systems.objectives import ObjectiveSystem
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, WORLD_WIDTH, WORLD_HEIGHT

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# Initialize font
interaction_font = pygame.font.Font(None, 28)

# Initialize the objective font
objective_font = pygame.font.Font(None, 30)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a tilemap
tilemap = TileMap()

# Create an objective system
objectives = ObjectiveSystem()

# Create a player
player = Player(150, 150)

# Create a power puzzle
power_puzzle = PowerPuzzle()

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

# Define the control room trigger area
control_room_trigger = pygame.Rect(13 * 64, 8 * 64, 8 * 64, 2 * 64)



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
    if not power_puzzle.active:
        player.update(dt, collision_system)

    # Update the camera
    camera.update(player)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle interaction key press when the power puzzle is not active
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and not power_puzzle.active:
                interaction = tilemap.get_nearby_interaction(player)

                if interaction is not None:
                    if interaction["type"] == "terminal":
                        power_puzzle.open()
                        print("Puzzle active: ", power_puzzle.active)
                        print("Puzzle solved: ", power_puzzle.solved)
                        print("Facility power: ", tilemap.power_on)
                        print("Current objective: ", objectives.current_index)

                    else:
                        tilemap.interact(player)

            if event.key == pygame.K_ESCAPE and power_puzzle.active:
                power_puzzle.close()
                print("Puzzle closed: ", power_puzzle.active)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and power_puzzle.active:
                power_puzzle.handle_click(event.pos, screen)

    # Draw background
    screen.fill((10, 10, 15))

    # Draw the world
    tilemap.draw(screen, camera)

    # Draw the player
    player.draw(screen, camera)

    # Check for nearby terminals & doors and draw interaction prompt if the player is close enough
    interaction = tilemap.get_nearby_interaction(player)
    
    # Draw the power puzzle if it's active
    power_puzzle.draw(screen)

    # Draw the interaction prompt if the player is near a terminal or door
    if interaction is not None:
        draw_interaction_prompt(screen, camera, interaction["rect"], interaction["message"])
    
    # Update objectives based on game state
    if tilemap.power_on and objectives.current_index == 0:
        objectives.advance()
    
    # Render the current objective text on the screen
    objective_text = objective_font.render(
        "OBJECTIVE: " + objectives.get_current_objective(),
        True, 
        (220, 220, 220)
    )

    # Advance to the next objective if the player enters the control room after restoring power
    if objectives.current_index == 1:
        if player.rect.colliderect(control_room_trigger):
            objectives.advance()
    screen.blit(objective_text, (20, 20))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
