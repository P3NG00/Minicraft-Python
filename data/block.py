import pygame
import random

Color = pygame.Color
Vec = pygame.Vector2


# block class
class Block:

    def __init__(self, name: str, color: Color, is_air: bool = False):
        self.name = name
        self.color = color
        self.is_air = is_air

    def update(self, position: tuple[int, int], world):
        pass

# grass block class
class BlockGrass(Block):

    def __init__(self):
        super().__init__("Grass", Color(32, 255, 16))
        self._spread_offsets = [(x, y) for y in [-1, 0, 1] for x in [-1, 1]]

    def update(self, position: tuple[int, int], world):
        # if able to spread
        if position[1] + 1 == world.height or world.get_block(position[0], position[1] + 1).is_air:
            # check blocks to spread to
            _offset = self._spread_offsets[random.randrange(0, len(self._spread_offsets))]
            _check_pos = (position[0] + _offset[0], position[1] + _offset[1])
            try:
                _block = world.get_block(_check_pos[0], _check_pos[1])
                if _block is Blocks.Dirt and (_check_pos[1] + 1 == world.height or world.get_block(_check_pos[0], _check_pos[1] + 1).is_air):
                    world.set_block(_check_pos[0], _check_pos[1], Blocks.Grass)
            except IndexError:
                pass
        else:
            world.set_block(position[0], position[1], Blocks.Dirt)

# blocks class
class Blocks:

    Air = Block("Air", Color(240, 255, 255), True)
    Dirt = Block("Dirt", Color(96, 48, 0))
    Grass = BlockGrass()
    Stone = Block("Stone", Color(192, 192, 192))
