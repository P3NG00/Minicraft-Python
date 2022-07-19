import data.display
import data.entity
import data.world
import data.block
import pygame

Color = pygame.Color
Font = pygame.font.Font
Surface = pygame.Surface
Vec = pygame.Vector2

Display = data.display.Display
Entity = data.entity.Entity
World = data.world.World
Block = data.block.Block


# constants
TITLE = "Minicraft"
SURFACE_SIZE = (800, 600)
FPS = 60.0
COLOR_BG = Color(128, 128, 128)
COLOR_DEBUG_CENTER = Color(0, 64, 255)
COLOR_DEBUG_INFO = Color(0, 0, 0)
COLOR_PLAYER = Color(255, 0, 0)
DEBUG_UI_SPACER = 5
FONT_SIZE = 16
BLOCK_SCALE = 25
BLOCK_SCALE_MIN = 1
WORLD_SIZE = (64, 48)
PLAYER_MOVE_SPEED = 3.0
PLAYER_JUMP_VELOCITY = 3.5
PLAYER_SIZE = Vec(0.75, 1.75)
GRAVITY = 10.0
CLOCK = pygame.time.Clock()


# blocks
BLOCK_AIR = Block("Air", Color(240, 255, 255), True)
BLOCK_DIRT = Block("Dirt", Color(96, 48, 0))
BLOCK_GRASS = Block("Grass", Color(32, 255, 16))


# runtime variables
running = True
debug = False
player = Entity(COLOR_PLAYER, Vec(0.75, 1.75), PLAYER_MOVE_SPEED, PLAYER_JUMP_VELOCITY, GRAVITY)
input_move = Vec(0)
input_jump = False
input_mouse_left = False
input_mouse_left_last = False

# init
pygame.init()
pygame.display.set_caption(TITLE)
surface = pygame.display.set_mode(SURFACE_SIZE)
display = Display(surface, WORLD_SIZE, BLOCK_SCALE)
player._pos = display.world_center.copy()

# default world generation
_blocks = []
_grass_level = (WORLD_SIZE[1] / 2) - 1
for y in range(WORLD_SIZE[1]):
    _block_layer = []
    for x in range(WORLD_SIZE[0]):
        if y > _grass_level:
            _block_layer.append(BLOCK_AIR)
        elif y == _grass_level:
            _block_layer.append(BLOCK_GRASS)
        else:
            _block_layer.append(BLOCK_DIRT)
    _blocks.append(_block_layer)
world = World(_blocks)
del _blocks, _grass_level, _block_layer, y, x

# font
font = Font("data/font/type_writer.ttf", FONT_SIZE)

def create_text_surface(text: str, color: Color) -> Surface:
    """returns a surface using the text and color"""
    return font.render(text, False, color)


# loop
while running:

    # handle events
    for event in pygame.event.get():

        match event.type:

            # window close request
            case pygame.QUIT:

                # end program
                running = False

            # key press
            case pygame.KEYDOWN:

                match event.key:

                    # key press 'end'
                    case pygame.K_END:

                        # end program
                        running = False

                    # key press 'page down'
                    case pygame.K_PAGEDOWN:

                        # minimize window
                        pygame.display.iconify()

                    # key press 'f12'
                    case pygame.K_F12:

                        # toggle debug mode
                        debug = not debug

                    # key press 'tab'
                    case pygame.K_TAB:

                        # toggle grid mode
                        display.show_grid = not display.show_grid

                    # key press movement
                    case pygame.K_w:
                        input_move.y -= 1
                    case pygame.K_a:
                        input_move.x -= 1
                    case pygame.K_s:
                        input_move.y += 1
                    case pygame.K_d:
                        input_move.x += 1
                    case pygame.K_SPACE:
                        input_jump = True

            # key release
            case pygame.KEYUP:

                match event.key:

                    # key release movement
                    case pygame.K_w:
                        input_move.y += 1
                    case pygame.K_a:
                        input_move.x += 1
                    case pygame.K_s:
                        input_move.y -= 1
                    case pygame.K_d:
                        input_move.x -= 1
                    case pygame.K_SPACE:
                        input_jump = False

            # mouse button press
            case pygame.MOUSEBUTTONDOWN:

                match event.button:

                    # left mouse button
                    case 1:
                        input_mouse_left = True

            # mouse button release
            case pygame.MOUSEBUTTONUP:

                match event.button:

                    # left mouse button
                    case 1:
                        input_mouse_left = False

            # mouse scrollwheel
            case pygame.MOUSEWHEEL:

                # adjust block scale
                display.block_scale += event.y
                # fix minimum scale
                if display.block_scale < BLOCK_SCALE_MIN:
                    display.block_scale = BLOCK_SCALE_MIN

    # event handling end


    # update

    # update player with input
    player.handle_input(input_move, input_jump)
    # update entities
    player.update(FPS)
    # update display handler
    display.update(player._pos)
    # update block mouse is hovering over
    _mouse_pos = Vec(pygame.mouse.get_pos())
    _mouse_pos.y = display.surface_size.y - _mouse_pos.y - 1
    _mouse_pos_block = ((_mouse_pos - display.surface_center) / display.block_scale) + player._pos
    # if valid location
    if input_mouse_left and \
       _mouse_pos_block.x >= 0 and _mouse_pos_block.x < display.world_size[0] and \
       _mouse_pos_block.y >= 0 and _mouse_pos_block.y < display.world_size[1]:
        # TODO remove below and interact with block
        # replace block with dirt
        world.set_block(int(_mouse_pos_block.x), int(_mouse_pos_block.y), BLOCK_DIRT)
    # update last input
    input_mouse_left_last = input_mouse_left


    # draw

    # fill background
    surface.fill(COLOR_BG)
    # draw world
    world.draw(display)
    # draw player
    player.draw(display)
    # draw debug
    if debug:
        # draw point in center of screen for debugging
        pygame.draw.circle(surface, COLOR_DEBUG_CENTER, display.surface_size / 2, 5)
        # draw debug info
        _debug_info = [f"surface_size: {display.surface_size.x}x{display.surface_size.y}",
                       f"world_size: {display.world_size[0]}x{display.world_size[1]}",
                       f"show_grid: {display.show_grid}",
                       f"fps: {CLOCK.get_fps():.3f}",
                       f"x: {player._pos.x:.3f}",
                       f"y: {player._pos.y:.3f}",
                       f"block_scale: {display.block_scale}",
                       f"mouse_x: {_mouse_pos_block.x:.3f} ({int(_mouse_pos_block.x)})",
                       f"mouse_y: {_mouse_pos_block.y:.3f} ({int(_mouse_pos_block.y)})"]
        surface.blits([(create_text_surface(_debug_info[i], COLOR_DEBUG_INFO), (DEBUG_UI_SPACER, ((FONT_SIZE + DEBUG_UI_SPACER) * i) + DEBUG_UI_SPACER)) for i in range(len(_debug_info))])


    # update display
    pygame.display.flip()
    # framerate tick
    CLOCK.tick(FPS)

    # loop end, loop again if running is True

# quit
pygame.quit()
