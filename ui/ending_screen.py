from pathlib import Path
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

        # Initialize fonts
        FONT_DIR = Path(__file__). parent.parent / "Plus_Jakarta_Sans" / "static"
        title_font = pygame.font.Font(str(FONT_DIR / "PlusJakartaSans-Bold.ttf"), 48)
        text_font = pygame.font.Font(str(FONT_DIR / "PlusJakartaSans-Regular.ttf"), 24)

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