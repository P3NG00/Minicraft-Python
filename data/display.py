import pygame

Surface = pygame.Surface
Vec = pygame.Vector2


class Display:
    """holds information regarding visual display"""

    def __init__(self, surface: Surface, world_size: tuple[int, int], block_scale: int):
        self.surface = surface
        self.update_surface_size(Vec(surface.get_size()))
        self.world_size = world_size
        self.world_center = Vec(self.world_size) / 2
        self.block_scale = block_scale
        self.show_grid = False

    def update_surface_size(self, surface_size: Vec): # TODO add type specifier
        self.surface_size = surface_size
        self.surface_center = self.surface_size / 2
        self.camera_offset = -self.surface_center

    def update(self, player_pos: Vec):
        """updates camera offset to center the player in the display"""
        _camera_offset = -self.surface_center
        _camera_offset.x = round(_camera_offset.x + (player_pos.x * self.block_scale))
        _camera_offset.y = round(_camera_offset.y - (player_pos.y * self.block_scale))
        self.camera_offset = _camera_offset
