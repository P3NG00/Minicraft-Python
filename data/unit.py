import pygame
import random

Color = pygame.Color
Surface = pygame.Surface
Vec = pygame.Vector2


# class
class Unit:

    def __init__(self):
        self.randomize_color()

    def randomize_color(self) -> None:
        """randomizes this unit's color"""
        self.color = Color(random.randrange(0, 256),
                           random.randrange(0, 256),
                           random.randrange(0, 256))

    def draw(self, surface: Surface, pos: Vec, size: Vec) -> None:
        """draws this unit to the surface"""
        global UNIT_SQUARE
        pygame.draw.rect(surface, self.color, (pos, size))
