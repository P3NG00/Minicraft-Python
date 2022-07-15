import pygame

Color = pygame.Color


# class
class Block:

    def __init__(self, name: str, color: Color, is_air: bool = False):
        self.name = name
        self.color = color
        self.is_air = is_air
