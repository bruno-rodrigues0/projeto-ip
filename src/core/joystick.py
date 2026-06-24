import pygame

from core.input import Action

STICK_DEADZONE = 0.3
xbox_action_mapping = {
    Action.LEFT: [], # Left empty to assign to stick and hat
    Action.RIGHT: [],
    Action.UP: [],
    Action.DOWN: [],
    Action.A: [],
    Action.B: [],
    Action.SELECT: [],
    Action.START: [pygame.CONTROLLER_BUTTON_A],
    Action.OPTIONS: [pygame.CONTROLLER_BUTTON_B]
}

ps4_action_mapping = {
    Action.LEFT: [pygame.CONTROLLER_BUTTON_DPAD_LEFT],
    Action.RIGHT: [pygame.CONTROLLER_BUTTON_DPAD_RIGHT],
    Action.UP: [pygame.CONTROLLER_BUTTON_DPAD_UP],
    Action.DOWN: [pygame.CONTROLLER_BUTTON_DPAD_DOWN],
    Action.A: [],
    Action.B: [],
    Action.SELECT: [],
    Action.START: [pygame.CONTROLLER_BUTTON_A],
    Action.OPTIONS: [pygame.CONTROLLER_BUTTON_B]
}

