
import pygame
from components.statemachine import State
import core.assets as assets
import core.constants as const

from core.input import InputBuffer, InputState, Action
from scenes import dialog
from scenes.context import Context


menu_options_group = pygame.sprite.Group()


class BattleMenu(State):
    """
    Shows battle menu.
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
            action_buffer[Action.LEFT] == InputState.PRESSED
        ):
            self.selected_option = (self.selected_option - 2) % 6
        elif (
            action_buffer[Action.RIGHT] == InputState.PRESSED
        ):
            self.selected_option = (self.selected_option + 2) % 6


        if not self.printer.finished:
            self.printer.update()


        heart_pos = (const.WINDOW_CENTRE[0] - 290 + 112 * self.selected_option, 615)

        pygame.draw.rect(
            surface,
            const.WHITE,
            (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)

        for i in range(0, 6, 2):
            if self.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        surface.blit(assets.S_HEART, heart_pos)

        self.printer.draw(surface, assets.F_JERSEY10_MEDIUM, (const.WINDOW_CENTRE[0] - 270, 400))

        if (
            action_buffer[Action.START] == InputState.PRESSED
        ):
            self.printer.reset()
            if self.selected_option == 0: # attack
                Context.battle_state = "attack"
                return
            elif self.selected_option == 2: # item
                if len(Context.items) > 0:
                    Context.battle_state = "item"
                else:
                    assets.SFX_NO_ITEMS.play()
                return
            else: # act
                Context.battle_state = "act"
                return

    def exit(self) -> None:
        pass
