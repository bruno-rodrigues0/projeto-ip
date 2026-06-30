import pygame
import scenes.menu
import core.assets as assets
import core.constants as const

from components.config import Config
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from utilities import languages
from components.achievements import AchievementsManager


achievements = AchievementsManager()

class Achievements(Scene):
    def enter(self) -> None:
        pass

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:
        global achievements
        config = Config()
        lang = languages.INTERFACE[config.data["lang"]]

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore



        surface.fill(const.BLACK)

        for i, key in enumerate(achievements.data):
            has_achievement = achievements.data[key]
            rect_pos = (
                100 + 350 * (i // 2),
                100 + 150 * (i % 2),
                300,
                100
            )
            color = const.WHITE if has_achievement else const.GRAY

            text = assets.F_JERSEY10.render(lang["achievements"][key], True, const.WHITE) if has_achievement else assets.F_JERSEY10.render(lang["achievements"]["locked"], True, color)
            text_pos = (
                rect_pos[0] + 10,
                rect_pos[1] + 30
            )
            pygame.draw.rect(surface, color, rect_pos, 3)
            surface.blit(text, text_pos)

        has_joystick = pygame.joystick.get_count() > 0
        back_subtitle = assets.F_JERSEY10_MEDIUM.render(f'{lang["options_menu"]["back"]} [{"ESC" if not has_joystick else "Options"}]', True, const.WHITE)
        surface.blit(back_subtitle, (100, const.WINDOW_HEIGHT - 50))


    def exit(self) -> None:
        pass
