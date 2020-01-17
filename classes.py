import pygame
from copy import copy
import numpy as np


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
        self.flee = False

    def check_state(self, target):
        if self.map_x == target.map_x and self.map_y == target.map_y:
            self.flee = True

    def take_turn(self, game_map, target):
        dijkstra = self.update_dijkstra_map(game_map, target)
        dx, dy = self.calculate_path(dijkstra)

        destination_x = self.map_x + dx
        destination_y = self.map_y + dy

        if not game_map.blocked[destination_x, destination_y]:  # Check if the tiles are walkable.
            self.move(dx, dy)  # Move the monster.

        self.check_state(target)

    def update_dijkstra_map(self, game_map, target):
        dijkstra = np.array([[None for y in range(game_map.height + 1)] for x in range(game_map.width + 1)], dtype=float)
        dijkstra[target.map_x, target.map_y] = 0

        for x, y in game_map:
            if not game_map.blocked[x, y]:
                x_distance = x - target.map_x
                y_distance = y - target.map_y

                if x_distance < 0:
                    x_distance = x_distance * -1

                if y_distance < 0:
                    y_distance = y_distance * -1

                dijkstra[x, y] = x_distance + y_distance

        if self.flee:
            dijkstra = copy(dijkstra) * -1.2

        return dijkstra

    def calculate_path(self, dijkstra):
        """
        Calculate the best path towards the player based on the passed Dijkstra array of steps (integers).

        :param dijkstra_map: The dijkstra map the monster will be pathfinding with. This is a Numpy Array.
        :return: dx and dy (integers) which dictate modifications to monsters x and y map coordinates.
        """

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

        viable_tiles = [key for key in cell.keys() if str(key) != "nan"]  # Remove walls which are NoneType not int

        dx, dy = cell[min(viable_tiles)]  # Return the lowest key value aka the shortest path to player.

        return dx, dy

