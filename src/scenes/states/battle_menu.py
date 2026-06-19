
import pygame
from components.statemachine import State
import core.assets as assets
import core.constants as const

from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from scenes.context import Context


menu_options_group = pygame.sprite.Group()


class BattleMenu(State):
    """
    Shows battle menu.
    """

    def enter(self) -> None:
        pass

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

        if (
            action_buffer[Action.START] == InputState.PRESSED
        ):  
            if self.selected_option == 0: # fight
                Context.battle_state = "fight"
                return
            elif self.selected_option == 2: # item
                pass
            else: # act
                pass


        heart_pos = (350 + 100 * self.selected_option, 615)
        pygame.draw.rect(
            surface, 
            const.WHITE,
            (const.WINDOW_CENTRE[0] - 300, 280, 600, 250), 5)
        for i in range(0, 6, 2):
            if self.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (340 + 100 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (340 + 100 * i, 600))
        surface.blit(assets.S_HEART, heart_pos)

    def exit(self) -> None:
        pass
