import pygame

Color = pygame.Color


# class
class Unit:
    """the block"""

    def __init__(self, color: Color, is_air: bool):
        self.color = color
        self.is_air = is_air
