import pygame
from . import display
from . import unit

Display = display.Display
Unit = unit.Unit

Vec = pygame.Vector2


class Grid:

    def __init__(self, unit_grid: list[list[Unit]]):
        self.unit_grid = unit_grid

    def get_unit(self, x: int, y: int) -> Unit:
        """returns the unit at the specified position"""
        return self.unit_grid[y][x]

    def draw(self, display: Display):
        """draws all grid units to the display surface"""
        # TODO only draw what can be seen on screen
        _start_x = -(display.unit_array_size[0] * display.unit_scale) / 2
        _start_y = ((display.unit_array_size[1] * display.unit_scale) / 2) - display.unit_scale
        for y in range(display.unit_array_size[1]):
            for x in range(display.unit_array_size[0]):
                _draw_pos = Vec(_start_x + (x * display.unit_scale),
                                _start_y - (y * display.unit_scale)) - display.camera_offset
                pygame.draw.rect(display.surface, self.get_unit(x, y).color, (_draw_pos, Vec(display.unit_scale)))
