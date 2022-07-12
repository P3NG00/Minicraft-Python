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
SURFACE_SIZE = Vec(800, 600)
FPS = 60.0
COLOR_BG = Color(128, 128, 128)
COLOR_DEBUG_CENTER = Color(0, 64, 255)
COLOR_DEBUG_INFO = Color(0, 0, 0)
COLOR_BLOCK_AIR = Color(240, 255, 255)
COLOR_BLOCK_DIRT = Color(96, 48, 0)
COLOR_PLAYER = Color(255, 0, 0)
DEBUG_UI_SPACER = 5
BLOCK_SCALE = 25
BLOCK_SCALE_MIN = 1
WORLD_SIZE = (32, 24)
PLAYER_MOVE_SPEED = 3.0
PLAYER_JUMP_VELOCITY = 3.5
PLAYER_SIZE = Vec(0.75, 1.75)
GRAVITY = 10.0

CLOCK = pygame.time.Clock()

BLOCK_AIR = Block(COLOR_BLOCK_AIR)
BLOCK_DIRT = Block(COLOR_BLOCK_DIRT)


# runtime variables
running = True
debug = False
player = Entity(COLOR_PLAYER, Vec(0.75, 1.75), PLAYER_MOVE_SPEED, PLAYER_JUMP_VELOCITY, GRAVITY)
input_move = Vec(0)
input_jump = False
input_mouse_left = False

# init
pygame.init()
pygame.display.set_caption(TITLE)
surface = pygame.display.set_mode(SURFACE_SIZE)
display = Display(surface, WORLD_SIZE, BLOCK_SCALE)
world = World([[BLOCK_DIRT if y < (WORLD_SIZE[1] / 2) else BLOCK_AIR for _ in range(WORLD_SIZE[0])] for y in range(WORLD_SIZE[1])])

# font
font_debug = Font("data/font/type_writer.ttf", 16)
# font_type_w95fa = Font("data/font/W95FA.otf", 24) # TODO utilize


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

    if input_mouse_left:
        # find clicked block
        # TODO account for camera offset and flipped y
        _mouse_pos = Vec(pygame.mouse.get_pos())
        x = int(_mouse_pos.x / display.block_scale)
        y = int((display.surface_size.y - _mouse_pos.y) / display.block_scale)
        # if valid location
        if x >= 0 and \
           y >= 0 and \
           x < display.world_size[0] and \
           y < display.world_size[1]:
            # print of selected block is air
            print(f"is air {x}, {y}: {world.get_block(x, y) is BLOCK_AIR}")


    # draw

    # fill background
    surface.fill(COLOR_BG)
    # draw worldf
    world.draw(display)
    # draw player
    player.draw(display)
    # draw debug
    if debug:
        # draw point in center of screen for debugging
        pygame.draw.circle(surface, COLOR_DEBUG_CENTER, SURFACE_SIZE / 2, 5)
        # draw debug info
        _debug_info = [f"fps: {CLOCK.get_fps():.3f}",
                       f"x: {player._pos.x:.3f}",
                       f"y: {player._pos.y:.3f}"]
        _draw_height = DEBUG_UI_SPACER
        for i in range(len(_debug_info)):
            _text_surface = font_debug.render(_debug_info[i], False, COLOR_DEBUG_INFO)
            _debug_info[i] = (_text_surface, (DEBUG_UI_SPACER, _draw_height))
            _draw_height += _text_surface.get_height() + DEBUG_UI_SPACER
        surface.blits(_debug_info)


    # update display
    pygame.display.flip()
    # framerate tick
    CLOCK.tick(FPS)

    # loop end, loop again if running is True

# quit
pygame.quit()
