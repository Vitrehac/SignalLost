class CollisionSystem:

    def __init__(self, obstacles):
        self.obstacles = obstacles

    def move(self, player, dx, dy):

        # Horizontal movement
        player.rect.x += dx
        player.rect.x = round(player.rect.x)

        for obstacle in self.obstacles:
            if player.rect.colliderect(obstacle):
                if dx > 0:
                    player.rect.right = obstacle.left
                elif dx < 0:
                    player.rect.left = obstacle.right

                player.x = player.rect.x
        
        # Vertical movement
        player.y += dy
        player.rect.y = round(player.y)

        for obstacle in self.obstacles:
            if player.rect.colliderect(obstacle):
                if dy > 0:
                    player.rect.bottom = obstacle.top
                elif dy < 0:
                    player.rect.top = obstacle.bottom
                
                player.y = player.rect.y
