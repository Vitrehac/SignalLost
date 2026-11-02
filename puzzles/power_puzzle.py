import pygame


class PowerPuzzle:
    def __init__(self):
        self.active = False
        self.solved = False

        self.grid_size = 3
        self.tile_size = 80
        self.grid = [
            [2, 0, 1],
            [0, 3, 0],
            [1, 2, 1]
        ]

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

        pygame.draw.rect(screen, (25, 35, 45), panel, border_radius=8)
        pygame.draw.rect(screen, (60, 160, 180), panel, 2, border_radius=8)

        grid_width = self.grid_size * self.tile_size
        grid_height = self.grid_size * self.tile_size

        start_x = panel.centerx - grid_width // 2
        start_y = panel.centery - grid_height // 2

        label_font = pygame.font.Font(None, 22)

        source_text = label_font.render("SOURCE >", True, (80, 220, 160))

        output_text = label_font.render("> OUTPUT", True, (230, 170, 90))

        source_pos = (start_x - 12, start_y + self.tile_size * 1.5)

        output_pos = (start_x + grid_width + 12, start_y + self.tile_size * 1.5)

        screen.blit(source_text, source_text.get_rect(midright=source_pos))

        screen.blit(output_text, output_text.get_rect(midleft=output_pos))

        instruction_font = pygame.font.Font(None, 24)
        instruction = instruction_font.render("Click tiles to rotate. Connect SOURCE to OUTPUT.", True, (210, 210, 210))

        screen.blit(instruction, instruction.get_rect(centerx=panel.centerx, y=panel.y + 25))
        print("hello, world")


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

                self.draw_circuit(screen, center_x, center_y, tile_type, rotation)

    def handle_click(self, mouse_pos, screen):

        # Check if the puzzle is active before handling clicks
        if not self.active:
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
                self.active = False
                print("Circuit connected! Power restored.")

            # Debugging output to verify the tile rotation
            print("Rotated tile: ", row, col)
            print("New rotation: ", self.grid[row][col])
    
    def draw_circuit(self, screen, center_x, center_y, tile_type, rotation):

        # Draw the circuit on the tile based on its type and rotation
        length = self.tile_size // 2 - 8
        color = (80, 220, 230)
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

        # Check if there is a valid path from the start tile to the end tile in the puzzle grid
        directions = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]

        start = (1, 0)
        end = (1, 2)

        if 3 not in self.get_connections(*start):
            return False

        if 1 not in self.get_connections(*end):
            return False

        queue = [start]
        visited = set()

        # Perform a search to find a valid path from the start tile to the end tile
        while queue:
            row, col = queue.pop(0)

            if (row, col) in visited:
                continue

            visited.add((row, col))

            if (row, col) == end:
                return True

            # Check the connections of the current tile and explore neighboring tiles
            for direction in self.get_connections(row, col):
                dr, dc = directions[direction]

                next_row = row + dr
                next_col = col + dc
                
                # Check if the next tile is within the bounds of the grid
                if not (0 <= next_row < self.grid_size and 0 <= next_col < self.grid_size):
                    continue

                opposite = (direction + 2) % 4

                # Check if the next tile has a connection back to the current tile
                if opposite in self.get_connections(next_row, next_col):
                    queue.append((next_row, next_col))
        return False