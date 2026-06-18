import pygame

import core.constants as const
import core.input as input
import core.assets as assets

from scenes.context import Context
from scenes.scene import Scene
import scenes.game


MENU_SPRITE = assets.MENU_SPRITE
MENU_SPRITE_X = const.WINDOW_CENTRE[0] - MENU_SPRITE.get_width() // 2
MENU_SPRITE_Y = const.WINDOW_CENTRE[1] - MENU_SPRITE.get_height() // 2


class Pause(Scene):
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
                self.statemachine.change_state(Context.last_scene) # type: ignore
                return
            else:
                pygame.quit()
                raise SystemExit

        surface.fill(const.BLACK)
        surface.blit(MENU_SPRITE, (MENU_SPRITE_X, MENU_SPRITE_Y))

        play_option_pos = (const.WINDOW_CENTRE[0] - assets.DEBUG_FONT_MEDIUM.size("CONTINUAR")[0] // 2, MENU_SPRITE_Y + 300)
        quit_option_pos = (const.WINDOW_CENTRE[0] - assets.DEBUG_FONT_MEDIUM.size("SAIR DO JOGO")[0] // 2, play_option_pos[1] + 50)

        if self.selected_option == 'play':
            play_option_color = const.YELLOW
            quit_option_color = const.ORANGE
            heart_pos = (play_option_pos[0] - 60, play_option_pos[1])
        else:
            play_option_color = const.ORANGE
            quit_option_color = const.YELLOW
            heart_pos = (quit_option_pos[0] - 60, quit_option_pos[1])

        play_option_text = assets.DEBUG_FONT_MEDIUM.render("CONTINUAR", True, play_option_color)
        quit_option_text = assets.DEBUG_FONT_MEDIUM.render("SAIR DO JOGO", True, quit_option_color)

        surface.blit(play_option_text, play_option_pos)
        surface.blit(quit_option_text, quit_option_pos)

        surface.blit(assets.HEART_SPRITE, heart_pos)


    def exit(self) -> None:
        pass
