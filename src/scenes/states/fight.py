import pygame
import core.assets as assets
import core.constants as const

from components.statemachine import State
from core.input import InputBuffer, InputState, Action
from components.object import SimulatedObject
from entities.player import Player
from scenes.context import Context


MAX_VEL = 220

# Scene objects
COLLECTABLE1 = SimulatedObject(
    assets.S_COIN, const.WINDOW_CENTRE[0] + 110, const.WINDOW_CENTRE[1] + 90
)
COLLECTABLE2 = SimulatedObject(
    assets.S_COIN, const.WINDOW_CENTRE[0] - 60, const.WINDOW_CENTRE[1] - 90
)
COLLECTABLE3 = SimulatedObject(
    assets.S_COIN, const.WINDOW_CENTRE[0] - 45, const.WINDOW_CENTRE[1] + 50
)

offset = assets.S_ARENA.get_size()[1] // 2
ARENA_WALL01 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    (const.WINDOW_WIDTH // 2) - offset,
    (const.WINDOW_HEIGHT // 2) - offset + 60,
)
ARENA_WALL02 = SimulatedObject(
    assets.S_ARENA,
    (const.WINDOW_WIDTH // 2) - offset,
    (const.WINDOW_HEIGHT // 2) - offset + 60,
)
ARENA_WALL03 = SimulatedObject(
    assets.S_ARENA,
    (const.WINDOW_WIDTH // 2) + assets.S_ARENA.get_size()[1] - offset,
    (const.WINDOW_HEIGHT // 2) - offset + 60,
)
ARENA_WALL04 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    (const.WINDOW_WIDTH // 2) - offset,
    (const.WINDOW_HEIGHT // 2) + assets.S_ARENA.get_size()[1] - offset - 5 + 60,
)

ARENA = [ARENA_WALL01, ARENA_WALL02, ARENA_WALL03, ARENA_WALL04]
COLLECTABLES = [COLLECTABLE1, COLLECTABLE2, COLLECTABLE3]

collectable_group = pygame.sprite.Group()
all_objects_group = pygame.sprite.Group()
arena_group = pygame.sprite.Group()

# all_objects_group.add(PLAYER)
for wall in ARENA:
    arena_group.add(wall)
    all_objects_group.add(wall)
for collectable in COLLECTABLES:
    collectable_group.add(collectable)
    all_objects_group.add(collectable)


class PredRect:
    """
    Player movement prediction rect.
    """

    def __init__(self, rect):
        self.rect = rect

class Fight(State):
    def enter(self) -> None:
        pass

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
        PLAYER: Player
    ) -> None:
        if (
            action_buffer[Action.B] == InputState.PRESSED
        ):
            Context.battle_state = "battle_menu"
            return

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


        # Collect items
        collected = pygame.sprite.spritecollide(PLAYER, collectable_group, True)

        for item in collected:
            all_objects_group.remove(item)
            Context.collected_coins += 1
            PLAYER.take_damage(40)

        PLAYER.update(dt)

        if len(collected) >= 1:
            Context.battle_state = "battle_menu"
            return

        surface.blit(PLAYER.image, PLAYER.get_pos())
        all_objects_group.draw(surface)

    def exit(self) -> None:
        pass
