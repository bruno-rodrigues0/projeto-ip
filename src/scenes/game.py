import pygame

import core.constants as const
import core.assets as asset
import scenes.pause
import scenes.dialog

from core.input import InputBuffer, InputState, Action
from components.object import SimulatedObject
from scenes.scene import Scene
from scenes.context import Context

MAX_X = const.WINDOW_WIDTH - asset.HEART_SPRITE.get_width()
MAX_Y = const.WINDOW_HEIGHT - asset.HEART_SPRITE.get_height()
MAX_VEL = 220

PLAYER = SimulatedObject(asset.HEART_SPRITE, const.WINDOW_CENTRE[0], const.WINDOW_CENTRE[1])
COLLECTABLE = SimulatedObject(asset.COIN_SPRITE, const.WINDOW_CENTRE[0] + 110, const.WINDOW_CENTRE[1] + 90)
COLLECTABLE2 = SimulatedObject(asset.COIN_SPRITE, const.WINDOW_CENTRE[0] - 60, const.WINDOW_CENTRE[1] - 90)

offset = asset.ARENA_SPRITE.get_size()[1] // 2
ARENA_WALL01= SimulatedObject(pygame.transform.rotate(asset.ARENA_SPRITE, 90), (const.WINDOW_WIDTH // 2) - offset, (const.WINDOW_HEIGHT // 2) - offset)
ARENA_WALL02= SimulatedObject(asset.ARENA_SPRITE, (const.WINDOW_WIDTH // 2) - offset, (const.WINDOW_HEIGHT // 2) - offset)
ARENA_WALL03= SimulatedObject(asset.ARENA_SPRITE, (const.WINDOW_WIDTH // 2) + asset.ARENA_SPRITE.get_size()[1] - offset, (const.WINDOW_HEIGHT // 2) - offset)
ARENA_WALL04= SimulatedObject(pygame.transform.rotate(asset.ARENA_SPRITE, 90), (const.WINDOW_WIDTH // 2) - offset, (const.WINDOW_HEIGHT // 2) + asset.ARENA_SPRITE.get_size()[1] - offset - 5)


ARENA = [ARENA_WALL01, ARENA_WALL02, ARENA_WALL03, ARENA_WALL04]

collectable_group = pygame.sprite.Group()
all_objects_group = pygame.sprite.Group()
arena_group= pygame.sprite.Group()

collectable_group.add(COLLECTABLE)
collectable_group.add(COLLECTABLE2)
all_objects_group.add(PLAYER)
all_objects_group.add(COLLECTABLE)
all_objects_group.add(COLLECTABLE2)
for wall in ARENA:
    arena_group.add(wall)
    all_objects_group.add(wall)

class PredRect:
    rect: pygame.rect.Rect

    def __init__(self, rect):
        self.rect = rect

class Game(Scene):
    def enter(self) -> None:
        pygame.mixer.music.unpause()

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            Context.last_scene = Game # type: ignore
            self.statemachine.change_state(scenes.pause.Pause) # type: ignore

        if (
            action_buffer[Action.B] == InputState.PRESSED
        ):
            Context.dialog_text = "Olá, Mundo! bla bla bla bla bla"
            self.statemachine.change_state(scenes.dialog.Dialog) # type: ignore

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
        assert PLAYER.image is not None
        pred_rect = PredRect(PLAYER.image.get_rect(topleft=(next_pos[0], next_pos[1])))
        collided = pygame.sprite.spritecollide(pred_rect, arena_group, False)
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
        collided = pygame.sprite.spritecollide(pred_rect, arena_group, False)
        if collided:
            PLAYER.vy = 0

        # Collect "coin"
        collected = pygame.sprite.spritecollide(PLAYER, collectable_group, True)

        for item in collected:
            all_objects_group.remove(item)
            Context.collected_coins += 1

        PLAYER.update(dt)
        surface.fill(const.BLACK)
        coins_text = asset.DEBUG_FONT.render(f"COINS: {Context.collected_coins}", True, const.YELLOW)
        surface.blit(coins_text, (820, 0))
        all_objects_group.draw(surface)

    def exit(self) -> None:
        pygame.mixer.music.pause()
