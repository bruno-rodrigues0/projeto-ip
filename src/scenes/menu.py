import pygame

import core.constants as const
import core.input as input
import core.assets as assets

from scenes.context import Context
from scenes.scene import Scene
import scenes.intro


class Menu(Scene):
    """
    Main/pause menu scene.
    """

    def enter(self) -> None:
        self.selected_option = "play"

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: input.InputBuffer,
    ) -> None:
        if action_buffer[input.Action.DOWN] == input.InputState.PRESSED:
            if self.selected_option == "play":
                assets.SFX_MOVE_SELECTION.play()
            self.selected_option = "quit"
        if action_buffer[input.Action.UP] == input.InputState.PRESSED:
            if self.selected_option == "quit":
                assets.SFX_MOVE_SELECTION.play()
            self.selected_option = "play"

        if action_buffer[input.Action.START] == input.InputState.PRESSED:
            assets.SFX_SELECT_OPTION.play()
            if self.selected_option == "play":
                # If paused, back to last_scene, else go to Intro scene
                if Context.paused:
                    self.statemachine.change_state(Context.last_scene)
                else:
                    Context.paused = False
                    self.statemachine.change_state(scenes.intro.Intro)  # type: ignore
                return
            else:
                pygame.quit()
                raise SystemExit

        surface.fill(const.BLACK)

        # Draw the title
        title1_text = assets.F_JERSEY10_LARGE.render("Ayuwoke Time", True, const.WHITE)
        title1_text_pos = (
            const.WINDOW_CENTRE[0] - (title1_text.get_width() // 2),
            50,
        )
        surface.blit(title1_text, title1_text_pos)

        title2_text = assets.F_JERSEY10_LARGE.render("CINmulator", True, const.WHITE)
        title2_text_pos = (
            const.WINDOW_CENTRE[0] - (title2_text.get_width() // 2),
            title1_text_pos[1] + 70,
        )
        surface.blit(title2_text, title2_text_pos)

        # If in pause menu or main menu
        play_option_value = "COMEÇAR" if not Context.paused else "CONTINUAR"
        play_option_pos = (
            const.WINDOW_CENTRE[0]
            - assets.F_JERSEY10_MEDIUM.size(play_option_value)[0] // 2,
            title2_text_pos[1] + 350,
        )
        quit_option_pos = (
            const.WINDOW_CENTRE[0]
            - assets.F_JERSEY10_MEDIUM.size("SAIR DO JOGO")[0] // 2,
            play_option_pos[1] + 50,
        )

        if self.selected_option == "play":
            play_option_color = const.YELLOW
            quit_option_color = const.ORANGE
            heart_pos = (play_option_pos[0] - 40, play_option_pos[1] + 7)
        else:
            play_option_color = const.ORANGE
            quit_option_color = const.YELLOW
            heart_pos = (quit_option_pos[0] - 40, quit_option_pos[1] + 7)

        play_option = assets.F_JERSEY10_MEDIUM.render(
            play_option_value, True, play_option_color
        )
        quit_option = assets.F_JERSEY10_MEDIUM.render(
            "SAIR DO JOGO", True, quit_option_color
        )

        surface.blit(play_option, play_option_pos)
        surface.blit(quit_option, quit_option_pos)

        surface.blit(assets.S_HEART, heart_pos)

    def exit(self) -> None:
        pass
