import math
import pygame
from . import display
from . import world

Display = display.Display
World = world.World

Color = pygame.Color
Vec = pygame.Vector2


# class
class Entity:

    def __init__(self, color: Color, dimensions: Vec, move_speed: float, jump_velocity: float, gravity: float):
        self._color = color
        self._dims = dimensions
        self._speed = move_speed
        self._jump_vel = jump_velocity
        self._gravity = gravity
        self._pos = Vec(0)
        self._vel = Vec(0)
        self._grounded = False

    def draw(self, display: Display):
        """uses the current camera offset and block scale to draw the entity to the surface"""
        # get current screen size of player
        _current_size = self._dims * display.block_scale
        # find offset to reach top-left corner for draw pos
        _draw_offset = Vec(_current_size.x / 2, _current_size.y)
        # get relative screen position
        _rel_pos = self._pos * display.block_scale
        # flip screen y position
        _rel_pos.y *= -1
        # find final screen draw position
        _draw_pos = _rel_pos - _draw_offset - display.camera_offset
        # round draw position
        _draw_pos.x = round(_draw_pos.x)
        _draw_pos.y = round(_draw_pos.y)
        # draw to surface
        pygame.draw.rect(display.surface, self._color, (_draw_pos, _current_size))

    def update(self, world: World, fps: float):
        """updates the entity"""
        # add movement this frame
        if not self._grounded:
            self._vel.y -= self._gravity / fps
        self._pos += (self._vel / fps) * self._speed
        if not world.get_block(int(self._pos.x), int(self._pos.y)).is_air:
            self._pos.y = math.ceil(self._pos.y)
            self._vel.y = 0
            self._grounded = True
        # TODO take into account wall tiles

    def handle_input(self, movement: Vec, jump: bool):
        """uses the given variables to calculate movement"""
        # set horizontal movement
        self._vel.x = movement.x
        # check jump
        if jump and self._vel.y == 0:
            self._vel.y = self._jump_vel
            self._grounded = False
