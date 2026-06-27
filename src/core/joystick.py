import pygame

from core.input import Action

STICK_DEADZONE = 0.3
xbox_action_mapping = {
    Action.LEFT: [], # Left empty to assign to stick and hat
    Action.RIGHT: [],
    Action.UP: [],
    Action.DOWN: [],
    Action.A: [pygame.CONTROLLER_BUTTON_A],
    Action.B: [pygame.CONTROLLER_BUTTON_B],
    Action.X: [pygame.CONTROLLER_BUTTON_X],
    Action.Y: [pygame.CONTROLLER_BUTTON_Y],
    Action.SELECT: [],
    Action.START: [7],
    Action.OPTIONS: [6]
}

ps4_action_mapping = {
    Action.LEFT: [pygame.CONTROLLER_BUTTON_DPAD_LEFT],
    Action.RIGHT: [pygame.CONTROLLER_BUTTON_DPAD_RIGHT],
    Action.UP: [pygame.CONTROLLER_BUTTON_DPAD_UP],
    Action.DOWN: [pygame.CONTROLLER_BUTTON_DPAD_DOWN],
    Action.A: [pygame.CONTROLLER_BUTTON_A],
    Action.B: [pygame.CONTROLLER_BUTTON_B],
    Action.X: [pygame.CONTROLLER_BUTTON_X],
    Action.Y: [pygame.CONTROLLER_BUTTON_Y],
    Action.SELECT: [],
    Action.START: [],
    Action.OPTIONS: [6]
}

