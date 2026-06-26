import pygame


class DialogConfig:
    """
    Agrupa os parâmetros de exibição de um contexto de diálogo.
    """

    BATTLE = None
    INTRO = None
    TALK_BOX = None

    def __init__(
        self,
        char_limit: int,
        typing_delay: int = 30,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.char_limit   = char_limit
        self.typing_delay = typing_delay
        self.color        = color


DialogConfig.BATTLE = DialogConfig(char_limit=40, typing_delay=30) # type: ignore
DialogConfig.INTRO = DialogConfig(char_limit=85, typing_delay=10) # type: ignore
DialogConfig.TALK_BOX = DialogConfig(char_limit=23, typing_delay=30, color=(0, 0, 0)) # type: ignore


def _format_text(text: str, limit: int) -> list[str]:
    """
    Quebra o texto em linhas sem cortar palavras no meio.
    """

    words = text.split(" ")
    lines: list[str] = []
    current = ""

    for word in words:
        if word == "\n":
            if current:
                lines.append(current)
                current = ""
            continue

        if len(word) > limit:
            if current:
                lines.append(current)
                current = ""
            lines.append(word)
            continue

        sep = " " if current else ""
        if len(current) + len(sep) + len(word) <= limit:
            current += sep + word
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


class DialogPrinter:
    def __init__(self, texts: list[str], config: DialogConfig) -> None:
        self._texts = texts
        self._config = config

        self._text_index = 0          # qual texto da sequência está ativo
        self._lines: list[str] = []   # linhas formatadas do texto atual
        self._done: list[str] = []   # linhas já completamente exibidas
        self._curr = ""             # linha sendo digitada agora
        self._line_i = 0              # índice da linha em andamento
        self._char_i = 0              # índice do char em andamento
        self._last_t = pygame.time.get_ticks()

        self._load_current_text()


    @classmethod
    def simple(cls, text: str, config: DialogConfig) -> "DialogPrinter":
        return cls([text], config)

    @classmethod
    def sequence(cls, texts: list[str], config: DialogConfig) -> "DialogPrinter":
        return cls(texts, config)


    @property
    def page_finished(self) -> bool:
        """
        Animação do texto atual terminou (mas pode haver próximos na sequência).
        """

        return self._line_i >= len(self._lines)

    @property
    def finished(self) -> bool:
        """
        Toda a sequência foi exibida.
        """

        return self.page_finished and self._text_index >= len(self._texts) - 1

    @property
    def has_next(self) -> bool:
        return self._text_index < len(self._texts) - 1


    def advance(self) -> bool:
        if not self.page_finished:
            self._skip_current_page()
            return False
        elif self.has_next:
            self._text_index += 1
            self._load_current_text()
            return True
        return False

    def reset(self) -> None:
        """
        Volta ao início da sequência.
        """

        self._text_index = 0
        self._load_current_text()

    def set_texts(self, texts: list[str]) -> None:
        """
        Substitui toda a sequência e reinicia.
        """

        self._texts = texts
        self._text_index = 0
        self._load_current_text()

    def set_text(self, text: str) -> None:
        """
        Atalho para substituir por um único texto.
        """

        self.set_texts([text])

    def set_config(self, config: DialogConfig) -> None:
        self._config = config
        self._load_current_text()

    def update(self) -> None:
        if self.page_finished:
            return

        now = pygame.time.get_ticks()
        if now - self._last_t <= self._config.typing_delay:
            return

        target = self._lines[self._line_i]

        if self._char_i < len(target):
            self._curr += target[self._char_i]
            self._char_i += 1
        else:
            self._done.append(self._curr)
            self._curr = ""
            self._char_i = 0
            self._line_i += 1

        self._last_t = now

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        pos: tuple[int, int],
        color: tuple[int, int, int] | None = None,
    ) -> None:
        color = color or self._config.color
        x, y = pos
        lh = font.get_linesize()

        for line in self._done:
            surface.blit(font.render(line, True, color), (x, y))
            y += lh

        if self._curr:
            surface.blit(font.render(self._curr, True, color), (x, y))

    def _load_current_text(self) -> None:
        text = self._texts[self._text_index]
        self._lines = _format_text(text, self._config.char_limit)
        self._done = []
        self._curr = ""
        self._line_i = 0
        self._char_i = 0
        self._last_t = pygame.time.get_ticks()

    def _skip_current_page(self) -> None:
        self._done = list(self._lines)
        self._curr = ""
        self._line_i = len(self._lines)
