class CollisionSystem:

    def __init__(self, obstacles):
        self.obstacles = obstacles

    def move(self, player, dx, dy):

        # Horizontal movement
        player.rect.x += dx

        for obstacle in self.obstacles:
            if player.rect.colliderect(obstacle):
                if dx >0:
                    player.rect.right = obstacle.left
                
                elif dx < 0:
                    player.rect.left = obstacle.right
        
        # Synchronize the player's position
        player.x = player.rect.x
        player.y = player.rect.y