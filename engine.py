"""
A simple game.
"""

import pygame
from input_functions import handle_keys, get_inputs
from render_functions import render_all
from classes import Player, Monster, get_blocking_entities, StatBlock
from map_functions import GameMap, display_to_map, get_visible_map_chunk
from random import randint
from game_states import Turn


def main():

    # Initialise pygame.
    pygame.init()

    # Set up screen.
    screen_width = 800
    screen_height = 640
    screen_surface = pygame.display.set_mode([screen_width, screen_height])

    # Set up sprites:
    SPR_TREE = pygame.image.load('Sprites\\tree.png').convert_alpha()
    SPR_PLAYER = pygame.image.load('Sprites\\player.png').convert_alpha()
    SPR_ORC = pygame.image.load('Sprites\\orc.png').convert_alpha()

    sprites = {"player": SPR_PLAYER, "tree": SPR_TREE, "orc": SPR_ORC}

    # Set up view port constants for the area which will display the game map. HUD dimensions are derived from this.
    view_port_width = 800
    view_port_height = 480
    view_port_x_offset = 0
    view_port_y_offset = 50

    # Calculate a simple map which is double the screen size to test scrolling.
    map_width, map_height = display_to_map(screen_width * 2, screen_height * 2)  # Map size in 16px by 16px tiles

    # Create player and map objects.
    player_stats = StatBlock(h=100, m=0, s=10, d=10)
    player = Player("Player", map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(0, 255, 0), sprite=SPR_PLAYER, stats=player_stats)
    game_map = GameMap(map_width, map_height)  # Create a game map.

    # Create some random noise in the map.
    for x, y in game_map:
        if randint(1, 10) == 1:
            game_map.blocked[x, y] = True

    # List to store all the game entities. Populate with player.
    entities = list()
    entities.append(player)

    # Add some basic monsters.
    for mon in range(10):
        name = "Orc " + str(mon + 1)
        mon_stats = StatBlock(h=10, m=0, s=12, d=8)
        mon = Monster(name, map_x=randint(1, map_width - 1), map_y=randint(1, map_height - 1), colour=(255, 0, 0), game_map=game_map, sprite=SPR_ORC, stats=mon_stats)
        entities.append(mon)

    # Set the first turn as the player.
    current_turn = Turn.player

    # Main game loop.
    running = True
    while running:

        # Create a map chunk for iteration based on the rect boundaries.
        visible_map_chunk = get_visible_map_chunk(player, game_map, view_port_width, view_port_height)

        # Render the various screen elements. The placement of this determines whether player or enemies movement lag..
        render_all(screen_surface, screen_width, screen_height, view_port_width, view_port_height, view_port_x_offset,
                   view_port_y_offset, game_map, player, entities, visible_map_chunk, sprites)

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
        if current_turn == Turn.monster:
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
