import pygame

Surface = pygame.Surface
Vec = pygame.Vector2


# class
class Entity:

    def __init__(self):
        self.pos = Vec(0)

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, )
        pass
