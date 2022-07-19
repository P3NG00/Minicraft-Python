import pygame
from . import display
from . import block

Display = display.Display
Block = block.Block

Vec = pygame.Vector2


class World:
    """holds block information"""

    def __init__(self, block_grid: list[list[Block]], gravity: float):
        self.block_grid = block_grid
        self.gravity = gravity

    def get_block(self, x: int, y: int) -> Block:
        """returns the block at the specified position"""
        return self.block_grid[y][x]

    def set_block(self, x: int, y: int, block: Block):
        """updates the block value of a position"""
        self.block_grid[y][x] = block

    def draw(self, display: Display):
        """draws all world blocks to the display surface"""
        _draw_scale = Vec(display.block_scale - 1 if display.show_grid else display.block_scale)
        for y in range(display.world_size[1]):
            for x in range(display.world_size[0]):
                _draw_pos = -display.camera_offset + Vec(x * display.block_scale,
                                                  (-y - 1) * display.block_scale)
                pygame.draw.rect(display.surface, self.get_block(x, y).color, (_draw_pos, _draw_scale))
