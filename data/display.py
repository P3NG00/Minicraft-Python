import pygame

Surface = pygame.Surface
Vec = pygame.Vector2


class Display:
    """holds information regarding visual display"""

    def __init__(self, surface: Surface, world_size: Vec, block_scale: int):
        self.surface = surface
        self.surface_size = Vec(surface.get_size())
        self.surface_center = self.surface_size / 2
        self.camera_offset = -self.surface_center
        self.world_size = world_size
        self.block_scale = block_scale

    def update(self, player_pos: Vec):
        """updates camera offset to center the player in the display"""
        _camera_offset = -self.surface_center
        _camera_offset.x += player_pos.x * self.block_scale
        _camera_offset.y -= player_pos.y * self.block_scale
        self.camera_offset = _camera_offset
