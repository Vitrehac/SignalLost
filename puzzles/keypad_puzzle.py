import pygame


class KeypadPuzzle:
    def __init__(self):

        # Set the puzzle password and timer when it's solved
        self.active = False
        self.solved =False
        self.correct_code = "6767"
        self.entered_code = ""
        self.message = ""
        self.success_start = None
        self.success_duration = 2000


    def open(self):

        # Open the puzzle if it hasn't been solved yet
        if not self.solved:
            self.active = True
            self.entered_code = ""
            self.message = ""
    
    def close(self):
        self.active = False

    def handle_key(self, key):

        # Handle the key for the puzzle
        if not self.active or self.solved:
            return
        
        if pygame.K_0 <= key <= pygame.K_9:

            if len(self.entered_code) < 4:
                self.entered_code += chr(key)

        elif key == pygame.K_BACKSPACE:
            self.entered_code = self.entered_code[:-1]

        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            
            # Print the messages accordingly based on the typed code
            if self.entered_code == self.correct_code:
                self.solved = True
                self.message = "ACCESS GRANTED"
                self.success_start = pygame.time.get_ticks()

            else:
                self.message = "ACCESS DENIED"
                self.entered_code = ""
    
    def draw(self, screen):
        if not self.active:
            return

        width, height = screen.get_size()

        # Darken the game background so it's clear a user has entered a different "game mode"
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))


        # Create the keypad panel
        panel = pygame.Rect(0, 0, 420, 320)
        panel.center = (width // 2, height // 2)

        pygame.draw.rect(screen, (25, 35, 45), panel, border_radius=8)
        pygame.draw.rect(screen, (200, 160, 60), panel, 2, border_radius=8)

        # Title
        title_font = pygame.font.Font(None, 34)
        code_font = pygame.font.Font(None, 54)
        small_font = pygame.font.Font(None, 25)
        title = title_font.render("SECURITY ACCESS", True, (230, 190, 90))
        screen.blit(title, title.get_rect(centerx=panel.centerx, y=panel.y + 30))

        # Entered code & hide unused digits
        display_code = self.entered_code + "_" * (4 - len(self.entered_code))
        code_text = code_font.render(display_code, True, (230, 230, 230))
        screen.blit(code_text, code_text.get_rect(centerx=panel.centerx, y=panel.y + 105))

        # Success or error feedback
        feedback_color = (80, 240, 150) if self.solved else (240, 100, 100)
        feedback = small_font.render(self.message, True, feedback_color)
        screen.blit(feedback, feedback.get_rect(centerx=panel.centerx, y=panel.y + 185))

        # Controls
        controls = small_font.render("ENTER: Confirm | BACKSPACE: Delete", True, (160, 170, 180))
        exit_text = small_font.render("ESC: Close", True, (160, 170, 180))
        screen.blit(controls, controls.get_rect(centerx=panel.centerx, y=panel.bottom - 65))
        screen.blit(exit_text, exit_text.get_rect(centerx=panel.centerx, y=panel.bottom - 35))


    def update(self):
        if not self.active or not self.solved:
            return

        elapsed = pygame.time.get_ticks() - self.success_start

        if elapsed >= self.success_duration:
            self.close()
