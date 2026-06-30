import pygame

from components.config import Config
import core.constants as const
import core.input as input
import core.assets as assets

from scenes.context import Context
from scenes.scene import Scene
import scenes.intro
import scenes.settings
import scenes.stats
import scenes.achievements
from utilities import languages


class Menu(Scene):
    """
    Main/pause menu scene.
    """
    is_start: bool = True
    def enter(self) -> None:
        self.selected_option = 0
        for audio in assets.SFX_MASTER.audios:
            assets.SFX_MASTER.audios[audio].stop()
        
        if Menu.is_start:
            pygame.time.wait(1000)
            assets.SFX_MASTER.audios["intro_menu_sound"].play()
            Menu.is_start = False

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: input.InputBuffer,
    ) -> None:
        config = Config()
        interface = languages.INTERFACE[config.data["lang"]]

        menu_options = [
            interface["initial_menu"]["start"][1] if Context.paused else interface["initial_menu"]["start"][0],
            interface["initial_menu"]["options"],
            interface["initial_menu"]["stats"],
            interface["initial_menu"]["achievements"],
            interface["initial_menu"]["quit"]
        ]

        if action_buffer[input.Action.DOWN] == input.InputState.PRESSED:
            self.selected_option = (self.selected_option + 1) % len(menu_options)
            assets.SFX_MASTER.audios["move_selection"].play()
        if action_buffer[input.Action.UP] == input.InputState.PRESSED:
            self.selected_option = (self.selected_option - 1) % len(menu_options)
            assets.SFX_MASTER.audios["move_selection"].play()

        if action_buffer[input.Action.A] == input.InputState.PRESSED:
            assets.SFX_MASTER.audios["select_option"].play()
            if (
                self.selected_option == menu_options.index(interface["initial_menu"]["start"][0])
                if not Context.paused else self.selected_option == menu_options.index(interface["initial_menu"]["start"][1])
            ):
                # If paused, back to last_scene, else go to Intro scene
                if Context.paused:
                    self.statemachine.change_state(Context.last_scene)
                else:
                    Context.paused = False
                    Context.last_scene = Menu # type: ignore
                    self.statemachine.change_state(scenes.intro.Intro)  # type: ignore
                return
            elif self.selected_option == menu_options.index(interface["initial_menu"]["options"]):
                self.statemachine.change_state(scenes.settings.Settings)
            elif self.selected_option == menu_options.index(interface["initial_menu"]["stats"]):
                self.statemachine.change_state(scenes.stats.Stats)
            elif self.selected_option == menu_options.index(interface["initial_menu"]["achievements"]):
                self.statemachine.change_state(scenes.achievements.Achievements)
            else:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return

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
                title2_text_pos[1] + 250 + 50 * (i),
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
