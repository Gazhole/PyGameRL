import pygame
import pygame.locals as pygame_locals

# # Set keys.
# Key constants.
K_UP = pygame_locals.K_UP
K_DOWN = pygame_locals.K_DOWN
K_LEFT = pygame_locals.K_LEFT
K_RIGHT = pygame_locals.K_RIGHT
K_ESCAPE = pygame_locals.K_ESCAPE
K_Q = pygame.locals.K_q
K_W = pygame.locals.K_w
K_A = pygame.locals.K_a
K_S = pygame.locals.K_s
# Event types.
KEYDOWN = pygame_locals.KEYDOWN
QUIT = pygame_locals.QUIT


def get_inputs(running):
    game_running = running

    # Iterate through event queue and handle game events.
    for event in pygame.event.get():

        # If the event type is KEYDOWN, the user has pressed a key.
        if event.type == KEYDOWN:
            user_input = event  # Assign event to input variable and break the loop.
            break

        elif event.type == QUIT:
            game_running = False  # Quit game.

    else:
        user_input = None  # If event queue completes with no user_input, set to None.

    return user_input, game_running


def handle_keys(event):
    """
    Take the pygame event, check for user key presses and return a dictionary with the
    movement direction (tuple), or a quit flag as a bool.

    :param event: pygame event object.
    :return: a dict with results.
    """

    if event.key == K_UP:
        return {"move": (0, -1)}
    elif event.key == K_DOWN:
        return {"move": (0, 1)}
    elif event.key == K_LEFT:
        return {"move": (-1, 0)}
    elif event.key == K_RIGHT:
        return {"move": (1, 0)}
    elif event.key == K_Q:
        return {"move": (-1, -1)}
    elif event.key == K_W:
        return {"move": (1, -1)}
    elif event.key == K_A:
        return {"move": (-1, 1)}
    elif event.key == K_S:
        return {"move": (1, 1)}

    if event.key == K_ESCAPE:
        return {"quit": True}

    return {}
