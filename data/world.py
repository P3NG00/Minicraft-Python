import data.block
import math
import pygame
import random

Blocks = data.block.Blocks

Vec = pygame.Vector2


class World:
    """holds block information"""

    def __init__(self, block_grid: list[list], gravity: float, block_updates_per_tick: int):
        self.block_grid = block_grid
        self.width = len(block_grid[0])
        self.height = len(block_grid)
        self.gravity = gravity
        self.block_updates_per_tick = block_updates_per_tick

    def get_block(self, x: int, y: int):
        """returns the block at the specified position"""
        return self.block_grid[y][x]

    def set_block(self, x: int, y: int, block):
        """updates the block value of a position"""
        self.block_grid[y][x] = block

    def update(self):
        """updates the world"""
        for _ in range(self.block_updates_per_tick):
            _rand_pos = (random.randrange(0, self.width), random.randrange(0, self.height))
            self.get_block(_rand_pos[0], _rand_pos[1]).update(_rand_pos, self)

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

    def generate_world(world_size: tuple[int, int], gravity: float, block_updates_per_tick: int):
        # TODO adjust _chunk_width, _height_variation, and _scan_radius variables for different effects
        # create world of air blocks for modification
        world = World([[Blocks.Air for _ in range(world_size[0])] for _ in range(world_size[1])], gravity, block_updates_per_tick)
        # create height map
        _chunk_width = 16
        _rel_width = int(world.width / _chunk_width)
        _mid_height = int(world.height / 2)
        _height_variation = 32
        _heightmap = []
        for _ in range(_rel_width):
            _height = _mid_height + random.randrange(-_height_variation, _height_variation)
            for _ in range(_chunk_width):
                _heightmap.append(_height)
        del _chunk_width, _rel_width, _mid_height, _height_variation, _height, _
        # smooth height map
        _scan_radius = 32
        _heightmap_smooth = []
        _current_heights = []
        _third_height = int(world.height / 3)
        for x in range(world.width):
            # get average height of surrounding area
            for scan_x in range(-_scan_radius, _scan_radius):
                _x = x + scan_x
                _current_heights.append(_heightmap[_x] if _x >= 0 and _x < world.width else _third_height)
            _heightmap_smooth.append(round(sum(_current_heights) / len(_current_heights)))
            _current_heights.clear()
        del _scan_radius, _current_heights, x, scan_x, _x
        # place blocks using height map
        for x in range(world.width):
            for y in range(_heightmap_smooth[x]):
                _block = Blocks.Dirt
                _height_max = _heightmap_smooth[x] - 1
                if y == _height_max:
                    _block = Blocks.Grass
                elif y < _height_max - 32:
                    _block = Blocks.Stone
                world.set_block(x, y, _block)
        del _block, _height_max, x, y
        # return generated world
        return world
