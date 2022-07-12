import pygame

Surface = pygame.Surface
Vec = pygame.Vector2


class Display:

    def __init__(self, surface: Surface, unit_array_size: Vec, unit_scale: int):
        self.surface = surface
        self.surface_size = Vec(surface.get_size())
        self.surface_center = self.surface_size / 2
        self.camera_offset = -self.surface_center
        self.unit_array_size = unit_array_size
        self.unit_scale = unit_scale

    def update(self, player_pos: Vec):
        """updates camera offset to player position"""
        _camera_offset = -self.surface_center
        _camera_offset.x += player_pos.x * self.unit_scale
        _camera_offset.y -= player_pos.y * self.unit_scale
        self.camera_offset = _camera_offset
