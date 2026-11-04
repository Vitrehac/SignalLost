from pathlib import Path
import pygame

class TileMap:
    def __init__(self, level_file="level1.txt"):
        self.tile_size = 64

        # Load the room layout from a text file
        map_path = Path(__file__).parent / "maps" / level_file
        with open(map_path, "r") as f:
            self.room = [line.strip() for line in f.readlines()]


        self.obstacles = []

        # Create obstacles based on the room layout
        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):

                # If the tile is a wall, create a rectangle for it and add it to the obstacles list
                if tile in ("#", "D", "L", "T", "C", "K", "S"):
                    x = column_index * self.tile_size
                    y = row_index * self.tile_size
                    self.obstacles.append(pygame.Rect(x, y, self.tile_size, self.tile_size))

        # Initialize the power state of the terminal
        self.power_on = False


    def draw(self, screen, camera):

        # Draw the room's floor and walls based on the room layout
        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):

                # Calculate the position of the tile in the world
                x = column_index * self.tile_size
                y = row_index * self.tile_size

                # Create a temporary entity to represent the tile's position in the world
                world_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                
                # Adjust the tile's position based on the camera's offset to get its position on the screen
                screen_rect = world_rect.move(
                    -camera.offset.x,
                    -camera.offset.y
                )

                # Draw the tile as a dark rectangle with a border
                if tile == "#":
                    color = (100, 100, 110)
                
                # Draw the door tile with a different color
                elif tile == "D":
                    color = (180, 100, 40)

                # Draw the locked door tile with a different color
                elif tile == "L":
                    color = (160, 40, 40)
                
                # Terminal colour
                elif tile == "T":
                    color = (40, 130, 180)

                # Computer colour
                elif tile == "C":
                    color = (120, 80, 180)

                # Keypad colour
                elif tile == "K":
                    color = (180, 180, 40)
                # Security door colour
                elif tile == "S":
                    color = (180, 50, 100)

                # Exit colour
                elif tile == "X":
                    color = (50, 200, 100)

                else:
                    color = (25, 25, 32)

                pygame.draw.rect(screen, color, screen_rect)

    def open_door(self, player):

        # Get the nearby door rectangle based on the player's position
        door_rect = self.get_nearby_door(player)

        if door_rect is None:
            return
        
        # Update the room layout to replace the door tile with a floor tile
        row_index = door_rect.y // self.tile_size
        column_index = door_rect.x // self.tile_size

        row = self.room[row_index]
        door_type = row[column_index]

        if door_type == "L" and not self.power_on:
            print("Door locked. Restore power first.")
            return

        self.room[row_index] = (row[:column_index] + "." + row[column_index + 1:])

        self.obstacles.remove(door_rect)


    def get_nearby_door(self, player):
        interaction_range = 80

        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):
                if tile not in ("D", "L"):
                    continue
                
                door_rect = pygame.Rect(
                    column_index * self.tile_size,
                    row_index * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )

                distance = pygame.Vector2(player.rect.center).distance_to(door_rect.center)

                if distance <= interaction_range:
                    return door_rect

        return None

    
    def get_nearby_terminal(self, player):
        interaction_range = 80

        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):
                if tile != "T":
                    continue

                terminal_rect = pygame.Rect(
                    column_index * self.tile_size,
                    row_index * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                    
                distance = pygame.Vector2(player.rect.center).distance_to(terminal_rect.center)

                if distance <= interaction_range:
                    return terminal_rect
        
        return None

    def activate_terminal(self, player):
        terminal = self.get_nearby_terminal(player)

        if terminal is None:
            return False

        self.power_on = True
        print("Power restored!")
        for row_index, row in enumerate(self.room):
            self.room[row_index] = row.replace("L", "D")
        return True

    def get_nearby_interaction(self, player):

        # Check for nearby terminal first, then check for nearby door
        terminal = self.get_nearby_terminal(player)

        # If the player is near a terminal and the power is off, return the interaction prompt for the terminal
        if terminal is not None and not self.power_on:
            return {
                "type": "terminal",
                "rect": terminal,
                "message": "E Restore power"
            }

        # If the player is near a door, return the interaction prompt for the door
        door = self.get_nearby_door(player)

        # If the player is near a door, determine the type of door and return the appropriate interaction prompt
        if door is not None:
            row = door.y // self.tile_size
            col = door.x // self.tile_size
            door_type = self.room[row][col]
        
            # If the door is locked and the power is off, return a message indicating that the door is locked
            if door_type == "L" and not self.power_on:
                message = "Door locked. Restore power first."
            else:
                message = "E Open door"

            # Return the interaction prompt for the door with the appropriate message
            return {
                "type": "door",
                "rect": door,
                "message": message
            }
        
        computer = self.get_nearby_computer(player)
        if computer is not None:
            return {
                "type": "computer", 
                "rect": computer, 
                "message": "E Read logs"
            }

        keypad = self.get_nearby_keypad(player)
        if keypad is not None:
            return {
                "type": "keypad",
                "rect": keypad,
                "message": "E Enter security code"
            }

        return None

    def interact(self, player):
        interaction = self.get_nearby_interaction(player)
        print("detected interaction:", interaction)

        if interaction is None:
            return
        
        elif interaction["type"] == "terminal":
            self.activate_terminal(player)

        elif interaction["type"] == "door":
            self.open_door(player)

        elif interaction["type"] == "computer":
            print("Interacting with computer")

    
    def get_nearby_computer(self, player):
        interaction_range = 80

        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):
                if tile != "C":
                    continue
                
                computer_rect = pygame.Rect(
                    column_index * self.tile_size,
                    row_index * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )

                distance = pygame.Vector2(player.rect.center).distance_to(computer_rect.center)

                if distance <= interaction_range:
                    return computer_rect
        return None

    
    def get_nearby_keypad(self, player):
        interaction_range = 80

        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):
                if tile != "K":
                    continue

                keypad_rect = pygame.Rect(
                    column_index * self.tile_size,
                    row_index * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                distance = pygame.Vector2(player.rect.center).distance_to(keypad_rect.center)

                if distance<= interaction_range:
                    return keypad_rect
        return None


    def unlock_security_door(self):
        for row_index, row in enumerate(self.room):
            if "S" not in row:
                continue
            column_index = row.index("S")

            door_rect = pygame.Rect(
            column_index * self.tile_size,
            row_index * self.tile_size,
            self.tile_size,
            self.tile_size
            )

            self.room[row_index] = (row[:column_index] + "." + row[column_index + 1:])
            self.obstacles.remove(door_rect)

            return True
        return False

    
    def get_exit_rect(self):
        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):
                if tile == "X":
                    return pygame.Rect(
                        column index * self.tile_size,
                        row_index * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
