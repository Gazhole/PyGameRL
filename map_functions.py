import numpy as np
from itertools import product


def display_to_map(screen_x, screen_y):
    return int(screen_x / 16), int(screen_y / 16)


class GameMap:
    """
    Game Map object to store map data, annotations (blocked tiles etc), and pathfinding information.
    """
    def __init__(self, width, height, block_borders=True):
        self.width = width  # Map width in tiles.
        self.height = height  # Map height in tiles
        self.blocked = np.array([[False for y in range(height + 1)] for x in range(width + 1)], dtype=bool)  # Non-walkable tiles.

        if block_borders:
            self.block_borders()  # By default, make an impassable border on the ultimate boundaries of the map.

    def __iter__(self):
        # This is used to pass a tuple of tuples to represent all coordinates on the map.
        # Used for rendering iteration and pathfinding, and allows the class object to be iterated through.
        for xy in product(range(self.width), range(self.height)):
            yield xy

    def block_borders(self):
        for x, y in product(range(self.width), range(self.height)):
                if y == 0 or x == 0:
                    self.blocked[x, y] = True

                if y == self.height - 1 or x == self.width - 1:
                    self.blocked[x, y] = True


class MapChunk:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def __iter__(self):
        # coordinates = ((x, y) for y in range(self.y1, self.y2 + 1) for x in range(self.x1, self.x2 + 1))
        for xy in product(range(self.x1, self.x2 + 1), range(self.y1, self.y2 + 1)):
            yield xy


def get_visible_map_chunk(player, game_map, view_port_width, view_port_height):
    """
    Calculate a rect of the game map centered on the player, to fit the view port on screen.
    This will be recalculated each frame based on player position.
    Allows for a scrolling map in the view port.
    There should be handling of edges where there is no more "map" to scroll.

    :param player: player object
    :param game_map: game map object
    :param view_port_width: int - the width of the view port (map display) in pixels.
    :param view_port_height: int - the height of the view port (map display) in pixels.
    :return: map coordinates carving out a rect of the map which fits the view port.
    """
    # Work out the size (in map tiles) the view port represents.
    visible_width, visible_height = display_to_map(view_port_width, view_port_height)

    # Work out rect coordinates with player in the centre.
    map_chunk_x1 = player.map_x - int(visible_width * 0.5)
    map_chunk_y1 = player.map_y - int(visible_height * 0.5)
    map_chunk_x2 = map_chunk_x1 + visible_width
    map_chunk_y2 = map_chunk_y1 + visible_height

    # If the player cannot be centered because the map cannot scroll further, limit the scrolling.
    if map_chunk_x2 > game_map.width:
        map_chunk_x2 = game_map.width
        map_chunk_x1 = game_map.width - visible_width
    elif map_chunk_x1 < 0:
        map_chunk_x2 += -map_chunk_x1
        map_chunk_x1 = 0

    if map_chunk_y2 > game_map.height:
        map_chunk_y2 = game_map.height
        map_chunk_y1 = game_map.height - visible_height
    elif map_chunk_y1 < 0:
        map_chunk_y2 += -map_chunk_y1
        map_chunk_y1 = 0

    return MapChunk(map_chunk_x1, map_chunk_x2, map_chunk_y1, map_chunk_y2)

