import pygame

import core.constants as const
import core.input as input
import core.assets as assets

from scenes.context import Context
from scenes.scene import Scene
import scenes.intro


S_MENU = assets.S_MENU
S_MENU_X = const.WINDOW_CENTRE[0] - S_MENU.get_width() // 2
S_MENU_Y = const.WINDOW_CENTRE[1] - S_MENU.get_height() // 2


class Menu(Scene):
    """
    Main/pause menu scene.
    """

    def enter(self) -> None:
        self.selected_option = 'play'

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: input.InputBuffer,
    ) -> None:
        if (action_buffer[input.Action.DOWN] == input.InputState.PRESSED):
            self.selected_option = 'quit'
        if (action_buffer[input.Action.UP] == input.InputState.PRESSED):
            self.selected_option = 'play' 

        if (action_buffer[input.Action.START] == input.InputState.PRESSED):
            if self.selected_option == 'play':
                # If paused, back to last_scene, else go to Intro scene
                if Context.paused:
                    self.statemachine.change_state(Context.last_scene)
                else:
                    Context.paused = False
                    self.statemachine.change_state(scenes.intro.Intro) # type: ignore
                return
            else:
                pygame.quit()
                raise SystemExit

        surface.fill(const.BLACK)
        surface.blit(S_MENU, (S_MENU_X, S_MENU_Y))

        # If in pause menu or main menu
        play_option_value = "COMEÇAR" if not Context.paused else "CONTINUAR"
        play_option_pos = (const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size(play_option_value)[0] // 2, S_MENU_Y + 400)
        quit_option_pos = (const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size("SAIR DO JOGO")[0] // 2, play_option_pos[1] + 50)

        if self.selected_option == 'play':
            play_option_color = const.YELLOW
            quit_option_color = const.ORANGE
            heart_pos = (play_option_pos[0] - 60, play_option_pos[1])
        else:
            play_option_color = const.ORANGE
            quit_option_color = const.YELLOW
            heart_pos = (quit_option_pos[0] - 60, quit_option_pos[1])

        play_option = assets.F_JERSEY10_MEDIUM.render(play_option_value, True, play_option_color)
        quit_option = assets.F_JERSEY10_MEDIUM.render("SAIR DO JOGO", True, quit_option_color)

        surface.blit(play_option, play_option_pos)
        surface.blit(quit_option, quit_option_pos)

        surface.blit(assets.S_HEART, heart_pos)


    def exit(self) -> None:
        pass
