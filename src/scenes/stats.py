import pygame
import core.assets as assets
import core.constants as const
import scenes.menu

from components.statistics import Statistics
from utilities import languages
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from components.config import Config


stats = Statistics()

class Stats(Scene):
    def enter(self) -> None:
        pass

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:
        global stats
        stats.load_file()
        config = Config()
        lang = languages.INTERFACE[config.data["lang"]]

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore


        surface.fill(const.BLACK)
        for i, key in enumerate(stats.data):
            value = stats.data[key]
            if key == "game_time":
                min = value < 3600
                value = value // 60 if value < 3600 else value / 3600
                text = assets.F_JERSEY10.render(f"{lang['stats'][key]}: {value:.1f} {'min' if min else 'h'}", True, const.WHITE)
            else:
                text = assets.F_JERSEY10.render(f"{lang['stats'][key]}: {value}", True, const.WHITE)

            surface.blit(text, (const.WINDOW_CENTRE[0] - (text.get_width() // 2), 200 + 30 * i))

        has_joystick = pygame.joystick.get_count() > 0
        back_subtitle = assets.F_JERSEY10_MEDIUM.render(f'{lang["options_menu"]["back"]} [{"ESC" if not has_joystick else "Options"}]', True, const.WHITE)
        surface.blit(back_subtitle, (100, const.WINDOW_HEIGHT - 50))

    def exit(self) -> None:
        pass
