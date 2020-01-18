import pygame
from copy import copy
import numpy as np
import math


# Get the entity currently occupying the destination tile. Or return None.
def get_blocking_entities(entities, destination_map_x, destination_map_y):
    for entity in entities:
        if entity.blocks and entity.map_x == destination_map_x and entity.map_y == destination_map_y:
            return entity
    return None


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
        self.blocks = True  # Does it block movement?

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

    def attack(self, attack_target):
        print("{} attacks {}".format(self.name, attack_target.name))

    def distance_to(self, other):
        dx = other.map_x - self.map_x
        dy = other.map_y - self.map_y
        return math.sqrt(dx ** 2 + dy ** 2)


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
    def __init__(self, name, map_x, map_y, colour, target=None):
        super().__init__(name, map_x, map_y, colour)
        self.flee = False  # Is the monster currently fleeing?
        self.target = target  # The monster's target (usually the player) chase and attack.

    def check_state(self, target):
        # Later - if hp < 90% set self.flee to True and vice versa.
        if self.map_x == target.map_x and self.map_y == target.map_y:
            self.flee = True

    # Main Monster AI routine.
    def take_turn(self, game_map, entities):
        dijkstra = self.update_dijkstra_map(game_map, self.target, entities)  # Update pathfinding map.
        dx, dy = self.calculate_path(dijkstra)  # Calculate the most appropriate tile to move into, return relative values.

        # Calculate destination coordinates.
        destination_x = self.map_x + dx
        destination_y = self.map_y + dy

        # Check if the tiles are walkable and that there are not any entities at that location.
        if not game_map.blocked[destination_x, destination_y] and not get_blocking_entities(entities, destination_x, destination_y):
            self.move(dx, dy)  # Move the monster.
        else:
            if self.distance_to(self.target) < 2:
                self.attack(self.target)

        # Check state of self at the end of turn.
        self.check_state(self.target)

    # Update the pathfinding map.
    def update_dijkstra_map(self, game_map, target, entities):
        # Initialise a NoneType array for the game map.
        dijkstra = np.array([[None for y in range(game_map.height + 1)] for x in range(game_map.width + 1)], dtype=float)
        dijkstra[target.map_x, target.map_y] = 0  # Set target's location to value of 0.

        # Iterate through all map tiles and set the value of the tile to the distance (in tiles) away from the target.
        for x, y in game_map:
            if not game_map.blocked[x, y]:
                x_distance = x - target.map_x
                y_distance = y - target.map_y

                if x_distance < 0:
                    x_distance = x_distance * -1

                if y_distance < 0:
                    y_distance = y_distance * -1

                dijkstra[x, y] = x_distance + y_distance

        # Blank out other monsters so AI doesn't try to move there
        for entity in entities:
            if entity is not target:
                dijkstra[entity.map_x, entity.map_y] = None

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


