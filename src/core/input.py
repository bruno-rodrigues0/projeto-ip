import pygame
from enum import IntEnum, auto


class InputState(IntEnum):
    NOTHING = 0
    PRESSED = auto()
    HELD = auto()
    RELEASED = auto()


class MouseButton(IntEnum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class Action(IntEnum):
    LEFT = 0
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    A = auto()
    B = auto()
    X = auto()
    Y = auto()
    SELECT = auto()
    START = auto()
    OPTIONS = auto()


action_mappings = {
    Action.LEFT: [pygame.K_a, pygame.K_LEFT],
    Action.RIGHT: [pygame.K_d, pygame.K_RIGHT],
    Action.UP: [pygame.K_w, pygame.K_UP],
    Action.DOWN: [pygame.K_s, pygame.K_DOWN],
    Action.A: [pygame.K_z, pygame.K_RETURN],
    Action.B: [pygame.K_x],
    Action.X: [pygame.K_c],
    Action.Y: [pygame.K_v],
    Action.SELECT: [],
    Action.START: [],
    Action.OPTIONS: [pygame.K_ESCAPE]
}


InputBuffer = list[InputState]
