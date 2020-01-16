import pygame


class Entity(pygame.sprite.Sprite):
    """
    This is the root class for all game entities.
    All entities have a name, a map location, and eventually a sprite which will be stored here too.
    """
    def __init__(self, name, map_x, map_y, colour):
        super().__init__()
        # Set up flavour stuff.
        self.name = name

        # Set up map and game objects.
        self.map_x = map_x
        self.map_y = map_y

        # Set up graphics.
        self.surf = pygame.Surface((16, 16))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect()

    def get_map_position(self):
        # Simply returns the current map coordinates as integers.
        return self.map_x, self.map_y

    def move(self, dx, dy):
        # Alter position on map by the amount in the parameters.
        self.map_x += dx
        self.map_y += dy


class Player(Entity):
    """
    Placeholder for the player class.
    """
    def __init__(self, name, map_x, map_y, colour):
        super().__init__(name, map_x, map_y, colour)


class Monster(Entity):
    """
    Monster class contains routines for AI and other things.
    """
    def __init__(self, name, map_x, map_y, colour):
        super().__init__(name, map_x, map_y, colour)
        self.alerted = False  # Has the monster seen the player yet? This dictates pathfinding towards player on/off.

    def calculate_path(self, dijkstra_map):
        """
        Calculate the best path towards the player based on the passed Dijkstra array of steps (integers).

        :param dijkstra_map: The dijkstra map the monster will be pathfinding with. This is a Numpy Array.
        :return: dx and dy (integers) which dictate modifications to monsters x and y map coordinates.
        """
        dijkstra = dijkstra_map

        # Create a dictionary -
        # Keys are the Dijkstra value (no. steps that tile is away from player).
        # Values are the position of the tile relative to the monster (dx and dy values)
        cell = dict()
        cell[dijkstra[(self.map_x - 1, self.map_y - 1)]] = (-1, -1)
        cell[dijkstra[(self.map_x, self.map_y - 1)]] = (0, -1)
        cell[dijkstra[(self.map_x + 1, self.map_y - 1)]] = (1, -1)
        cell[dijkstra[(self.map_x - 1, self.map_y)]] = (-1, 0)
        cell[dijkstra[(self.map_x, self.map_y)]] = (0, 0)
        cell[dijkstra[(self.map_x, self.map_y + 1)]] = (0, 1)
        cell[dijkstra[(self.map_x - 1, self.map_y + 1)]] = (-1, 1)
        cell[dijkstra[(self.map_x + 1, self.map_y)]] = (1, 0)
        cell[dijkstra[(self.map_x + 1, self.map_y + 1)]] = (1, 1)

        viable_tiles = [key for key in cell.keys() if isinstance(key, int)]  # Remove walls which are NoneType not int

        dx, dy = cell[min(viable_tiles)]  # Return the lowest key value aka the shortest path to player.

        return dx, dy

