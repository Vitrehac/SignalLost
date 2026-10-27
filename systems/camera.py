import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height


    def update(self, target):

        # Follow the target
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.y = target.rect.centery - self.height // 2

        # Keep camera within the bounds of the world
        self.offset.x = max(0, min(self.offset.x, self.width - self.width_))
        self.offset.y = max(0, min(self.offset.y, self.height - self.height_))

        pass

    def apply(self, entity):
        
        # Return the entity's screen position
        return entity.rect.move(-self.offset.x, -self.offset.y)

        pass

