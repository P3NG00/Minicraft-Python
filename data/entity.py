import pygame

Color = pygame.Color
Surface = pygame.Surface
Vec = pygame.Vector2


# class
class Entity:

    def __init__(self, color: Color, dimensions: Vec):
        self._color = color
        self._dims = dimensions
        self._pos = Vec(0)

    def draw(self, surface: Surface, camera_offset: Vec, unit_scale: int) -> None:
        """uses the current camera offset and unit scale to draw the entity to the surface"""
        _current_size = self._dims * unit_scale
        _rel_pos = self._pos * unit_scale
        _draw_offset = Vec(_current_size.x / 2, _current_size.y)
        _draw_pos = _rel_pos - _draw_offset - camera_offset
        pygame.draw.rect(surface, self._color, (_draw_pos, _current_size))

    def move(self, movement: Vec) -> None:
        self._pos += movement
