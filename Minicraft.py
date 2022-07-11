import pygame

Color = pygame.Color
Vec = pygame.Vector2


# changable constants
TITLE = "Minicraft"
SURFACE_SIZE = Vec(800, 600)
FPS = 60
COLOR_BG = Color(128, 128, 128)
COLOR_LINE = Color(255, 0, 0)

# dependable constants
CLOCK = pygame.time.Clock()

# runtime variables
running = True

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

    # draw
    # TODO DONT DRAW LIKE THIS EVERY FRAME
    # fill background
    surface.fill(COLOR_BG)
    # draw test line from top-left to bottom-right
    pygame.draw.line(surface, COLOR_LINE, (0, 0), SURFACE_SIZE)

    # update display
    pygame.display.flip()
    # framerate tick
    CLOCK.tick(FPS)

    # loop end, loop again if running is True

# quit
pygame.quit()
