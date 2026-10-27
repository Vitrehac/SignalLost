import pygame

class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        
        # Initialize the camera with screen and world dimensions
        self.offset = pygame.Vector2(0, 0)

        # Store the screen and world dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Store the world dimensions
        self.world_width = world_width
        self.world_height = world_height


    def update(self, target):

        # Follow the target
        self.offset.x = target.rect.centerx - self.screen_width // 2
        self.offset.y = target.rect.centery - self.screen_height // 2

        # Keep camera within the bounds of the world
        self.offset.x = max(0, min(self.offset.x, self.world_width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.world_height - self.screen_height))

        pass

    def apply(self, entity):
        
        # Return the entity's screen position
        return entity.rect.move(-self.offset.x, -self.offset.y)

        pass

