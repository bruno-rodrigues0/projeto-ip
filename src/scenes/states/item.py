import pygame
import math
from components.statemachine import State
import core.assets as assets
import core.constants as const

from core.input import InputBuffer, InputState, Action
from scenes.context import Context


menu_options_group = pygame.sprite.Group()

class ItemUsed(State):
    @staticmethod
    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:

        if not self.printer.finished:
            self.printer.update()
        else:
            if (
                action_buffer[Action.START] == InputState.PRESSED
            ):
                Context.battle_state = "fight"
                return

        pygame.draw.rect(
            surface,
            const.WHITE,
            (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if self.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        self.printer.draw(surface, assets.F_JERSEY10_MEDIUM, (const.WINDOW_CENTRE[0] - 270, 400))


class Item(State):
    """
    Item menu.
    """

    def enter(self) -> None:
        pass

    @staticmethod
    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:

        if (
            action_buffer[Action.UP] == InputState.PRESSED
        ):
            self.action_option = (self.action_option - 1) % len(Context.items)
        elif (
            action_buffer[Action.DOWN] == InputState.PRESSED
        ):
            self.action_option = (self.action_option + 1) % len(Context.items)
        elif (
            action_buffer[Action.RIGHT] == InputState.PRESSED
        ):
            self.action_option = (self.action_option + 2) % len(Context.items)
        elif (
            action_buffer[Action.LEFT] == InputState.PRESSED
        ):
            self.action_option = (self.action_option - 2) % len(Context.items)


        if (
            action_buffer[Action.START] == InputState.PRESSED
        ):
            self.action_option = 0
            Context.item_used = "Pie"
            Context.battle_state = "item_used"
            return

        items_pos = []
        items_options = []
        page = self.action_option // 6
        page_start = page * 6

        for i, item in enumerate(Context.items[page_start: page_start + 6]):
            pos = (const.WINDOW_CENTRE[0] - 240 + 150 * (i // 2), 400 + 50 * (i % 2))
            option = assets.F_JERSEY10_MEDIUM.render(
                item,
                True,
                const.WHITE
            )

            items_pos.append(pos)
            items_options.append(option)


        heart_pos = (
            const.WINDOW_CENTRE[0] - 280 + 150 * ((self.action_option % 6) // 2),
            410 + 50 * ((self.action_option) % 2)
        )

        pygame.draw.rect(
            surface,
            const.WHITE,
            (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)

        for i in range(0, 6, 2):
            if self.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        for (pos, item) in zip(items_pos, items_options):
            surface.blit(item, pos)

        surface.blit(assets.S_HEART, heart_pos)

    def exit(self) -> None:
        pass
