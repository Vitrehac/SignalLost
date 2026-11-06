import pygame


class EndingScreen:
    def __init__(self):
        self.active = False

    def open(self):
        self.active = True
    
    def draw(self, screen):
        if not self.active:
            return

        width, height = screen.get_size()
        screen.fill((8, 12, 20))
        title_font = pygame.font.Font(None, 64)
        text_font = pygame.font.Font(None, 30)

        lines = [
            "CONTAINMENT ARCHIVE HAS BEEN RECOVERED",
            "",
            "THANKS FOR PLAYING SIGNAL LOST",
            "",
            "Press ESC to exit"
        ]

        for index, line in enumerate(lines):
            font = title_font if line == "SIGNAL LOST" else text_font
            text = font.render(line, True, (220, 230, 235))
            rect = text.get_rect(center=(width // 2, 90 + index * 48))
            screen.blit(text, rect)