from random import randint

import pygame
from components.statemachine import State
from components.dialog_printer import DialogConfig
import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from scenes.context import Context


class Check(State):
    @staticmethod
    def enter(game) -> None:
        game.printer.set_text(game.lang_dialog["check"])
        game.printer.set_config(DialogConfig.BATTLE)

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if not game.printer.page_finished:
            if action_buffer[Action.START] == InputState.PRESSED:
                game.printer.advance()
                assets.SFX_MASTER.audios["talking_long"].stop()
            else:
                game.printer.update()
        else:
            if action_buffer[Action.START] == InputState.PRESSED:
                game.initial_time = pygame.time.get_ticks()
                Context.battle_state = "fight"
                return

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
        game.printer.draw(surface, assets.F_JERSEY10_MEDIUM, (const.WINDOW_CENTRE[0] - 270, 400))


class Talk(State):
    @staticmethod
    def enter(game) -> None:
        assets.SFX_MASTER.audios["talking_long"].play(-1)
        game.printer.set_text(
            game.lang_dialog["talk"][randint(0, len(game.lang_dialog["talk"]) - 1)]
        )
        game.printer.set_config(DialogConfig.TALK_BOX)

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if not game.printer.page_finished:
            if action_buffer[Action.START] == InputState.PRESSED:
                game.printer.advance()
                assets.SFX_MASTER.audios["talking_long"].stop()
            else:
                game.printer.update()
        else:
            assets.SFX_MASTER.audios["talking_long"].stop()
            if action_buffer[Action.START] == InputState.PRESSED:
                game.initial_time = pygame.time.get_ticks()
                Context.battle_state = "fight"
                return

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        surface.blit(assets.S_TALK_BOX, (const.WINDOW_CENTRE[0] + 100, 100))
        game.printer.draw(surface, assets.F_JERSEY10_SMALL, (const.WINDOW_CENTRE[0] + 130, 110))


class Act(State):
    """Act — sub-menu com Check e Talk."""

    @staticmethod
    def enter(game) -> None:
        pass

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if action_buffer[Action.UP] == InputState.PRESSED:
            game.action_option = (game.action_option - 1) % 2
        elif action_buffer[Action.DOWN] == InputState.PRESSED:
            game.action_option = (game.action_option + 1) % 2

        if action_buffer[Action.START] == InputState.PRESSED:
            if game.action_option == 0:
                Context.battle_state = "check"
            else:
                Context.battle_state = "talk"
            return

        check_pos = (const.WINDOW_CENTRE[0] - 240, 400)
        check_text = assets.F_JERSEY10_MEDIUM.render(game.lang_inter["fight_menu"]["check"], True, const.WHITE)
        talk_pos = (const.WINDOW_CENTRE[0] - 240, 450)
        talk_text = assets.F_JERSEY10_MEDIUM.render(game.lang_inter["fight_menu"]["talk"],  True, const.WHITE)
        heart_pos = (const.WINDOW_CENTRE[0] - 280, 410 + 50 * game.action_option)

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        surface.blit(assets.S_HEART, heart_pos)
        surface.blit(talk_text, talk_pos)
        surface.blit(check_text, check_pos)
