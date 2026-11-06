from pathlib import Path
import pygame


class PowerPuzzle:
    def __init__(self):

        # Initialise the puzzle state
        self.active = False
        self.solved = False

        # Define the duration for which the success message is displayed after solving the puzzle
        self.success_duration = 1000
        self.success_start = None
        # Define the grid size and tile size for the puzzle
        self.grid_size = 3
        self.tile_size = 80
        self.grid = [
            [2, 0, 1],
            [0, 3, 0],
            [1, 2, 1]
        ]

        # Define the tile types for the puzzle, which determine the circuit connections
        self.tile_types = [
            ["corner", "straight", "corner"],
            ["corner", "corner", "corner"],
            ["straight", "corner", "straight"]
        ]


    def open(self):
        if not self.solved:
            self.active = True


    def close(self):
        self.active = False


    def draw(self, screen):
        if not self.active:
            return

        width, height = screen.get_size()

        # Darken the game background
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0,))

        # Draw terminal window
        panel = pygame.Rect(0, 0, 600, 400)
        panel.center = (width // 2, height // 2)

        # Draw the panel background and border
        pygame.draw.rect(screen, (25, 35, 45), panel, border_radius=8)
        pygame.draw.rect(screen, (60, 160, 180), panel, 2, border_radius=8)

        # Calculate the grid dimensions
        grid_width = self.grid_size * self.tile_size
        grid_height = self.grid_size * self.tile_size
        
        # Calculate the starting position of the grid within the panel
        start_x = panel.centerx - grid_width // 2
        start_y = panel.centery - grid_height // 2

        # Draw labels for the source and output tiles
        FONT_DIR = Path(__file__).parent.parent / "Plus_Jakarta_Sans" / "static"
        label_font = pygame.font.Font(str(FONT_DIR / "PlusJakartaSans-Bold.ttf"), 22)

        # Draw the SOURCE and OUTPUT labels with different colors
        source_text = label_font.render("SOURCE >", True, (80, 220, 160))

        output_text = label_font.render("> OUTPUT", True, (230, 170, 90))

        # Calculate the positions for the labels relative to the grid
        source_pos = (start_x - 12, start_y + self.tile_size * 1.5)

        output_pos = (start_x + grid_width + 12, start_y + self.tile_size * 1.5)

        screen.blit(source_text, source_text.get_rect(midright=source_pos))

        screen.blit(output_text, output_text.get_rect(midleft=output_pos))

        # Draw the instruction text above the grid
        instruction_font = pygame.font.Font(str(FONT_DIR / "PlusJakartaSans-Bold.ttf"), 20)
        instruction = instruction_font.render("Click tiles to rotate. Connect SOURCE to OUTPUT.", True, (210, 210, 210))

        # Calculate the position of the instruction text above the panel
        screen.blit(instruction, instruction.get_rect(centerx=panel.centerx, y=panel.y + 25))
        
        # Get the powered tiles based on the current grid configuration
        powered_tiles = self.get_powered_tiles()

        # Draw the grid of tiles
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = start_x + col * self.tile_size
                y = start_y + row * self.tile_size

                # Draw the tile background and border
                tile_rect = pygame.Rect(x, y, self.tile_size - 4, self.tile_size - 4)
                pygame.draw.rect(screen, (40, 55, 65), tile_rect)
                pygame.draw.rect(screen, (80, 120, 140), tile_rect, 2)

                # Draw the circuit on the tile based on its type and rotation
                center_x = tile_rect.centerx
                center_y = tile_rect.centery

                # Get the tile type and rotation for the current tile
                tile_type = self.tile_types[row][col]
                rotation = self.grid[row][col]

                self.draw_circuit(screen, center_x, center_y, tile_type, rotation, powered=(row, col) in powered_tiles)

        # If the puzzle is solved, display a success message
        if self.solved:
            success_font = pygame.font.Font(None, 42)
            success_text = success_font.render("POWER RESTORED", True, (80, 240, 150))
            screen.blit(success_text, success_text.get_rect(centerx=panel.centerx, y=panel.bottom - 65))


    def handle_click(self, mouse_pos, screen):

        # Check if the puzzle is active before handling clicks
        if not self.active or self.solved:
            return
        
        # Get the size of the screen to calculate the position of the puzzle panel
        width, height = screen.get_size()

        panel = pygame.Rect(0, 0, 600, 400)
        panel.center = (width // 2, height // 2)

        # Calculate the grid dimensions
        grid_width = self.grid_size * self.tile_size
        grid_height = self.grid_size * self.tile_size

        # Calculate the starting position of the grid within the panel
        start_x = panel.centerx - grid_width // 2
        start_y = panel.centery - grid_height // 2

        mouse_x, mouse_y = mouse_pos

        col = (mouse_x - start_x) // self.tile_size
        row = (mouse_y - start_y) // self.tile_size

        # Check if the click is within the bounds of the grid
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.grid[row][col] = (self.grid[row][col] + 1) % 4

            if self.check_solution():
                self.solved = True
                self.success_start = pygame.time.get_ticks()
                print("Circuit connected!")

            # Debugging output to verify the tile rotation
            print("Rotated tile: ", row, col)
            print("New rotation: ", self.grid[row][col])
    

    def draw_circuit(self, screen, center_x, center_y, tile_type, rotation, powered=False):

        # Draw the circuit on the tile based on its type and rotation
        length = self.tile_size // 2 - 8
        color = (80, 240, 150) if powered else (80, 220, 230)
        thickness = 8
        
        # Define the directions for drawing the circuit lines
        directions = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

        # Determine the connections based on the tile type
        if tile_type == "straight":
            connections = [0, 2]
        else:
            connections = [0, 1]

        # Rotate the connections based on the tile's rotation
        for direction in connections:
            rotated_direction = (direction + rotation) % 4
            dx, dy = directions[rotated_direction]

            # Draw the line representing the circuit on the tile
            pygame.draw.line(
                screen,
                color,
                (center_x, center_y),
                (center_x + dx * length, center_y + dy * length),
                thickness
            )


    def get_connections(self, row, col):

        # Get the tile type and rotation for the specified tile
        tile_type = self.tile_types[row][col]
        rotation = self.grid[row][col]

        # Determine the base connections based on the tile type
        if tile_type == "straight":
            base_connections = [0, 2]
        else:
            base_connections = [0, 1]

        return [(direction + rotation) % 4 for direction in base_connections]


    def check_solution(self):
        
        # Check if the output tile is powered by verifying if it's connected to the source tile through the circuit
        end = (1, 2)

        return(end in self.get_powered_tiles()) and 1 in self.get_connections(*end)


    def get_powered_tiles(self):

        # Start from the SOURCE tile and perform a breadth-first search to find all connected tiles
        start = (1, 0)

        # If the SOURCE tile doesn't have a connection to the right, return an empty set
        if 3 not in self.get_connections(*start):
            return set()
        
        # Define the directions for moving in the grid
        directions = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]

        # Initialise a set to keep track of powerewd tiles and a queue for the search
        powered = {start}
        queue = [start]

        # Perform a search to find all connected tiles startinf from the SOURCE tile
        while queue:
            row, col = queue.pop(0)

            # Check each direction for connections and add connected tiles to the powered set
            for direction in self.get_connections(row, col):
                dr, dc = directions[direction]

                next_row = row + dr
                next_col = col + dc

                # Check if the next tile is within the grid bounds
                if not (0 <= next_row < self.grid_size and 0 <= next_col < self.grid_size):
                    continue
                
                # Check if the next tile has a connection back to the current tile
                opposite = (direction + 2) % 4

                if opposite in self.get_connections(next_row, next_col):
                    neighbor = (next_row, next_col)

                    if neighbor not in powered:
                        powered.add(neighbor)
                        queue.append(neighbor)

        return powered
    

    def update(self):
        if not self.active or not self.solved:
            return
        
        elapsed = pygame.time.get_ticks() - self.success_start

        if elapsed >= self.success_duration:
            self.close()