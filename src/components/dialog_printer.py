import pygame

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

class DialogPrinter:
    def __init__(self, text: str, char_limit: int = 20, typing_delay: int = 60):
        self.lines_formatted = format_text(text, char_limit)
        self.lines_completed = []
        self.curr_line_text = ""
        self.line_index = 0
        self.char_index = 0
        self.last_char_time = pygame.time.get_ticks()
        self.typing_delay = typing_delay

    @property
    def finished(self) -> bool:
        return self.line_index >= len(self.lines_formatted)

    def reset(self) -> None:
        self.lines_completed = []
        self.curr_line_text = ""
        self.line_index = 0
        self.char_index = 0
        self.last_char_time = pygame.time.get_ticks()

    def change_text(self, text: str, char_limit: int) -> None:
        self.lines_formatted = format_text(text, char_limit)
        self.lines_completed = []
        self.curr_line_text = ""
        self.line_index = 0
        self.char_index = 0
        self.last_char_time = pygame.time.get_ticks()

    def skip(self) -> None:
        """Mostra todo o texto de uma vez."""
        self.lines_completed = list(self.lines_formatted)
        self.curr_line_text = ""
        self.line_index = len(self.lines_formatted)

    def update(self) -> None:
        """Avança o estado da animação. Chamar uma vez por frame."""
        if self.finished:
            return

        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_char_time <= self.typing_delay:
            return

        target_line = self.lines_formatted[self.line_index]

        if self.char_index < len(target_line):
            self.curr_line_text += target_line[self.char_index]
            self.char_index += 1
        else:
            self.lines_completed.append(self.curr_line_text)
            self.curr_line_text = ""
            self.char_index = 0
            self.line_index += 1

        self.last_char_time = curr_time

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        pos: tuple[int, int],
        color=(255, 255, 255)
    ) -> None:
        """Desenha o texto na posição dada."""
        x, y = pos
        line_height = font.get_linesize()

        for line in self.lines_completed:
            surface.blit(font.render(line, True, color), (x, y))
            y += line_height

        if self.curr_line_text:
            surface.blit(font.render(self.curr_line_text, True, color), (x, y))
