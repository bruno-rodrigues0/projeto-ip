import pygame
from random import randint

import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from components.statemachine import State
from components.object import SimulatedObject
from components.dialog_printer import DialogPrinter
from entities.collectable import Collectable
from entities.player import Player
from scenes.context import Context

MAX_VEL = 220


# Scene objects
COLLECTABLE = Collectable(
    assets.S_COLLECTABLE,
    const.WINDOW_CENTRE[0],
    const.WINDOW_CENTRE[1] - 25,
    "healing",
    5,
    assets.SFX_MASTER.audios["healing_item"]
)

offset = assets.S_ARENA.get_size()[1] // 2
ARENA_RECT = pygame.Rect(
    const.WINDOW_CENTRE[0] - offset,
    const.WINDOW_CENTRE[1] - offset + 80,
    assets.S_ARENA.height,
    assets.S_ARENA.height
)

ARENA_WALL01 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    ARENA_RECT.topleft[0],
    ARENA_RECT.topleft[1],
)
ARENA_WALL02 = SimulatedObject(
    assets.S_ARENA,
    ARENA_RECT.topleft[0],
    ARENA_RECT.topleft[1],
)
ARENA_WALL03 = SimulatedObject(
    assets.S_ARENA,
    ARENA_RECT.topright[0],
    ARENA_RECT.topright[1],
)
ARENA_WALL04 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    ARENA_RECT.bottomleft[0],
    ARENA_RECT.bottomleft[1] - 5,
)

ARENA = [ARENA_WALL01, ARENA_WALL02, ARENA_WALL03, ARENA_WALL04]

collectable_group = pygame.sprite.Group()
all_objects_group = pygame.sprite.Group()
arena_group = pygame.sprite.Group()


for wall in ARENA:
    arena_group.add(wall)
    all_objects_group.add(wall)


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
        PLAYER: Player,
    ) -> None:

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
            collectable_group.remove(item)
            self.has_collectable = False
            item.sound.play()
            if item.type == "healing":
                PLAYER.heal(item.buff)
                Context.collected_life_orbs += 1
            elif item.type == "defense":
                PLAYER.buff_defense(item.buff, 1)
                Context.collected_defense_orbs += 1

        PLAYER.update(dt)


        # WARN sistema de turno por tempo. mudar para attack.finished
        if (pygame.time.get_ticks() - self.initial_time) / 1000 >= 10:
            PLAYER.update_buffs() # reseta os buffs de turno
            Context.battle_state = "battle_menu"
            self.printer = DialogPrinter(const.BASE_DIALOGS[randint(0, len(const.BASE_DIALOGS) - 1)], 40, 30)
            return


        # Spawn chance of a collectable item (1 in 2000 per frame)
        # WARN mudar chance por tempo (quem tem +fps tem mais chance de pegar item assim)
        if 1 == randint(0, 2000) and not self.has_collectable:
            self.has_collectable = True

            types = ["healing", "defense"]
            COLLECTABLE.type = types[randint(0, 1)]

            assert COLLECTABLE.image is not None
            if COLLECTABLE.type == "healing":
                COLLECTABLE.image.fill(const.RED)
            else:
                COLLECTABLE.image.fill(const.CYAN)

            COLLECTABLE.x_ref = randint(ARENA_RECT.topleft[0] + 50, ARENA_RECT.topright[0] - 50)
            COLLECTABLE.y = const.WINDOW_CENTRE[1] - 30
            COLLECTABLE.update(dt)

            all_objects_group.add(COLLECTABLE)
            collectable_group.add(COLLECTABLE)

        # If have a collectable item in scene
        if self.has_collectable:
            COLLECTABLE.update(dt)

            if COLLECTABLE.y >= ARENA_RECT.bottomleft[1] - 5:
                self.has_collectable = False
                all_objects_group.remove(COLLECTABLE)
                collectable_group.remove(COLLECTABLE)


        surface.blit(PLAYER.image, PLAYER.get_pos())
        all_objects_group.draw(surface)

    def exit(self) -> None:
        pass
