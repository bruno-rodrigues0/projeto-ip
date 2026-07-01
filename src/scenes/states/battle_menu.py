import pygame
from components.dialog_printer import DialogConfig
from components.statemachine import State
import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from scenes.context import Context
from random import randint


class BattleMenu(State):
    """
    Mostra o menu principal de batalha.
    """

    @staticmethod
    def enter(game) -> None:
        game.printer.set_text(
            game.lang_dialog["fight_menu"][randint(0, len(game.lang_dialog["fight_menu"]) - 1)]
        )
        game.printer.set_config(DialogConfig.BATTLE)

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:

        if action_buffer[Action.LEFT] == InputState.PRESSED:
            game.selected_option = (game.selected_option - 2) % 6
            assets.SFX_MASTER.audios["move_selection"].play()
        elif action_buffer[Action.RIGHT] == InputState.PRESSED:
            game.selected_option = (game.selected_option + 2) % 6
            assets.SFX_MASTER.audios["move_selection"].play()

        if not game.printer.page_finished:
            game.printer.update()

        heart_pos = (const.WINDOW_CENTRE[0] - 290 + 112 * game.selected_option, 615)

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        surface.blit(assets.S_HEART, heart_pos)
        game.printer.draw(surface, assets.F_JERSEY10_MEDIUM, (const.WINDOW_CENTRE[0] - 270, 400))

        if action_buffer[Action.A] == InputState.PRESSED:
            assets.SFX_MASTER.audios["select_option"].play()
            if game.selected_option == 0:
                Context.battle_state = "attack"
            elif game.selected_option == 2:
                if len(Context.items) > 0:
                    Context.battle_state = "item"
                else:
                    assets.SFX_MASTER.audios["no_items"].play()
            else:
                Context.battle_state = "act"
