import pygame

class Level:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.wall_thickness = 20
        self.obstacles = []
        self.create_room()


    def create_room(self):
        # Create a simple room with walls
        # Bottom wall
        self.obstacles.append(pygame.Rect(0, self.height - self.wall_thickness, self.width, self.wall_thickness))

        # Top wall
        self.obstacles.append(pygame.Rect(0, 0, self.width, self.wall_thickness))

        # Left wall
        self.obstacles.append(pygame.Rect(0, 0, self.wall_thickness, self.height))

        # Right wall
        self.obstacles.append(pygame.Rect(self.width - self.wall_thickness, 0, self.wall_thickness, self.height))
      
    def draw(self, screen, camera):
        # Draw the room's obstacles
        for obstacle in self.obstacles:
            screen_rect = obstacle.move(-camera.offset.x, - camera.offset.y)
            pygame.draw.rect(screen, (100, 100, 110), screen_rect)
