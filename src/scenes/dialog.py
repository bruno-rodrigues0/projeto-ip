import pygame
import core.constants as const
import core.assets as asset
import scenes.game
import scenes.menu

from core.input import InputBuffer, InputState, Action
from scenes.scene import Scene
from scenes.context import Context

last_char_time = pygame.time.get_ticks()
lines_formatted = []
lines_completed = []
curr_line_text = ""
line_index = 0
char_index = 0
CHAR_LIMIT = 20
TYPING_DELAY = 60 # 100 ms

def format_text(text: str, limit: int) -> list[str]:
    """Splits text into lines without cutting words in the middle."""
    words = text.split(" ")
    final_lines = []
    current_line = ""

    for word in words:
        if len(word) > limit:
            if current_line:
                final_lines.append(current_line)
                current_line = ""
            final_lines.append(word)
            continue

        space = " " if current_line else ""
        if len(current_line) + len(space) + len(word) <= limit:
            current_line += space + word
        else:
            final_lines.append(current_line)
            current_line = word

    if current_line:
        final_lines.append(current_line)
        
    return final_lines


class Dialog(Scene):
    def enter(self) -> None:
        pygame.mixer.music.unpause()
        global lines_formatted, lines_completed, curr_line_text, line_index, char_index, last_char_time
        
        # Format the context text right when entering the scene
        lines_formatted = format_text(Context.dialog_text, CHAR_LIMIT)
        lines_completed = []
        curr_line_text = ""
        line_index = 0
        char_index = 0
        last_char_time = pygame.time.get_ticks()

    def execute(
        self, 
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:
        global lines_formatted, lines_completed, curr_line_text, line_index, char_index, last_char_time
        curr_time = pygame.time.get_ticks()

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            Context.last_scene = Dialog # type: ignore
            Context.paused = True
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore
            return

        text_finished = line_index >= len(lines_formatted)

        if not text_finished:
            if action_buffer[Action.START] == InputState.PRESSED:
                lines_completed = list(lines_formatted)
                curr_line_text = ""
                line_index = len(lines_formatted)
            
            elif curr_time - last_char_time > TYPING_DELAY:
                target_line = lines_formatted[line_index]
                
                if char_index < len(target_line):
                    curr_line_text += target_line[char_index]
                    char_index += 1
                else:
                    lines_completed.append(curr_line_text)
                    curr_line_text = ""
                    char_index = 0
                    line_index += 1
                    
                last_char_time = curr_time
        else:
            if action_buffer[Action.START] == InputState.PRESSED:
                self.statemachine.change_state(scenes.game.Game) # type: ignore
                return

        surface.fill(const.BLACK)
        
        y_offset = 100
        x_pos = 700
        line_height = asset.DEBUG_FONT_SMALL.get_linesize()

        for line in lines_completed:
            text_surface = asset.DEBUG_FONT_SMALL.render(line, True, const.WHITE)
            surface.blit(text_surface, (x_pos, y_offset))
            y_offset += line_height

        if curr_line_text:
            text_surface = asset.DEBUG_FONT_SMALL.render(curr_line_text, True, const.WHITE)
            surface.blit(text_surface, (x_pos, y_offset))

    def exit(self) -> None:
        pygame.mixer.music.pause()
        global lines_formatted, lines_completed, curr_line_text, line_index, char_index
        lines_formatted = []
        lines_completed = []
        curr_line_text = ""
        line_index = 0
        char_index = 0


