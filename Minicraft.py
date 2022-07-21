import data.block
import data.display
import data.entity
import data.world
import pygame
import random


# main
def main():

    Color = pygame.Color
    Surface = pygame.Surface
    Vec = pygame.Vector2

    # constants
    TITLE = "Minicraft"
    SURFACE_SIZE = (800, 600)
    FPS = 60
    COLOR_BG = Color(128, 128, 128)
    COLOR_FONT_DEBUG = Color(0, 0, 0)
    COLOR_FONT_UI = Color(255, 255, 255)
    UI_SPACER = 5
    FONT_SIZE = 16
    BLOCK_SCALE = 25
    BLOCK_SCALE_MAX = 75
    BLOCK_SCALE_MIN = 10
    WORLD_SIZE = (256, 256)
    TICKS_PER_SECOND = 64
    BLOCK_UPDATES_PER_TICK = 32
    GRAVITY = 10.0


    # variables
    running = True
    debug = False
    player = data.entity.Entity(Color(255, 0, 0), Vec(0.75, 1.75), 3.0, 3.5)
    input_move = Vec(0)
    input_jump = False
    input_mouse_left = False
    input_mouse_right = False
    input_mouse_left_last = False
    input_mouse_right_last = False

    # init
    pygame.init()
    pygame.display.set_caption(TITLE)
    surface = pygame.display.set_mode(SURFACE_SIZE, pygame.RESIZABLE)
    display = data.display.Display(surface, BLOCK_SCALE, FPS, TICKS_PER_SECOND)
    player.pos = Vec(WORLD_SIZE) / 2
    blocks = data.block.Blocks()
    current_block = blocks.Dirt

    # default world generation
    _blocks = []
    _dirt_level = int(WORLD_SIZE[1] / 2) - 1
    _stone_level = int(WORLD_SIZE[1] / 3)
    for y in range(WORLD_SIZE[1]):
        _block_layer = []
        for x in range(WORLD_SIZE[0]):
            if y > _dirt_level:
                _block_layer.append(blocks.Air)
            elif y == _dirt_level:
                _block_layer.append(blocks.Grass if random.random() < 0.8 else blocks.Dirt)
            elif y > _stone_level:
                _block_layer.append(blocks.Dirt)
            else:
                _block_layer.append(blocks.Stone)
        _blocks.append(_block_layer)
    world = data.world.World(_blocks, GRAVITY, BLOCK_UPDATES_PER_TICK)
    del _blocks, _dirt_level, _stone_level, _block_layer, y, x

    # font
    font = pygame.font.Font("data/font/type_writer.ttf", FONT_SIZE)

    def create_text_surface(text: str, color: Color) -> Surface:
        """returns a surface using the text and color"""
        return font.render(text, False, color)


    # main game loop
    while running:

        # add delta time
        display.tick_delta += display.delta_time()

        # update for every tick step
        while display.tick_delta >= display.tick_step:

            # decrement delta time by tick step
            display.tick_delta -= display.tick_step
            # increment total tick counter
            display.tick_total += 1


            # update

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

                            # key press block selection
                            case pygame.K_1:
                                current_block = blocks.Dirt
                            case pygame.K_2:
                                current_block = blocks.Grass
                            case pygame.K_3:
                                current_block = blocks.Stone

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

                            # mouse button left
                            case 1:
                                input_mouse_left = True

                            # mouse button right
                            case 3:
                                input_mouse_right = True

                    # mouse button release
                    case pygame.MOUSEBUTTONUP:

                        match event.button:

                            # mouse button left
                            case 1:
                                input_mouse_left = False

                            # mouse button right
                            case 3:
                                input_mouse_right = False

                    # mouse scrollwheel
                    case pygame.MOUSEWHEEL:

                        # adjust block scale
                        display.block_scale += event.y
                        # fix minimum scale
                        if display.block_scale < BLOCK_SCALE_MIN:
                            display.block_scale = BLOCK_SCALE_MIN
                        elif display.block_scale > BLOCK_SCALE_MAX:
                            display.block_scale = BLOCK_SCALE_MAX

                    # resize window
                    case pygame.VIDEORESIZE:

                        # update display info
                        display.update_surface_size(Vec(event.w, event.h))

            # event handling end

            # update player with input
            player.handle_input(input_move, input_jump)
            # update entities
            player.update(display, world)
            # update world
            world.update(blocks)
            # update display handler
            display.update(player)
            # get block position from mouse
            _mouse_pos = Vec(pygame.mouse.get_pos())
            _mouse_pos.y = display.surface_size.y - _mouse_pos.y - 1
            _mouse_pos_rel = ((_mouse_pos - display.surface_center) / display.block_scale) + player.pos
            _block_pos = (int(_mouse_pos_rel.x), int(_mouse_pos_rel.y))
            # catch out of bounds
            if _block_pos[0] >= 0 and _block_pos[0] < world.width and \
               _block_pos[1] >= 0 and _block_pos[1] < world.height:
                # if left click
                if input_mouse_left and not input_mouse_left_last:
                    # replace block with air
                    world.set_block(_block_pos[0], _block_pos[1], blocks.Air)
                # if right click
                if input_mouse_right and not input_mouse_right_last:
                    # replace block with current block
                    world.set_block(_block_pos[0], _block_pos[1], current_block)
            # update last input
            input_mouse_left_last = input_mouse_left
            input_mouse_right_last = input_mouse_right
        # end update loop


        # draw

        # fill background
        surface.fill(COLOR_BG)
        # draw world
        world.draw(display, player)
        # draw player
        player.draw(display)
        # draw current selected block name
        surface.blit(create_text_surface(f"block: {current_block.name}", COLOR_FONT_UI), (UI_SPACER, display.surface_size.y - FONT_SIZE - UI_SPACER))
        # draw debug
        if debug:
            # draw debug info
            _debug_info = [f"surface_size: {int(display.surface_size.x)}x{int(display.surface_size.y)}",
                           f"world_size: {world.width}x{world.height} ({world.width * world.height})",
                           f"ticks: {display.tick_total} ({display.tps}/tps)",
                           f"seconds: {(display.tick_total / display.tps):.3f}",
                           f"show_grid: {display.show_grid}",
                           f"fps: {display.clock.get_fps():.3f}",
                           f"x: {player.pos.x:.3f}",
                           f"y: {player.pos.y:.3f}",
                           f"block_scale: {display.block_scale}",
                           f"mouse_x: {_mouse_pos_rel.x:.3f} ({_block_pos[0]})",
                           f"mouse_y: {_mouse_pos_rel.y:.3f} ({_block_pos[1]})",
                           f"player_grounded: {player.is_grounded}"]
            # iterate through each debug string, create a text surface, and blit them from top to bottom
            surface.blits([(create_text_surface(_debug_info[i], COLOR_FONT_DEBUG), (UI_SPACER, ((FONT_SIZE + UI_SPACER) * i) + UI_SPACER)) for i in range(len(_debug_info))])


        # update display
        pygame.display.flip()
        # framerate tick
        display.clock.tick(display.fps)
    # game loop end


    # quit
    pygame.quit()


# boilerplate
if __name__ == "__main__":
    main()
