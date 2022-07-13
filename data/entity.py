import pygame
from . import display

Display = display.Display

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
        _draw_pos.x = int(_draw_pos.x)
        _draw_pos.y = int(_draw_pos.y)
        # draw to surface
        pygame.draw.rect(display.surface, self._color, (_draw_pos, _current_size))

    def update(self, fps: float):
        """updates the entity using its values"""
        # add movement this frame
        self._pos += (self._vel / fps) * self._speed
        # TODO change below to check if not on ground
        # if self._vel.y != 0:
        #     self._vel.y -= self._gravity / fps
        # TODO take into account surrounding tiles

    def handle_input(self, movement: Vec, jump: bool):
        """uses the given variables to calculate movement"""
        # set horizontal movement
        # TODO change back to only horizontal movement
        # self._vel.x = movement.x
        self._vel.x = movement.x
        self._vel.y = -movement.y
        # check jump
        if jump and self._vel.y == 0:
            self._vel.y = self._jump_vel
