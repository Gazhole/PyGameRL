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
    def __init__(self, name, map_x, map_y, colour, sprite=None, stats=None):
        super().__init__()
        # Set up flavour stuff.
        self.name = name
        self.colour = colour
        self.sprite = sprite

        # Set up map and game objects.
        self.map_x = map_x
        self.map_y = map_y
        self.blocks = True  # Does it block movement?

        # Set up graphics.
        self.surf = pygame.Surface((16, 16))

        # Stats n stuff
        self.stats = stats

        # If there is a sprite, blit it to the instance's surface. If not, just fill with a block of colour.
        if self.sprite:
            self.surf.blit(self.sprite, (0, 0))
        else:
            self.surf.fill(self.colour)

        self.rect = self.surf.get_rect()

    def get_map_position(self):
        # Simply returns the current map coordinates as integers.
        return self.map_x, self.map_y

    def move(self, dx, dy):
        # Alter position on map by the amount in the parameters.
        self.map_x += dx
        self.map_y += dy

    def attack(self, attack_target):
        damage = self.stats.s - attack_target.stats.d
        print("{} attacks {} for {} damage.".format(self.name, attack_target.name, damage))
        attack_target.take_damage(damage)

    def distance_to(self, other):
        dx = other.map_x - self.map_x
        dy = other.map_y - self.map_y
        return math.sqrt(dx ** 2 + dy ** 2)

    def take_damage(self, damage):
        self.stats.h -= damage


class Player(Entity):
    """
    Placeholder for the player class.
    """
    def __init__(self, name, map_x, map_y, colour, sprite=None, stats=None):
        super().__init__(name, map_x, map_y, colour, sprite, stats)


class Monster(Entity):
    """
    Monster class contains routines for AI and other things.
    """
    def __init__(self, name, map_x, map_y, colour, game_map, sprite=None, target=None, stats=None):
        super().__init__(name, map_x, map_y, colour, sprite, stats)
        self.flee = False  # Is the monster currently fleeing?
        self.target = target  # The monster's target (usually the player) chase and attack.
        self.dijkstra = np.array([[None for y in range(game_map.height + 1)] for x in range(game_map.width + 1)], dtype=float)

    def check_state(self, target):
        # TODO make the 0.25 flee threshold a creature stat.

        if self.stats.h <= int(self.stats.max_h * 0.25) and not self.flee:
            self.flee = True

        if self.flee and self.stats.h > int(self.stats.max_h * 0.25):
            self.flee = False

    # Main Monster AI routine.
    def take_turn(self, game_map, entities):
        self.update_dijkstra_map(game_map, self.target, entities)  # Update pathfinding map.
        dx, dy = self.calculate_path()  # Calculate the most appropriate tile to move into, return relative values.

        # Calculate destination coordinates.
        destination_x = self.map_x + dx
        destination_y = self.map_y + dy

        # Check if the tiles are walkable and that there are not any entities at that location.
        if not game_map.blocked[destination_x, destination_y] and not get_blocking_entities(entities, destination_x, destination_y):
            self.move(dx, dy)  # Move the monster.
        else:
            if self.distance_to(self.target) < 2:
                self.attack(self.target)

        # End of turn
        self.check_state(self.target)  # Check state - fleeing, death, etc

    # Update the pathfinding map.
    def update_dijkstra_map(self, game_map, target, entities):
        # Initialise a NoneType array for the game map.
        self.dijkstra[target.map_x, target.map_y] = 0  # Set target's location to value of 0.

        # Iterate through all map tiles and set the value of the tile to the distance (in tiles) away from the target.
        for x, y in game_map:
            if not game_map.blocked[x, y]:
                x_distance = x - target.map_x
                y_distance = y - target.map_y

                if x_distance < 0:
                    x_distance = x_distance * -1

                if y_distance < 0:
                    y_distance = y_distance * -1

                self.dijkstra[x, y] = x_distance + y_distance

        # Blank out other monsters so AI doesn't try to move there
        for entity in entities:
            if entity is not target:
                self.dijkstra[entity.map_x, entity.map_y] = None

        if self.flee:
            self.dijkstra = self.dijkstra * -1.2

    def calculate_path(self):
        """
        Calculate the best path towards the player based on the passed Dijkstra array of steps (integers).

        :return: dx and dy (integers) which dictate modifications to monsters x and y map coordinates.
        """

        # Create a dictionary -
        # Keys are the Dijkstra value (no. steps that tile is away from player).
        # Values are the position of the tile relative to the monster (dx and dy values)
        cell = dict()
        cell[self.dijkstra[(self.map_x - 1, self.map_y - 1)]] = (-1, -1)
        cell[self.dijkstra[(self.map_x, self.map_y - 1)]] = (0, -1)
        cell[self.dijkstra[(self.map_x + 1, self.map_y - 1)]] = (1, -1)
        cell[self.dijkstra[(self.map_x - 1, self.map_y)]] = (-1, 0)
        cell[self.dijkstra[(self.map_x, self.map_y)]] = (0, 0)
        cell[self.dijkstra[(self.map_x, self.map_y + 1)]] = (0, 1)
        cell[self.dijkstra[(self.map_x - 1, self.map_y + 1)]] = (-1, 1)
        cell[self.dijkstra[(self.map_x + 1, self.map_y)]] = (1, 0)
        cell[self.dijkstra[(self.map_x + 1, self.map_y + 1)]] = (1, 1)

        viable_tiles = [key for key in cell.keys() if str(key) != "nan"]  # Remove walls which are NoneType not int

        dx, dy = cell[min(viable_tiles)]  # Return the lowest key value aka the shortest path to player.

        return dx, dy


class StatBlock:
    def __init__(self, h, m, s, d):
        self.h = h
        self.m = m
        self.s = s
        self.d = d

        self.max_h = h
        self.max_m = m
