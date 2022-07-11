import data.entity
import data.unit
import pygame

Color = pygame.Color
Vec = pygame.Vector2

Entity = data.entity.Entity
Unit = data.unit.Unit


# changable constants
TITLE = "Minicraft"
SURFACE_SIZE = Vec(800, 600)
FPS = 60
COLOR_BG = Color(128, 128, 128)
COLOR_PLAYER = Color(255, 0, 0)
UNIT_SIZE = 20
UNIT_SIZE_MIN = 1
UNIT_ARRAY_SIZE = (15, 10)


# dependable constants
CLOCK = pygame.time.Clock()
SURFACE_SIZE_HALF = SURFACE_SIZE / 2
UNIT_ARRAY_SIZE_RANGE = (range(UNIT_ARRAY_SIZE[0]),
                         range(UNIT_ARRAY_SIZE[1]))


# function
def get_unit(x: int, y: int) -> Unit:
    """returns the unit at the given position"""
    return unit_array[y][x]


# runtime variables
running = True
player = Entity(COLOR_PLAYER, Vec(0.8, 1.75))
input_move = Vec(0)
camera_offset = -SURFACE_SIZE_HALF.copy()
unit_array = [[Unit() for _ in UNIT_ARRAY_SIZE_RANGE[0]]
                      for _ in UNIT_ARRAY_SIZE_RANGE[1]]


# init
pygame.init()
pygame.display.set_caption(TITLE)
surface = pygame.display.set_mode(SURFACE_SIZE)


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

                    # key press movement
                    case pygame.K_w:
                        input_move.y -= 1
                    case pygame.K_a:
                        input_move.x -= 1
                    case pygame.K_s:
                        input_move.y += 1
                    case pygame.K_d:
                        input_move.x += 1

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

            # mouse press
            case pygame.MOUSEBUTTONDOWN:

                match event.button:

                    # mouse press 'left'
                    case 1:

                        # find clicked unit
                        mouse_pos = Vec(pygame.mouse.get_pos())
                        x = int(mouse_pos.x / UNIT_SIZE)
                        y = int(mouse_pos.y / UNIT_SIZE)
                        # if valid unit area randomize color
                        if x >= 0 and \
                           y >= 0 and \
                           x < UNIT_ARRAY_SIZE[0] and \
                           y < UNIT_ARRAY_SIZE[1]:
                            get_unit(x, y).randomize_color()

            # mouse scrollwheel
            case pygame.MOUSEWHEEL:

                # adjust size of units
                UNIT_SIZE += event.y
                # fix negative size
                if UNIT_SIZE < UNIT_SIZE_MIN:
                    UNIT_SIZE = UNIT_SIZE_MIN

    # event handling end


    # update

    # move player
    player.move(input_move / FPS)


    # draw

    # fill background
    surface.fill(COLOR_BG)
    # draw units
    _start_x = -(UNIT_ARRAY_SIZE[0] * UNIT_SIZE) / 2
    _start_y = -(UNIT_ARRAY_SIZE[1] * UNIT_SIZE) / 2
    for y in UNIT_ARRAY_SIZE_RANGE[1]:
        for x in UNIT_ARRAY_SIZE_RANGE[0]:
            _draw_pos = Vec(_start_x + (x * UNIT_SIZE),
                            _start_y + (y * UNIT_SIZE)) - camera_offset
            get_unit(x, y).draw(surface, _draw_pos, UNIT_SIZE)
    player.draw(surface, camera_offset, UNIT_SIZE)


    # update display
    pygame.display.flip()
    # framerate tick
    CLOCK.tick(FPS)

    # loop end, loop again if running is True

# quit
pygame.quit()
