import pygame
from levels.tilemap import TileMap
from entities.player import Player
from puzzles.keypad_puzzle import KeypadPuzzle
from puzzles.power_puzzle import PowerPuzzle
from systems.camera import Camera
from systems.collision import CollisionSystem
from systems.game_state import GameState
from systems.objectives import ObjectiveSystem
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, WORLD_WIDTH, WORLD_HEIGHT
from ui.log_viewer import LogViewer


# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# Initialize font
interaction_font = pygame.font.Font(None, 28)

# Initialize the objective font
objective_font = pygame.font.Font(None, 30)

# Initialize the log viewer
log_viewer = LogViewer([])

# Initialize the game state
game_state = GameState()

# Clock to control the frame rate
clock = pygame.time.Clock()

# Create a tilemap no 1
tilemap = TileMap("level1.txt")

# Create a keypad puzzle
keypad_puzzle = KeypadPuzzle()

# Create a security door
security_door_unlocked = False

# Create an objective system
objectives = ObjectiveSystem()

# Create a player
player = Player(150, 150)

# Create a power puzzle
power_puzzle = PowerPuzzle()

# Create a checkpoint
checkpoint = (150, 150)

security_alert_start = None
security_alert_duration = 1500
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

# Track the current level to determine which tilemap to use
current_level = 1

def load_level(level_number):

    # Load the specified level and update the global variables for tilemap, collision system, and camera
    global tilemap, collision_system, camera

    tilemap = TileMap(f"level{level_number}.txt")

    map_width = len(tilemap.room[0]) * tilemap.tile_size
    map_height = len(tilemap.room) * tilemap.tile_size

    camera = Camera(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        map_width,
        map_height
    )

    collision_system = CollisionSystem(tilemap.obstacles)

    # Reset the player's position to the starting point for the new level
    player.x = 150
    player.y = 150
    player.rect.topleft = (150, 150)


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
    if not power_puzzle.active and not log_viewer.active and not keypad_puzzle.active:
        player.update(dt, collision_system)

    # Security laser interaction
    if current_level == 3 and not game_state.security_disabled:
        hazard = tilemap.get_touching_hazard(player)
        if hazard is not None:
            security_alert_start = pygame.time.get_ticks()
            player.x, player.y = checkpoint
            player.rect.topleft = checkpoint


    # Update the camera
    camera.update(player)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle interaction key press when the power puzzle is not active
        elif event.type == pygame.KEYDOWN:
            
            # Keypad puzzle
            if keypad_puzzle.active:

                if event.key == pygame.K_ESCAPE:
                    if not keypad_puzzle.solved:
                        keypad_puzzle.close()
                
                else:
                    keypad_puzzle.handle_key(event.key)

            # Log viewer
            elif log_viewer.active:
                
                if event.key == pygame.K_ESCAPE:
                    log_viewer.close()

            # Power puzzle
            elif power_puzzle.active:
                if event.key == pygame.K_ESCAPE and not power_puzzle.solved:
                    power_puzzle.close()
            
            # Normal gameplay interactions
            elif event.key == pygame.K_e:
                switch = None

                if current_level == 3:
                    switch = tilemap.get_nearby_shutdown_switch(player)

                if switch is not None:
                    if not game_state.security_disabled:
                        game_state.security_disabled = True
                        tilemap.disable_lasers()
                        print("SECURITY SYSTEM DISABLED")

                else:
                    interaction = tilemap.get_nearby_interaction(player)

                    if interaction is not None:
                        if interaction["type"] == "terminal":
                            power_puzzle.open()
                        
                        elif interaction["type"] == "computer":
                            log_viewer.open(
                                "L0G NO1: Emergency shutdown. "
                                "At 4:36 a.m., the facility experienced a complete system failure. "
                                "A11 communication with the lower research levels has been lost. "
                                "The emergency broadcast was activat3d without authorization. "
                                "There are rumors that the archive has been corrupted. "
                                "Make sure to check character integrity. "
                            )
                            game_state.computer_read = True

                        elif interaction["type"] == "keypad":
                            keypad_puzzle.open()  

                        else:
                            tilemap.interact(player)

        # Handle mouse click events when the power puzzle is active
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

    # Draw the keypad puzzle
    keypad_puzzle.draw(screen)

    # Draw the interaction prompt if the player is near a terminal or door
    if (
        interaction is not None
        and not power_puzzle.active
        and not log_viewer.active
        and not keypad_puzzle.active
    ):
        draw_interaction_prompt(screen, camera, interaction["rect"], interaction["message"])

    # Render the current objective text on the screen
    objective_text = objective_font.render(
        "OBJECTIVE: " + objectives.get_current_objective(game_state),
        True, 
        (220, 220, 220)
    )

    # Draw the objective text on the screen at a fixed position
    screen.blit(objective_text, (20, 20))

    # Draw the log viewer if it's active
    log_viewer.draw(screen)

    # Check if the power puzzle is solved and the power is not yet on, then activate the terminal
    if (
        current_level == 1
        and power_puzzle.solved
        and not power_puzzle.active
        and not tilemap.power_on
    ):
        if tilemap.activate_terminal(player):
            game_state.power_restored = True

    # Update the power puzzle state
    power_puzzle.update()

    # Update the keypad puzzle state
    keypad_puzzle.update()
    
    # Transition logic
    exit_rect = tilemap.get_exit_rect()
    if exit_rect is not None and player.rect.colliderect(exit_rect):
        current_level += 1
        load_level(current_level)

        if current_level == 2:
            game_state.control_room_entered = True
        
        elif current_level == 3:
            game_state.containment_entered = True

        print(f"Loaded Level {current_level}")

    # Proccess security doors
    if (
        current_level == 2
        and keypad_puzzle.solved
        and not security_door_unlocked
    ):
        if tilemap.unlock_security_door():
            security_door_unlocked = True
            game_state.security_unlocked = True
            print("Security door unlocked!")

    if current_level == 3:
        switch = tilemap.get_nearby_shutdown_switch(player)

        if switch is not None:
            print("Player is standing on the shutdown switch")

        final_terminal = tilemap.get_nearby_final_terminal(player)
        if final_terminal is not None:
            print("FINAL TERMINAL DETECTED")

    if security_alert_start is not None:
        elapsed = pygame.time.get_ticks() - security_alert_start

        if elapsed < security_alert_duration:
            alert_font = pygame.font.Font(None, 48)

            alert_text = alert_font.render(
                "SECURITY BREACH - RETURNED TO CHECKPOINT",
                True,
                (255, 70, 70)
            )

            alert_rect = alert_text.get_rect(
                center=(SCREEN_WIDTH // 2, 100)
            )

            screen.blit(alert_text, alert_rect)
        
        else:
            security_alert_start = None
   
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
