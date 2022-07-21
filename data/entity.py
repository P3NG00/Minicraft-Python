import math
import pygame

Color = pygame.Color
Vec = pygame.Vector2


# class
class Entity:

    def __init__(self, color: Color, dimensions: Vec, move_speed: float, jump_velocity: float):
        self.color = color
        self.dimensions = dimensions
        self.speed = move_speed
        self.jump_velocity = jump_velocity
        self.pos = Vec(0)
        self.velocity = Vec(0)
        self.is_grounded = False

    def draw(self, display):
        """uses the current camera offset and block scale to draw the entity to the surface"""
        # get current screen size of player
        _current_size = self.dimensions * display.block_scale
        # find offset to reach top-left corner for draw pos
        _draw_offset = Vec(_current_size.x / 2, _current_size.y)
        # get relative screen position
        _rel_pos = self.pos * display.block_scale
        # flip screen y position
        _rel_pos.y *= -1
        # find final screen draw position
        _draw_pos = _rel_pos - _draw_offset - display.camera_offset
        # round draw position
        _draw_pos.x = math.ceil(_draw_pos.x)
        _draw_pos.y = math.ceil(_draw_pos.y)
        # draw to surface
        pygame.draw.rect(display.surface, self.color, (_draw_pos, _current_size))

    def update(self, display, world):
        """updates the entity"""
        # add movement this frame
        if not self.is_grounded:
            self.velocity.y -= world.gravity * display.delta_time()
        self.pos += (self.velocity * display.delta_time()) * self.speed
        if not world.get_block(int(self.pos.x), int(self.pos.y)).is_air:
            self.pos.y = math.ceil(self.pos.y)
            self.velocity.y = 0
            self.is_grounded = True
        # TODO take into account wall tiles

    def handle_input(self, movement: Vec, jump: bool):
        """uses the given variables to calculate movement"""
        # set horizontal movement
        self.velocity.x = movement.x
        # check jump
        if jump and self.velocity.y == 0:
            self.velocity.y = self.jump_velocity
            self.is_grounded = False
