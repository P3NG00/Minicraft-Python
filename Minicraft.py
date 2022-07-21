import data.block
import data.display
import data.entity
import data.world
import pygame
import random

Color = pygame.Color
Surface = pygame.Surface
Vec = pygame.Vector2


# main
def main():

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
    BLOCK_SCALE_MIN = 1
    WORLD_SIZE = (256, 256)
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
    display = data.display.Display(surface, BLOCK_SCALE, FPS)
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
    world = data.world.World(_blocks, GRAVITY)
    del _blocks, _dirt_level, _stone_level, _block_layer, y, x

    # font
    font = pygame.font.Font("data/font/type_writer.ttf", FONT_SIZE)

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

                # resize window
                case pygame.VIDEORESIZE:

                    # update display info
                    display.update_surface_size(Vec(event.w, event.h))

        # event handling end


        # update

        # update player with input
        player.handle_input(input_move, input_jump)
        # update entities
        player.update(world, display.fps)
        # update world
        world.update(display, blocks)
        # update display handler
        display.update(player)
        # get block position from mouse
        _mouse_pos = Vec(pygame.mouse.get_pos())
        _mouse_pos.y = display.surface_size.y - _mouse_pos.y - 1
        _mouse_pos_block = ((_mouse_pos - display.surface_center) / display.block_scale) + player.pos
        _mouse_pos_block_rounded = (int(_mouse_pos_block.x), int(_mouse_pos_block.y))
        # catch out of bounds
        try:
            # if left click
            if input_mouse_left and not input_mouse_left_last:
                # replace block with air
                world.set_block(_mouse_pos_block_rounded[0], _mouse_pos_block_rounded[1], blocks.Air)
            # if right click
            if input_mouse_right and not input_mouse_right_last:
                # replace block with current block
                world.set_block(_mouse_pos_block_rounded[0], _mouse_pos_block_rounded[1], current_block)
        except:
            pass
        # update last input
        input_mouse_left_last = input_mouse_left
        input_mouse_right_last = input_mouse_right


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
            _debug_info = [f"surface_size: {display.surface_size.x}x{display.surface_size.y}",
                        f"world_size: {world.width}x{world.height} ({world.width * world.height})",
                        f"world_ticks: {world.ticks} ({world.updates_per_second}/tick)",
                        f"world_time: {(world.ticks / world.updates_per_second):.3f}",
                        f"show_grid: {display.show_grid}",
                        f"fps: {display.clock.get_fps():.3f}",
                        f"x: {player.pos.x:.3f}",
                        f"y: {player.pos.y:.3f}",
                        f"block_scale: {display.block_scale}",
                        f"mouse_x: {_mouse_pos_block.x:.3f} ({_mouse_pos_block_rounded[0]})",
                        f"mouse_y: {_mouse_pos_block.y:.3f} ({_mouse_pos_block_rounded[1]})",
                        f"player_grounded: {player.is_grounded}"]
            surface.blits([(create_text_surface(_debug_info[i], COLOR_FONT_DEBUG), (UI_SPACER, ((FONT_SIZE + UI_SPACER) * i) + UI_SPACER)) for i in range(len(_debug_info))])
            del _mouse_pos, _mouse_pos_block, _mouse_pos_block_rounded, _debug_info


        # update display
        pygame.display.flip()
        # framerate tick
        display.clock.tick(display.fps)

        # loop end, loop again if running is True

    # quit
    pygame.quit()


if __name__ == "__main__":
    main()
