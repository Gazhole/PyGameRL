import pygame

# Set up colours.
CLR_WHITE = (255, 255, 255)
CLR_BLACK = (0, 0, 0)
CLR_BLUE = (0, 0, 255)
CLR_RED = (255, 0, 0)
CLR_GREEN = (0, 255, 0)
CLR_YELLOW = (255, 255, 0)


def map_coords_to_pixels(map_x, map_y):
    """
    Simple conversion function to transform map coordinates into screen coordinates for drawing sprites.
    :param map_x: (int) The map coordinate x axis (tiles)
    :param map_y: (int) The map coordinate y axis (tiles)
    :return: pixes
    """
    return int(map_x * 16), int(map_y * 16)


def render_all(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset,
               view_port_y_offset, game_map, player, entities, visible_map_chunk):
    """

    :param screen_surface: obj - the main pygame drawing surface.
    :param screen_width: int - screen width in pixels
    :param screen_height: int - screen height in pixels
    :param view_port_width: int - width in pixels of the screen segment which displays the map
    :param view_port_height: int - height in pixels of the screen segment which displays the map
    :param view_port_x_offset: int - pixels to shift view port to the left.
    :param view_port_y_offset: int - pixels to shift view port down.
    :param game_map: game map object
    :param player: player object
    :param entities: list - tracking all entities in game.
    :return:
    """
    # Set the background colour of the window to black.
    screen_surface.fill(CLR_BLACK)

    # Invoke individual draw functions.
    render_map(screen_surface, view_port_x_offset, view_port_y_offset, game_map, visible_map_chunk)
    render_entities(screen_surface, view_port_x_offset, view_port_y_offset, entities, visible_map_chunk)
    render_bottom_hud(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset, view_port_y_offset, player)
    render_top_hud(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset, view_port_y_offset, player)

    # Refresh the display.
    pygame.display.flip()


def render_top_hud(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset, view_port_y_offset, player):
    hud_screen_x1 = view_port_x_offset
    hud_screen_x2 = view_port_x_offset + view_port_width
    hud_screen_y1 = 0
    hud_screen_y2 = view_port_y_offset

    hud_width = hud_screen_x2 - hud_screen_x1
    hud_height = hud_screen_y2 - hud_screen_y1

    draw_element(screen_surface, hud_screen_x1, hud_screen_y1, hud_width, hud_height, CLR_YELLOW)


def render_bottom_hud(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset, view_port_y_offset, player):
    hud_screen_x1 = view_port_x_offset
    hud_screen_x2 = view_port_x_offset + view_port_width
    hud_screen_y1 = view_port_y_offset + view_port_height
    hud_screen_y2 = screen_height

    hud_width = hud_screen_x2 - hud_screen_x1
    hud_height = hud_screen_y2 - hud_screen_y1

    draw_element(screen_surface, hud_screen_x1, hud_screen_y1, hud_width, hud_height, CLR_BLUE)


def render_map(screen_surface, view_port_x_offset, view_port_y_offset, game_map, visible_map_chunk):
    map_chunk_x1 = visible_map_chunk.x1
    map_chunk_y1 = visible_map_chunk.y1

    # Draw walls (blocked tiles).
    for x, y in visible_map_chunk:

        floor_colour = CLR_WHITE
        wall_colour = CLR_RED

        if game_map.blocked[x, y]:  # If it's a wall, work out its screen position, create filled surface and blit.
            tile_colour = wall_colour
        else:
            tile_colour = floor_colour

        # Calculate screen position for tile. Draw it!
        tile_screen_x, tile_screen_y = map_coords_to_pixels(x - map_chunk_x1, y - map_chunk_y1)
        draw_element(screen_surface, tile_screen_x + view_port_x_offset, tile_screen_y + view_port_y_offset, 16, 16, tile_colour)


def render_entities(screen_surface, view_port_x_offset, view_port_y_offset, entities, visible_map_chunk):
    map_chunk_x1 = visible_map_chunk.x1
    map_chunk_y1 = visible_map_chunk.y1

    # Iterate through entities and blit it's surface to the screen.
    for entity in entities:
        entity_screen_x, entity_screen_y = map_coords_to_pixels(entity.map_x - map_chunk_x1, entity.map_y - map_chunk_y1)
        screen_surface.blit(entity.surf, (entity_screen_x + view_port_x_offset, entity_screen_y + view_port_y_offset))


def draw_element(screen_surface, screen_x, screen_y, element_width, element_height, colour):
    element_surface = pygame.Surface((element_width, element_height))
    element_surface.fill(colour)
    screen_surface.blit(element_surface, (screen_x, screen_y))
