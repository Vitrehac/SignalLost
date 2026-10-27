class Level:
    def __init__(self):
        self.obstacles = []
        self.create_room()

    def create_room(self):
        # Define walls and objects in the room
        
        # Left wall
        self.obstacles.append(pygame.Rect(400, 200, 300, 40))

        # Right wall
        self.obstacles.append(pygame.Rect(400, 240, 40, 200))

        # Bottom wall
        self.obstacles.append(pygame.Rect(700, 400, 300, 40))

        # Top wall
        self.obstacles.append(pygame.Rect(0, 0, 800, 20))

    def draw(self, screen, camera):
        # Draw the room's walls and objects
        for obstacle in self.obstacles