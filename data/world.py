import pygame
import random

Vec = pygame.Vector2


class World:
    """holds block information"""

    def __init__(self, block_grid: list[list], gravity: float):
        self.block_grid = block_grid
        self.width = len(block_grid[0])
        self.height = len(block_grid)
        self.gravity = gravity
        self.ticks = 0
        # makes tick rate scale for amount of blocks in world
        self.updates_per_second = int((self.width * self.height) / 2)
        # amount of time to wait to pass before updating
        self.update_step = 1.0 / self.updates_per_second
        self.update_ms = 0.0

    def get_block(self, x: int, y: int):
        """returns the block at the specified position"""
        return self.block_grid[y][x]

    def set_block(self, x: int, y: int, block):
        """updates the block value of a position"""
        self.block_grid[y][x] = block

    def update(self, display, blocks):
        """updates the world"""
        self.update_ms += display.fps_ms
        while self.update_ms >= self.update_step:
            self.ticks += 1
            self.update_ms -= self.update_step
            _rand_pos = (random.randrange(0, self.width), random.randrange(0, self.height))
            self.get_block(_rand_pos[0], _rand_pos[1]).update(_rand_pos, self, blocks)

    def draw(self, display):
        """draws all world blocks to the display surface"""
        _draw_scale = Vec(display.block_scale - 1 if display.show_grid else display.block_scale)
        # TODO make start/end only on screen
        for y in range(self.height):
            for x in range(self.width):
                _draw_pos = -display.camera_offset + Vec(x * display.block_scale,
                                                  (-y - 1) * display.block_scale)
                pygame.draw.rect(display.surface, self.get_block(x, y).color, (_draw_pos, _draw_scale))
