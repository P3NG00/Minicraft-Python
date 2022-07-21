import math
import pygame
import random

Vec = pygame.Vector2


class World:
    """holds block information"""

    def __init__(self, block_grid: list[list], gravity: float, block_updates_per_tick: int):
        self.block_grid = block_grid
        self.width = len(block_grid[0])
        self.height = len(block_grid)
        self.area = self.width * self.height
        self.gravity = gravity
        self.block_updates_per_tick = block_updates_per_tick

    def get_block(self, x: int, y: int):
        """returns the block at the specified position"""
        return self.block_grid[y][x]

    def set_block(self, x: int, y: int, block):
        """updates the block value of a position"""
        self.block_grid[y][x] = block

    def update(self, blocks):
        """updates the world"""
        for _ in range(self.block_updates_per_tick):
            _rand_pos = (random.randrange(0, self.width), random.randrange(0, self.height))
            self.get_block(_rand_pos[0], _rand_pos[1]).update(_rand_pos, self, blocks)

    def draw(self, display, player):
        """draws all world blocks to the display surface"""
        _draw_scale = Vec(display.block_scale - 1 if display.show_grid else display.block_scale)
        # find edge to start drawing
        _visual_width = math.ceil(display.surface_size.x / display.block_scale) + 2
        _visual_height = math.ceil(display.surface_size.y / display.block_scale) + 2
        _visual_start_x = math.floor(player.pos.x - (_visual_width / 2.0))
        _visual_start_y = math.floor(player.pos.y - (_visual_height / 2.0))
        # fix variables if outside of bounds
        if _visual_start_x < 0:
            _visual_width += _visual_start_x
            _visual_start_x = 0
        if _visual_start_y < 0:
            _visual_height += _visual_start_y
            _visual_start_y = 0
        if _visual_width >= self.width - _visual_start_x:
            _visual_width = self.width - _visual_start_x - 1
        if _visual_height >= self.height - _visual_start_y:
            _visual_height = self.height - _visual_start_y - 1
        # draw each visible block
        for y in range(_visual_height):
            for x in range(_visual_width):
                _x = x + _visual_start_x
                _y = y + _visual_start_y
                _draw_pos = -display.camera_offset + Vec((_x) * display.block_scale,
                                                    (-1 - _y) * display.block_scale)
                pygame.draw.rect(display.surface, self.get_block(_x, _y).color, (_draw_pos, _draw_scale))
