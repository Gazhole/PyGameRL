"""
A simple game.
"""

import pygame
from input_functions import handle_keys, get_inputs
from render_functions import render_all
from classes import Player, Monster, get_blocking_entities
from map_functions import GameMap, display_to_map, MapChunk, get_visible_map_chunk
from random import randint
from game_states import Turn


def main():

    # Initialise pygame.
    pygame.init()

    # Set up screen.
    screen_width = 800
    screen_height = 640
    screen_surface = pygame.display.set_mode([screen_width, screen_height])

    # Set up view port constants for the area which will display the game map. HUD dimensions are derived from this.
    view_port_width = 800
    view_port_height = 480
    view_port_x_offset = 0
    view_port_y_offset = 50

    # Calculate a simple map which is double the screen size to test scrolling.
    map_width, map_height = display_to_map(screen_width * 2, screen_height * 2)  # Map size in 16px by 16px tiles

    # Create player and map objects.
    player = Player("Player", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(0, 255, 0))
    game_map = GameMap(map_width, map_height)  # Create a game map.

    # Create some random noise in the map.
    for x, y in game_map:
        if randint(1, 10) == 1:
            game_map.blocked[x, y] = True

    # List to store all the game entities. Populate with player.
    entities = list()
    entities.append(player)

    # Add some basic monsters.
    entities.append(Monster("Orc 1", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc 2", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc 3", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc 4", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc 5", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc 6", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))

    # Set the first turn as the player.
    current_turn = Turn.player

    # Main game loop.
    running = True
    while running:

        # Get rect boundaries representing the visible part of the map.
        map_chunk_x1, map_chunk_x2, map_chunk_y1, map_chunk_y2 = get_visible_map_chunk(player, game_map, view_port_width, view_port_height)

        # Create a map chunk for iteration based on the rect boundaries.
        visible_map_chunk = MapChunk(map_chunk_x1, map_chunk_x2, map_chunk_y1, map_chunk_y2)

        # Render the various screen elements.
        render_all(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset,
                   view_port_y_offset, game_map, player, entities, visible_map_chunk)

        # Start Player Turn
        if current_turn == Turn.player:

            # Get inputs and terminate loop if necessary.
            user_input, running = get_inputs(running)

            if not user_input:
                continue  # If no input continue with game loop.

            # Process actions
            else:
                # Process user input and get actions.
                action = handle_keys(user_input)

                # Action categories.
                move = action.get("move")
                quit_game = action.get("quit")

                if quit_game:  # Triggered when ESC key is pressed.
                    running = False

                if move:  # If movement keys are pressed move player.
                    player_map_x, player_map_y = player.get_map_position()
                    dx, dy = move  # Pull relative values from action.

                    # Calculate potential new coordinates
                    destination_x = player_map_x + dx
                    destination_y = player_map_y + dy

                    if not game_map.blocked[destination_x, destination_y]:  # Check if the tiles are walkable.
                        attack_target = get_blocking_entities(entities, destination_x, destination_y)  # Is there a monster at the destination?

                        # if there is an entity at the location...
                        if attack_target:
                            if isinstance(attack_target, Monster):  # ... and it's a monster
                                player.attack(attack_target)  # Attack it.
                        else:
                            player.move(dx, dy)  # If the cell is empty, move player into it.

            current_turn = Turn.monster  # Set turn state to monster.

        # Start Monster Turn
        elif current_turn == Turn.monster:
            # Iterate through all entities.
            for entity in entities:
                if isinstance(entity, Monster):  # If the entity is a Monster
                    # Can the monster see the player (and vice versa).
                    if (entity.map_x, entity.map_y) in visible_map_chunk:
                        if not entity.target:  # If the monster doesn't have a target, set it to the player.
                            entity.target = player

                        # Process monster turn ai
                        entity.take_turn(game_map, entities)

            current_turn = Turn.player  # Set to player's turn again.

    # If the main game loop is broken, quit the game.
    pygame.quit()


if __name__ == "__main__":
    main()
