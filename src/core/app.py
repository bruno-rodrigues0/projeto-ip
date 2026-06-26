from posix import stat

import pygame
import time

import core.constants as const
import core.setup as setup
import core.assets as assets
import core.input as input

from core.joystick import xbox_action_mapping, ps4_action_mapping, STICK_DEADZONE
from components.config import Config
from components.statistics import Statistics
from components.statemachine import StateMachine
from scenes.context import Context
from scenes.menu import Menu
from utilities.filters import chromatic_distortion, create_crt_mask


def run() -> None:
    config = Config()
    statistics = Statistics()
    print(statistics.data)
    pygame.display.set_caption(const.CAPTION)
    pygame.display.set_icon(assets.ICON)
    assets.SFX_MASTER.set_master_volume(config.data["master_volume"])
    assets.SFX_MASTER.set_music_volume(config.data["music_volume"])
    assets.SFX_MASTER.set_effect_volume(config.data["effect_volume"])
    assets.SFX_MASTER.update_volume()
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
    initial_time = time.time()
    action_buffer: input.InputBuffer = [
        input.InputState.NOTHING for _ in input.Action
    ]

    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        joysticks.append(joy)

    print("Starting game loop")

    clock.tick()

    while True:
        config = Config()
        fps = config.data["fps"]
        elapsed_time = clock.tick(fps)
        dt = elapsed_time / 1000.0  # Convert to seconds
        dt = min(dt, 0.05)

        running = input_event_queue()

        if not running:
            terminate(surface, initial_time)

        update_action_buffer(action_buffer, joysticks)

        scene_manager.execute(surface, dt, action_buffer)

        if config.data["chromatic"]:
            filtered = chromatic_distortion(surface)

            if config.data["crt"]:
                filtered.blit(crt_mask, (0, 0))

            surface.blit(filtered, (0, 0))
        elif config.data["crt"]:
            surface.blit(crt_mask, (0, 0))


        debug_str = f"FPS {clock.get_fps():.0f}"
        debug_text = assets.F_JERSEY10_SMALL.render(debug_str, False, const.WHITE, const.BLACK)
        surface.blit(debug_text, (1, 1))


        pygame.time.wait(1) # libera a CPU
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
    joysticks: list[pygame.joystick.Joystick] # type: ignore
) -> None:
    keys_held = pygame.key.get_pressed()

    for action in input.Action:
        action_active = any(keys_held[key] for key in input.action_mappings[action])

        if not action_active:
            for joy in joysticks:
                if (
                    "xbox" in joy.get_name().lower()
                    or "sony interactive" == joy.get_name().lower()
                ):
                    # Xbox and PS5 controller buttons
                    for button_id in xbox_action_mapping[action]:
                        if joy.get_button(button_id):
                            action_active = True
                            break

                    # Xbox and PS5 controller hat
                    if not action_active:
                        hat_x, hat_y = joy.get_hat(0)

                        if action == input.Action.LEFT and hat_x == -1:
                            action_active = True
                        elif action == input.Action.RIGHT and hat_x == 1:
                            action_active = True
                        elif action == input.Action.UP and hat_y == 1:
                            action_active = True
                        elif action == input.Action.DOWN and hat_y == -1:
                            action_active = True

                elif (
                    "wireless controller" == joy.get_name().lower()
                    or "ps4 controller" in joy.get_name().lower()
                ):
                    # PS4 controller buttons and dpad
                    for button_id in ps4_action_mapping[action]:
                        if joy.get_button(button_id):
                            action_active = True
                            break

                if not action_active:
                    if joy and joy.get_numaxes() >= 2:
                        raw_x = joy.get_axis(0)
                        raw_y = joy.get_axis(1)
                        axis_x = raw_x if abs(raw_x) > STICK_DEADZONE else 0.0
                        axis_y = raw_y if abs(raw_y) > STICK_DEADZONE else 0.0

                        if action == input.Action.LEFT and axis_x < 0:
                            action_active = True
                        elif action == input.Action.RIGHT and axis_x > 0:
                            action_active = True
                        elif action == input.Action.UP and axis_y < 0:
                            action_active = True
                        elif action == input.Action.DOWN and axis_y > 0:
                            action_active = True

                if action_active:
                    break

        if action_active:
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


def terminate(surface: pygame.Surface, initial_time: float) -> None:
    print("Terminated application")

    statistics = Statistics()

    pygame.mixer.stop()
    surface.fill(const.BLACK)
    game_time = time.time() - initial_time

    statistics.data["game_time"] += int(game_time)
    statistics.data["deaths"] += Context.deaths
    statistics.save_file()
    print(statistics.data) # colocar na tela final

    pygame.quit()
    raise SystemExit
