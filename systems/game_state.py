import pygame

class GameState:
    def __init__(self):
        self.power_restored = False
        self.control_room_entered = False
        self.computer_read = False
        self.security_unlocked = False
        self.containment_entered = False
        self.security_disabled = False