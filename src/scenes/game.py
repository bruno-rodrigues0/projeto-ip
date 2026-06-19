import pygame

import core.constants as const
import core.assets as assets
import scenes.menu
import scenes.dialog

from core.input import InputBuffer, InputState, Action
from entities.player import Player
from scenes.scene import Scene
from scenes.context import Context
from scenes.states.battle_menu import BattleMenu
from scenes.states.fight import Fight


MAX_VEL = 220


# Scene objects
PLAYER = Player(assets.S_HEART, const.WINDOW_CENTRE[0], const.WINDOW_CENTRE[1], 100)

class Game(Scene):
    """
    Main battle loop.
    """

    def enter(self) -> None:
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.unpause()
        self.selected_option = 0

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


        # Draw
        surface.fill(const.BLACK)

        # Display player's HP
        hp_text = assets.F_JERSEY10.render("HP", True, const.WHITE)
        hp_initial_pos = (
            const.WINDOW_CENTRE[0] - (hp_text.get_size()[0] + 10 + 150 + 77) // 2,
            const.WINDOW_CENTRE[1] + 210,
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

        if Context.battle_state == "battle_menu":
            BattleMenu.execute(self, surface, dt, action_buffer)
        elif Context.battle_state == "fight":
            Fight.execute(self, surface, dt, action_buffer, PLAYER)
        surface.blit(hp_text, hp_initial_pos)
        surface.blit(
            hp_values_text, (hp_red_bar_rect.right + 10, hp_red_bar_rect.y)
        )

        if Context.battle_state != "battle_menu":
            for i in range(0, 6, 2):
                surface.blit(assets.S_MENU_OPTIONS[i], (340 + 100 * i, 600))

    def exit(self) -> None:
        pygame.mixer.music.pause()
