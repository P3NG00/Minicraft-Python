import pygame
from . import display
from . import block

Display = display.Display
Block = block.Block

Vec = pygame.Vector2


class World:
    """holds block information"""

    def __init__(self, block_grid: list[list[Block]]):
        self.block_grid = block_grid

    def get_block(self, x: int, y: int) -> Block:
        """returns the block at the specified position"""
        return self.block_grid[y][x]

    def set_block(self, x: int, y: int, block: Block):
        """updates the block value of a position"""
        self.block_grid[y][x] = block

    def draw(self, display: Display):
        """draws all world blocks to the display surface"""
        _start_x = -(display.world_size[0] * display.block_scale) / 2
        _start_y = ((display.world_size[1] * display.block_scale) / 2) - display.block_scale
        for y in range(display.world_size[1]):
            for x in range(display.world_size[0]):
                _draw_pos = Vec(_start_x + (x * display.block_scale),
                                _start_y - (y * display.block_scale)) - display.camera_offset
                pygame.draw.rect(display.surface, self.get_block(x, y).color, (_draw_pos, Vec(display.block_scale)))
