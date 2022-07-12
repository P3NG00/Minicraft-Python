import data.display
import data.entity
import data.grid
import data.unit
import pygame

Color = pygame.Color
Font = pygame.font.Font
Surface = pygame.Surface
Vec = pygame.Vector2

Display = data.display.Display
Entity = data.entity.Entity
Grid = data.grid.Grid
Unit = data.unit.Unit


# constants
TITLE = "Minicraft"
SURFACE_SIZE = Vec(800, 600)
FPS = 60.0
COLOR_BG = Color(128, 128, 128)
COLOR_DEBUG_CENTER = Color(0, 64, 255)
COLOR_DEBUG_INFO = Color(0, 0, 0)
COLOR_UNIT_AIR = Color(240, 255, 255)
COLOR_UNIT_DIRT = Color(96, 48, 0)
COLOR_PLAYER = Color(255, 0, 0)
UNIT_SIZE = 25
UNIT_SIZE_MIN = 1
UNIT_ARRAY_SIZE = (32, 24)
PLAYER_MOVE_SPEED = 3.0
PLAYER_JUMP_VELOCITY = 3.5
PLAYER_SIZE = Vec(0.75, 1.75)
GRAVITY = 10.0

CLOCK = pygame.time.Clock()

UNIT_AIR = Unit(COLOR_UNIT_AIR, True)
UNIT_DIRT = Unit(COLOR_UNIT_DIRT, False)


# runtime variables
running = True
debug = False
player = Entity(COLOR_PLAYER, Vec(0.75, 1.75), PLAYER_MOVE_SPEED, PLAYER_JUMP_VELOCITY, GRAVITY)
input_move = Vec(0)
input_jump = False

# init
pygame.init()
pygame.display.set_caption(TITLE)
surface = pygame.display.set_mode(SURFACE_SIZE)
display = Display(surface, UNIT_ARRAY_SIZE, UNIT_SIZE)
grid = Grid([[UNIT_DIRT if y < (UNIT_ARRAY_SIZE[1] / 2) else UNIT_AIR for _ in range(UNIT_ARRAY_SIZE[0])] for y in range(UNIT_ARRAY_SIZE[1])])

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

                        # find clicked unit
                        # TODO account for centered unit size whatever
                        mouse_pos = Vec(pygame.mouse.get_pos())
                        x = int(mouse_pos.x / display.unit_scale)
                        y = int(mouse_pos.y / display.unit_scale)
                        # if valid unit area
                        if x >= 0 and \
                           y >= 0 and \
                           x < display.unit_array_size[0] and \
                           y < display.unit_array_size[1]:
                            # print of selected unit is air
                            print(grid.get_unit(x, y).is_air)

            # mouse scrollwheel
            case pygame.MOUSEWHEEL:

                # adjust size of units
                display.unit_scale += event.y
                # fix negative size
                if display.unit_scale < UNIT_SIZE_MIN:
                    display.unit_scale = UNIT_SIZE_MIN

    # event handling end


    # update

    # update player with input
    player.handle_input(input_move, input_jump)
    # update entities
    player.update(FPS)
    # update display handler
    display.update(player._pos)


    # draw

    # fill background
    surface.fill(COLOR_BG)
    # draw grid
    grid.draw(display)
    # draw player
    player.draw(display)
    # draw debug
    if debug:
        # draw point in center of screen for debugging
        pygame.draw.circle(surface, COLOR_DEBUG_CENTER, SURFACE_SIZE / 2, 5)
        # draw debug info
        _debug_info = [f"x: {player._pos.x:.3f}",
                       f"y: {player._pos.y:.3f}"]
        _draw_height = 0
        for i in range(len(_debug_info)):
            _text_surface = font_debug.render(_debug_info[i], False, COLOR_DEBUG_INFO)
            _debug_info[i] = (_text_surface, (0, _draw_height))
            _draw_height += _text_surface.get_height()
        surface.blits(_debug_info)


    # update display
    pygame.display.flip()
    # framerate tick
    CLOCK.tick(FPS)

    # loop end, loop again if running is True

# quit
pygame.quit()
