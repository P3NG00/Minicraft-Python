import pygame
import random

Color = pygame.Color
Vec = pygame.Vector2


# changable constants
TITLE = "Minicraft"
SURFACE_SIZE = Vec(800, 600)
FPS = 60
COLOR_BG = Color(128, 128, 128)
COLOR_LINE = Color(255, 0, 0)
UNIT_SIZE = 20
UNIT_ARRAY_SIZE = (15, 10)


# dependable constants
CLOCK = pygame.time.Clock()
UNIT_SQUARE = Vec(UNIT_SIZE)
UNIT_ARRAY_SIZE_RANGE = (range(UNIT_ARRAY_SIZE[0]),
                         range(UNIT_ARRAY_SIZE[1]))


# class
class Unit:

    def __init__(self):
        self.randomize_color()

    def randomize_color(self) -> None:
        """randomizes this unit's color"""
        self.color = Color(random.randrange(0, 256),
                           random.randrange(0, 256),
                           random.randrange(0, 256))

    def draw(self, pos: Vec) -> None:
        """draws this unit to the surface"""
        pygame.draw.rect(surface, self.color, (pos, UNIT_SQUARE))


# function
def get_unit(x: int, y: int) -> Unit:
    """returns the unit at the given position"""
    return unit_array[y][x]


# runtime variables
running = True
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

            # mouse press
            case pygame.MOUSEBUTTONDOWN:

                print(event.button)

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
                            unit = get_unit(x, y)
                            unit.randomize_color()

            # mouse scrollwheel
            case pygame.MOUSEWHEEL:

                # adjust size of units
                UNIT_SIZE += event.y
                # fix negative size
                if UNIT_SIZE < 0:
                    UNIT_SIZE = 0
                # fix unit square value
                UNIT_SQUARE = Vec(UNIT_SIZE)
    # event handling end

    # draw
    # fill background
    surface.fill(COLOR_BG)
    # draw units
    for y in UNIT_ARRAY_SIZE_RANGE[1]:
        for x in UNIT_ARRAY_SIZE_RANGE[0]:
            get_unit(x, y).draw(Vec(x, y) * UNIT_SIZE)

    # update display
    pygame.display.flip()
    # framerate tick
    CLOCK.tick(FPS)

    # loop end, loop again if running is True

# quit
pygame.quit()
