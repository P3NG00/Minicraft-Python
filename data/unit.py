import pygame

Color = pygame.Color
Surface = pygame.Surface
Vec = pygame.Vector2


# class
class Unit:

    def __init__(self, color: Color, is_air: bool):
        self._color = color
        self._is_air = is_air

    def draw(self, surface: Surface, pos: Vec, unit_scale: int):
        """draws this unit to the surface"""
        pygame.draw.rect(surface, self._color, (pos, Vec(unit_scale)))
