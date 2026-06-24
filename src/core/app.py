import pygame

import core.constants as const
import core.setup as setup
import core.assets as assets
import core.input as input

from components.config import Config
from components.statemachine import StateMachine
from scenes.menu import Menu
from utilities.filters import chromatic_distortion, create_crt_mask


def run() -> None:
    config = Config()
    pygame.display.set_caption(const.CAPTION)
    pygame.display.set_icon(assets.ICON)
    assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    scene_manager = StateMachine(Menu) # type: ignore
    crt_mask = create_crt_mask(const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
    game_loop(setup.window, setup.clock, scene_manager, crt_mask)


def game_loop(
    surface: pygame.Surface,
    clock: pygame.time.Clock,
    scene_manager: StateMachine,
    crt_mask: pygame.Surface
) -> None:
    action_buffer: input.InputBuffer = [
        input.InputState.NOTHING for _ in input.Action
    ]

    last_action_mapping_pressed:  list[pygame.key] = [ # type: ignore
        input.action_mappings[action][0] for action in input.Action
    ]

    print("Starting game loop")

    clock.tick()
    joysticks = {}

    while True:
        fps = Config().config["fps"]
        elapsed_time = clock.tick(fps)
        dt = elapsed_time / 1000.0  # Convert to seconds
        dt = min(dt, 0.05)

        running = input_event_queue()

        if not running:
            terminate(surface)

        update_action_buffer(action_buffer, last_action_mapping_pressed)


        for event in pygame.event.get():

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")


        scene_manager.execute(surface, dt, action_buffer)

        if Config().config["chromatic"]:
            filtered = chromatic_distortion(surface)

            if Config().config["crt"]:
                filtered.blit(crt_mask, (0, 0))

            surface.blit(filtered, (0, 0))
        elif Config().config["crt"]:
            surface.blit(crt_mask, (0, 0))


        debug_str = f"FPS {clock.get_fps():.0f}"
        debug_text = assets.F_JERSEY10_SMALL.render(debug_str, False, const.WHITE, const.BLACK)
        surface.blit(debug_text, (1, 1))

        # Keep these calls together in this order
        pygame.display.flip()


def input_event_queue() -> bool:
    '''
    Pumps the event queue and handle application events
    Return: False if should terminate, else True
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


def update_action_buffer(
    action_buffer: input.InputBuffer,
    last_action_mapping_pressed: list[pygame.key] # type: ignore
) -> None:
    keys_held = pygame.key.get_pressed()
    for action in input.Action:
        if (action_buffer[action] == input.InputState.NOTHING):
            # Verifica se qualquer tecla de ação foi pressionada
            for mapping in input.action_mappings[action]:
                if mapping == last_action_mapping_pressed[action]:
                    continue

                if keys_held[mapping]:
                    last_action_mapping_pressed[action] = mapping # type: ignore

        if keys_held[last_action_mapping_pressed[action]]: # type: ignore
            if (action_buffer[action] == input.InputState.NOTHING or
                    action_buffer[action] == input.InputState.RELEASED):
                action_buffer[action] = input.InputState.PRESSED
            elif action_buffer[action] == input.InputState.PRESSED:
                action_buffer[action] = input.InputState.HELD
        else:
            if (action_buffer[action] == input.InputState.PRESSED or
                    action_buffer[action] == input.InputState.HELD):
                action_buffer[action] = input.InputState.RELEASED
            elif action_buffer[action] == input.InputState.RELEASED:
                action_buffer[action] = input.InputState.NOTHING


def terminate(surface: pygame.Surface) -> None:
    print("Terminated application")

    pygame.mixer.stop()
    surface.fill(const.BLACK)

    pygame.quit()
    raise SystemExit
