import pygame
import core.constants as const
import core.assets as asset
import scenes.game
import scenes.menu

from core.input import InputBuffer, InputState, Action
from scenes.scene import Scene
from scenes.context import Context
from components.dialog_printer import DialogPrinter

last_char_time = pygame.time.get_ticks()
lines_formatted = []
lines_completed = []
curr_line_text = ""
line_index = 0
char_index = 0
CHAR_LIMIT = 20
TYPING_DELAY = 60 # 60 ms

class Dialog(Scene):
    def enter(self) -> None:
        pygame.mixer.music.unpause()
        self.printer = DialogPrinter(
            text=Context.dialog_text,
            char_limit=CHAR_LIMIT,
            typing_delay=TYPING_DELAY
        )

    def execute(self, surface, dt, action_buffer) -> None:
        if action_buffer[Action.OPTIONS] == InputState.PRESSED:
            Context.last_scene = Dialog # type: ignore
            Context.paused = True
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore
            return

        if not self.printer.finished:
            if action_buffer[Action.START] == InputState.PRESSED:
                self.printer.skip()
            else:
                self.printer.update()
        else:
            if action_buffer[Action.START] == InputState.PRESSED:
                self.statemachine.change_state(scenes.game.Game) # type: ignore
                return

        surface.fill(const.BLACK)
        self.printer.draw(surface, asset.DEBUG_FONT_SMALL, (700, 100))

    def exit(self) -> None:
        pygame.mixer.music.pause()
        self.printer = None


