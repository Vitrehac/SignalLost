import pygame

class TileMap:
    def __init__(self):
        self.tile_size = 64

        # "#" represents walls, "." represents empty space
        self.room = [
            "########################",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "#......................#",
            "########################"
        ]

        self.obstacles = []

        # Create obstacles based on the room layout
        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):

                # If the tile is a wall, create a rectangle for it and add it to the obstacles list
                if tile == "#":
                    x = column_index * self.tile_size
                    y = row_index * self.tile_size
                    self.obstacles.append(pygame.Rect(x, y, self.tile_size, self.tile_size))

    def draw(self, screen, camera):
        # Draw the room's floor and walls based on the room layout
        for row_index, row in enumerate(self.room):
            for column_index, tile in enumerate(row):

                # Calculate the position of the tile in the world
                x = column_index * self.tile_size
                y = row_index * self.tile_size

                # Create a temporary entity to represent the tile's position in the world
                world_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                
                screen_rect = world_rect.move(
                    -camera.offset.x,
                    -camera.offset.y
                )

                # Draw the tile as a dark rectangle with a border
                if tile == "#":
                    color = (100, 100, 110)
                else:
                    color = (25, 25, 32)

                pygame.draw.rect(screen, color, screen_rect)
