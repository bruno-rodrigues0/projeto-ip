import pygame
from components.statemachine import State
import core.assets as assets
import core.constants as const

from core.input import InputBuffer, InputState, Action
from scenes.context import Context


menu_options_group = pygame.sprite.Group()


class Attack(State):
    """
    Attack.
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
        surface.blit(assets.S_ATTACK_BAR, (const.WINDOW_CENTRE[0] - 273, 400))

    def exit(self) -> None:
        pass
