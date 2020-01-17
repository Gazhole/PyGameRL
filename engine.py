"""
A simple game.
"""

import pygame
from input_functions import handle_keys, get_inputs
from render_functions import render_all
from classes import Player, Monster
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
    entities.append(Monster("Orc", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))
    entities.append(Monster("Orc", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0)))

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

        if current_turn == Turn.player:

            # Get inputs and terminate loop if necessary.
            user_input, running = get_inputs(running)

            if not user_input:
                continue  # Continue with game loop.

            # Process actions
            else:
                # Process user input and get actions.
                action = handle_keys(user_input)

                # Action categories.
                move = action.get("move")
                attack = action.get("attack")  # Not used, just example.
                quit_game = action.get("quit")

                if quit_game:  # Triggered when ESC key is pressed.
                    running = False

                if move:  # If movement keys are pressed move player.
                    player_map_x, player_map_y = player.get_map_position()
                    dx, dy = move  # Pull relative values from action.

                    destination_x = player_map_x + dx
                    destination_y = player_map_y + dy

                    if not game_map.blocked[destination_x, destination_y]:  # Check if the tiles are walkable.
                        player.move(dx, dy)  # Move player.

                if attack:  # Not used, just example.
                    pass

            current_turn = Turn.monster  # Set turn state to monster.

        elif current_turn == Turn.monster:
            # Iterate through all entities.
            for entity in entities:
                if isinstance(entity, Monster):  # If the entity is a Monster
                    # Can the monster see the player (and vice versa), and is it not alerted to the player?
                    if (entity.map_x, entity.map_y) in visible_map_chunk:
                        entity.take_turn(game_map, player)

            current_turn = Turn.player  # Set to player's turn again.

# If the main game loop is broken, quit the game.
    pygame.quit()


if __name__ == "__main__":
    main()
