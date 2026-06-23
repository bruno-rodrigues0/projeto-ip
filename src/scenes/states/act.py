import pygame
from components.statemachine import State
import core.assets as assets
import core.constants as const

from core.input import InputBuffer, InputState, Action
from scenes.context import Context


menu_options_group = pygame.sprite.Group()

class Check(State):
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
                self.initial_time = pygame.time.get_ticks()
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


class Act(State):
    """
    Act.
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
            self.action_option = (self.action_option - 1) % 2
        elif (
            action_buffer[Action.DOWN] == InputState.PRESSED
        ):
            self.action_option = (self.action_option + 1) % 2

        if (
            action_buffer[Action.START] == InputState.PRESSED
        ):
            if self.action_option == 0: # check
                Context.battle_state = "check"
                return
            else: # Talk
                Context.battle_state = "fight"
                return


        check_pos = (const.WINDOW_CENTRE[0] - 240, 400)
        check_option = assets.F_JERSEY10_MEDIUM.render(
            "Check",
            True,
            const.WHITE
        )

        talk_pos = (const.WINDOW_CENTRE[0] - 240, 400 + 50)
        talk_option = assets.F_JERSEY10_MEDIUM.render(
            "Talk",
            True,
            const.WHITE
        )


        heart_pos = (const.WINDOW_CENTRE[0] - 280, 410 + 50 * self.action_option)
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
        surface.blit(talk_option, talk_pos)
        surface.blit(check_option, check_pos)

    def exit(self) -> None:
        pass
