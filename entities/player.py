import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 250

        self.width = 32
        self.height = 32

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )


    def handle_input(self):

        # Get the current state of all keyboard keys
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        # Check for movement keys and set the direction vector accordingly
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y = -1
            
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y = 1

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x = -1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x = 1

        if direction.length() > 0:
            direction = direction.normalize()

        return direction
       

    def update(self, dt, collision_system):

        # Handle player input and get the direction vector
        direction = self.handle_input()

        dx = direction.x * self.speed * dt
        dy = direction.y * self.speed * dt

        # Move the player using the collision system
        collision_system.move(self, dx, dy)


    def draw(self, screen, camera):

        # Draw the player as a red rectangle on the screen that's adjusted for the camera's offset
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(self))