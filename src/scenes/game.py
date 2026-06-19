import pygame

import core.constants as const
import core.assets as assets
import scenes.menu
import scenes.dialog

from core.input import InputBuffer, InputState, Action
from components.object import SimulatedObject
from entities.player import Player
from scenes.scene import Scene
from scenes.context import Context


MAX_VEL = 220


# Scene objects
PLAYER = Player(assets.S_HEART, const.WINDOW_CENTRE[0], const.WINDOW_CENTRE[1], 100)
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
    (const.WINDOW_HEIGHT // 2) - offset,
)
ARENA_WALL02 = SimulatedObject(
    assets.S_ARENA,
    (const.WINDOW_WIDTH // 2) - offset,
    (const.WINDOW_HEIGHT // 2) - offset,
)
ARENA_WALL03 = SimulatedObject(
    assets.S_ARENA,
    (const.WINDOW_WIDTH // 2) + assets.S_ARENA.get_size()[1] - offset,
    (const.WINDOW_HEIGHT // 2) - offset,
)
ARENA_WALL04 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    (const.WINDOW_WIDTH // 2) - offset,
    (const.WINDOW_HEIGHT // 2) + assets.S_ARENA.get_size()[1] - offset - 5,
)

ARENA = [ARENA_WALL01, ARENA_WALL02, ARENA_WALL03, ARENA_WALL04]
COLLECTABLES = [COLLECTABLE1, COLLECTABLE2, COLLECTABLE3]


collectable_group = pygame.sprite.Group()
all_objects_group = pygame.sprite.Group()
arena_group = pygame.sprite.Group()

all_objects_group.add(PLAYER)
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


class Game(Scene):
    """
    Main battle loop.
    """

    # NOTE essa cena atualmente contém atualmente apenas a arena de batalha. Posteriormente deve ser refatorada e
    # conter apenas o gerenciamento entre os turnos da batalha. A ser discutido.

    def enter(self) -> None:
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.unpause()

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:

        # Pause logic
        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            Context.last_scene = Game # type: ignore
            Context.paused = True
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore


        # NOTE Abre a cena de dialogo, apenas para teste.
        if (
            action_buffer[Action.B] == InputState.PRESSED
        ):
            Context.dialog_text = ["Olá, Mundo! bla bla bla bla bla"]
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


        # Collect items
        collected = pygame.sprite.spritecollide(PLAYER, collectable_group, True)

        for item in collected:
            all_objects_group.remove(item)
            Context.collected_coins += 1
            PLAYER.take_damage(10)
            
        PLAYER.update(dt)            


        # Display player's HP
        hp_text = assets.F_JERSEY10.render("HP", True, const.WHITE)
        hp_initial_pos = (
            const.WINDOW_CENTRE[0] - (hp_text.get_size()[0] + 10 + 150 + 77) // 2,
            const.WINDOW_CENTRE[1] + 150,
        )

        hp_yellow_bar_rect = pygame.draw.rect(
            surface,
            const.YELLOW,
            (
                hp_initial_pos[0] + hp_text.get_size()[0] + 10,
                hp_initial_pos[1],
                150 * PLAYER.hp_percent,
                30,
            ),
        )
        hp_red_bar_rect = pygame.draw.rect(
            surface,
            const.RED,
            (
                hp_yellow_bar_rect.right,
                hp_yellow_bar_rect.y,
                150 * (1 - PLAYER.hp_percent),
                30,
            ),
        )

        hp_values_text = assets.F_JERSEY10.render(
            f"{str(PLAYER.current_hp).rjust(3)} / {PLAYER.max_hp}", True, const.WHITE
        )

        # Draw
        surface.fill(const.BLACK)
        all_objects_group.draw(surface)
        surface.blit(hp_text, hp_initial_pos)
        surface.blit(
            hp_values_text, (hp_red_bar_rect.right + 10, hp_red_bar_rect.y)
        )
        coins_text = assets.F_JERSEY10.render(
            f"COINS: {Context.collected_coins}", True, const.YELLOW
        )
        surface.blit(coins_text, (820, 0))

    def exit(self) -> None:
        pygame.mixer.music.pause()
