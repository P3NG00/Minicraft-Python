import pygame

Surface = pygame.Surface
Vec = pygame.Vector2


class Display:
    """holds information regarding visual display"""

    def __init__(self, surface: Surface, block_scale: int, fps: int):
        self.surface = surface
        self.update_surface_size(Vec(surface.get_size()))
        self.block_scale = block_scale
        self.fps = fps
        self.show_grid = False
        self.clock = pygame.time.Clock()

    def delta_time(self) -> float:
        """returns the amount of time the last frame took"""
        return self.clock.get_time() / 1000.0

    def update_surface_size(self, surface_size: Vec):
        """updates display variables using size of surface"""
        self.surface_size = surface_size
        self.surface_center = self.surface_size / 2
        self.camera_offset = -self.surface_center

    def update(self, player):
        """updates camera offset to center the player in the display"""
        _camera_offset = -self.surface_center
        _camera_offset.x = round(_camera_offset.x + (player.pos.x * self.block_scale))
        _camera_offset.y = round(_camera_offset.y - (player.pos.y * self.block_scale))
        self.camera_offset = _camera_offset
