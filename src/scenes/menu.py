import pygame

import core.constants as const
import core.input as input
import core.assets as assets

from scenes.context import Context
from scenes.scene import Scene
import scenes.intro
import scenes.settings


class Menu(Scene):
    """
    Main/pause menu scene.
    """

    def enter(self) -> None:
        self.selected_option = 0
        for audio in assets.SFX_MASTER.audios:
            assets.SFX_MASTER.audios[audio].stop()

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: input.InputBuffer,
    ) -> None:
        menu_options = ["CONTINUAR" if Context.paused else "COMEÇAR", "OPÇÕES", "SAIR DO JOGO"]
        if action_buffer[input.Action.DOWN] == input.InputState.PRESSED:
            self.selected_option = (self.selected_option + 1) % 3
            assets.SFX_MASTER.audios["move_selection"].play()
        if action_buffer[input.Action.UP] == input.InputState.PRESSED:
            self.selected_option = (self.selected_option - 1) % 3
            assets.SFX_MASTER.audios["move_selection"].play()

        if action_buffer[input.Action.START] == input.InputState.PRESSED:
            assets.SFX_MASTER.audios["select_option"].play()
            if self.selected_option == 0: # play
                # If paused, back to last_scene, else go to Intro scene
                if Context.paused:
                    self.statemachine.change_state(Context.last_scene)
                else:
                    Context.paused = False
                    Context.last_scene = Menu # type: ignore
                    self.statemachine.change_state(scenes.intro.Intro)  # type: ignore
                return
            elif self.selected_option == 1: # settings
                self.statemachine.change_state(scenes.settings.Settings)
            else: #quit
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

        heart_pos = (0, 0)
        for i, option in enumerate(menu_options):
            pos = (
                const.WINDOW_CENTRE[0]
                - assets.F_JERSEY10_MEDIUM.size(option)[0] // 2,
                title2_text_pos[1] + 300 + 50 * (i),
            )

            if self.selected_option == i:
                color = const.YELLOW
                heart_pos = (pos[0] - 40, pos[1] + 7)
            else:
                color = const.ORANGE

            option_text = assets.F_JERSEY10_MEDIUM.render(option, True, color)

            surface.blit(option_text, pos)

        surface.blit(assets.S_HEART, heart_pos)

    def exit(self) -> None:
        pass
