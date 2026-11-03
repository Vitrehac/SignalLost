import pygame


class LogViewer:
    def __init__(self, logs):

        # Initialize the log viewer with a list of logs
        self.active = False
        self.current_log = ""
        self.has_read_log = False


    def open(self, message):

        # Open the log viewer with the specified message
        self.current_log = message
        self.active = True
        self.has_read_log = True


    def close(self):

        # Close the log viewer
        self.active = False


    def draw(self, screen):

        # Draw the log viewer interface on the screen if it's active
        if not self.active:
            return
        
        # Get the screen dimensions
        width, height = screen.get_size()

        # Darken the game background with a transparent overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        # Draw the log viewer panel
        panel = pygame.Rect(0, 0, 650, 400)
        panel.center = (width // 2, height // 2)

        # Draw the panel background and border
        pygame.draw.rect(screen, (20, 30, 35), panel, border_radius=8)
        pygame.draw.rect(screen, (70, 180, 150), panel, 2, border_radius=8)

        # Draw the title and the log message on the panel
        title_font = pygame.font.Font(None, 36)
        body_font = pygame.font.Font(None, 26)

        title = title_font.render("FACILITY ARCHIVE", True, (80, 230, 170))
        screen.blit(title, (panel.x + 30, panel.y + 30))

        # Wrap the log message text to fit within the panel width
        lines = self.wrap_text(self.current_log, body_font, panel.width - 60)

        # Draw each line of the wrapped log message on the panel
        for index, line in enumerate(lines):
            rendered_line = body_font.render(line, True, (220, 220, 220))
            screen.blit(rendered_line, (panel.x + 30, panel.y + 110 + index * 32))

        # Draw the exit instruction at the bottom of the panel
        exit_text = body_font.render("ESC - Close", True, (140, 160, 160))
        screen.blit(exit_text, (panel.x + 30, panel.bottom - 45))

    
    def wrap_text(self, text, font, max_width):

        # Wrap the text to fit within the specified maximum width
        words = text.split()
        lines = []
        current_line = ""

        # Iterate through each word in the text and build lines that fit within the maximum width
        for word in words:
            test_line = f"{current_line} {word}".strip()

            # If the test line fits within the maximum width, update the current line
            if font.size(test_line)[0] <= max_width:
                current_line = test_line

            # If the test line exceeds the maximum width, add the current line to the list of lines and start a new line with the current word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
    
        # Add the last line to the list of lines if it's not empty
        if current_line:
            lines.append(current_line)

        return lines