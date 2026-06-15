import pygame

import scenes.menu
import core.constants as const
import core.assets as asset

from core.input import InputBuffer, InputState, Action
from components.object import SimulatedObject
from scenes import scene
from scenes.scene import Scene

MAX_X = const.WINDOW_WIDTH - asset.PLAYER_SPRITE.get_width()
MAX_Y = const.WINDOW_HEIGHT - asset.PLAYER_SPRITE.get_height()
MAX_VEL = 200

PLAYER = SimulatedObject(asset.PLAYER_SPRITE, 400, 300)
OBSTACLE = SimulatedObject(asset.COIN_SPRITE, 700, 200)
COLLECTABLE = SimulatedObject(asset.COIN_SPRITE, 100, 400)

collectable_group = pygame.sprite.Group()
all_objects_group = pygame.sprite.Group()

collectable_group.add(COLLECTABLE)
all_objects_group.add(PLAYER)
all_objects_group.add(OBSTACLE)
all_objects_group.add(COLLECTABLE)

class PredRect:
    rect: pygame.rect.Rect

    def __init__(self, rect):
        self.rect = rect

class Game(Scene):
    def enter(self) -> None:
        pygame.mixer.music.play(-1)

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:

        # Go to menu
        if (action_buffer[Action.A] == InputState.PRESSED):
            self.statemachine.change_state(scenes.menu.Menu)

        # Move in X axis
        if (
            action_buffer[Action.RIGHT] == InputState.HELD
            and action_buffer[Action.LEFT] == InputState.NOTHING
        ):
            PLAYER.vx = MAX_VEL
        elif (
            action_buffer[Action.LEFT] == InputState.HELD
            and action_buffer[Action.RIGHT] == InputState.NOTHING
        ):
            PLAYER.vx = -MAX_VEL
        else:
            PLAYER.vx = 0

        next_pos = PLAYER.get_next_pos(dt)
        pred_rect = PredRect(PLAYER.image.get_rect(topleft=(next_pos[0], next_pos[1])))
        collided = pygame.sprite.collide_rect(pred_rect, OBSTACLE)
        if collided:
            PLAYER.vx = 0

        # Move in Y axis
        if (
            action_buffer[Action.UP] == InputState.HELD
            and action_buffer[Action.DOWN] == InputState.NOTHING
        ):
            PLAYER.vy = -MAX_VEL
        elif (
            action_buffer[Action.DOWN] == InputState.HELD
            and action_buffer[Action.UP] == InputState.NOTHING
        ):
            PLAYER.vy = MAX_VEL
        else:
            PLAYER.vy = 0

        next_pos = PLAYER.get_next_pos(dt)
        pred_rect = PredRect(PLAYER.image.get_rect(topleft=(next_pos[0], next_pos[1])))
        collided = pygame.sprite.collide_rect(pred_rect, OBSTACLE)
        if collided:
            PLAYER.vy = 0

        # Collect "coin"

        nex_pos  = PLAYER.get_next_pos(dt)
        pred_rect = PredRect(PLAYER.image.get_rect(topleft=(next_pos[0], next_pos[1])))

        collected = pygame.sprite.spritecollide(PLAYER, collectable_group, True)

        for item in collected:
            all_objects_group.remove(item)

        PLAYER.update(dt)
        surface.fill(const.MAGENTA)
        all_objects_group.draw(surface)

    def exit(self) -> None:
        pygame.mixer.music.stop()
