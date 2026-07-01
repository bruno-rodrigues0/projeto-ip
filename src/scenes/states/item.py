import pygame
from random import randint

from components.statemachine import State
from components.dialog_printer import DialogConfig
import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from scenes.context import Context
from entities.player import Player


class ItemUsed(State):
    @staticmethod
    def enter(game) -> None:
        item = Context.item_used
        if not item:
            return

        # Efeito aplicado aqui, uma única vez na transição
        match item.type:
            case "healing":
                game.player.heal(item.buff)
            case "damage":
                game.player.buff_damage(item.buff, item.buff_count)
            case "defense":
                game.player.buff_defense(item.buff, item.buff_count)

        item.sound.play()
        game.printer.set_text(item.dialog)
        game.printer.set_config(DialogConfig.BATTLE)

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if not game.printer.page_finished:
            game.printer.update()
        else:
            if action_buffer[Action.A] == InputState.PRESSED:
                if Context.item_used in Context.items:
                    Context.items.remove(Context.item_used)
                Context.battle_state = "fight"
                return

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
        game.printer.draw(surface, assets.F_JERSEY10_MEDIUM, (const.WINDOW_CENTRE[0] - 270, 400))


class Item(State):
    """Menu de itens."""

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
        n = len(Context.items)

        if action_buffer[Action.UP] == InputState.PRESSED:
            assets.SFX_MASTER.audios["move_selection"].play()
            game.action_option = (game.action_option - 1) % n
        elif action_buffer[Action.DOWN] == InputState.PRESSED:
            assets.SFX_MASTER.audios["move_selection"].play()
            game.action_option = (game.action_option + 1) % n
        elif action_buffer[Action.RIGHT] == InputState.PRESSED:
            assets.SFX_MASTER.audios["move_selection"].play()
            game.action_option = (game.action_option + 2) % n
        elif action_buffer[Action.LEFT] == InputState.PRESSED:
            assets.SFX_MASTER.audios["move_selection"].play()
            game.action_option = (game.action_option - 2) % n

        if action_buffer[Action.A] == InputState.PRESSED:
            Context.item_used = Context.items[game.action_option]
            game.action_option = 0
            Context.battle_state = "item_used"
            return

        page = game.action_option // 6
        page_start = page * 6
        items_pos, items_options = [], []

        for i, item in enumerate(Context.items[page_start: page_start + 6]):
            pos = (const.WINDOW_CENTRE[0] - 240 + 150 * (i // 2), 400 + 50 * (i % 2))
            items_pos.append(pos)
            items_options.append(assets.F_JERSEY10_MEDIUM.render(item.name, True, const.WHITE))

        heart_pos = (
            const.WINDOW_CENTRE[0] - 280 + 150 * ((game.action_option % 6) // 2),
            410 + 50 * (game.action_option % 2),
        )

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)

        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        for pos, surf in zip(items_pos, items_options):
            surface.blit(surf, pos)

        surface.blit(assets.S_HEART, heart_pos)
