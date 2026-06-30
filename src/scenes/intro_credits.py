import pygame

from components.config import Config
from components.dialog_printer import DialogConfig, DialogPrinter
import core.constants as const
import core.assets as assets
from scenes.menu import Menu
from core.input import InputBuffer
from scenes.scene import Scene
from utilities import languages


class IntroCredits(Scene):
    def enter(self) -> None:
        self.config = Config()
        self.interface = languages.INTERFACE[self.config.data["lang"]]
        printer_config = DialogConfig(80, 20, const.WHITE)
        pygame.time.wait(1000)

        texts_and_fonts = [
            (
                self.interface["intro_credits"]["made_by"],
                assets.F_JERSEY10_MEDIUM_LARGE,
            ),
            ("Arthur Jordão", assets.F_JERSEY10_MEDIUM),
            ("Bruno Rodrigues", assets.F_JERSEY10_MEDIUM),
            ("Fabrício Fernandes", assets.F_JERSEY10_MEDIUM),
            ("Gabriel Almeida", assets.F_JERSEY10_MEDIUM),
            ("João Eduardo", assets.F_JERSEY10_MEDIUM),
            ("Lucas Rafhael", assets.F_JERSEY10_MEDIUM),
        ]

        cx, cy = const.WINDOW_CENTRE[0], const.WINDOW_CENTRE[1]
        heights = [cy - 200, cy - 80, cy - 40, cy, cy + 40, cy + 80, cy + 120]

        self.positions = []
        for i, (text, font) in enumerate(texts_and_fonts):
            pos_x = cx - (font.size(text)[0] // 2)
            pos_y = heights[i]

            self.positions.append((pos_x, pos_y))

        self.printer_made_by = DialogPrinter.simple(
            texts_and_fonts[0][0], printer_config
        )
        self.printer_arthur = DialogPrinter.simple(
            texts_and_fonts[1][0], printer_config
        )
        self.printer_bruno = DialogPrinter.simple(texts_and_fonts[2][0], printer_config)
        self.printer_fabricio = DialogPrinter.simple(
            texts_and_fonts[3][0], printer_config
        )
        self.printer_gabriel = DialogPrinter.simple(
            texts_and_fonts[4][0], printer_config
        )
        self.printer_joao = DialogPrinter.simple(texts_and_fonts[5][0], printer_config)
        self.printer_lucas = DialogPrinter.simple(texts_and_fonts[6][0], printer_config)

        self.printer_fase = 0
        self.waiting = False
        self.delay_timer = 0
        self.fade_alpha = 0

    def execute(
        self,
        surface: pygame.Surface,
        _dt: float,
        _action_buffer: InputBuffer,
    ) -> None:
        surface.fill(const.BLACK)
        now = pygame.time.get_ticks()

        # Display all the texts letter by letter
        if self.printer_fase == 0:
            self.handle_printer_writing(self.printer_made_by, now, 1000)
        elif self.printer_fase == 1:
            self.handle_printer_writing(self.printer_arthur, now, 300)
        elif self.printer_fase == 2:
            self.handle_printer_writing(self.printer_bruno, now, 300)
        elif self.printer_fase == 3:
            self.handle_printer_writing(self.printer_fabricio, now, 300)
        elif self.printer_fase == 4:
            self.handle_printer_writing(self.printer_gabriel, now, 300)
        elif self.printer_fase == 5:
            self.handle_printer_writing(self.printer_joao, now, 300)
        elif self.printer_fase == 6:
            self.handle_printer_writing(self.printer_lucas, now, 300)

        # Draw the texts
        if self.printer_fase >= 0:
            self.printer_made_by.draw(
                surface, assets.F_JERSEY10_MEDIUM_LARGE, self.positions[0]
            )
        if self.printer_fase >= 1:
            self.printer_arthur.draw(
                surface, assets.F_JERSEY10_MEDIUM, self.positions[1]
            )
        if self.printer_fase >= 2:
            self.printer_bruno.draw(
                surface, assets.F_JERSEY10_MEDIUM, self.positions[2]
            )
        if self.printer_fase >= 3:
            self.printer_fabricio.draw(
                surface, assets.F_JERSEY10_MEDIUM, self.positions[3]
            )
        if self.printer_fase >= 4:
            self.printer_gabriel.draw(
                surface, assets.F_JERSEY10_MEDIUM, self.positions[4]
            )
        if self.printer_fase >= 5:
            self.printer_joao.draw(surface, assets.F_JERSEY10_MEDIUM, self.positions[5])
        if self.printer_fase >= 6:
            self.printer_lucas.draw(
                surface, assets.F_JERSEY10_MEDIUM, self.positions[6]
            )

        # Apply the fade out effect
        if self.printer_fase == 7:
            fade_surface = pygame.Surface((surface.get_width(), surface.get_height()))
            fade_surface.fill(const.BLACK)
            fade_surface.set_alpha(self.fade_alpha)

            surface.blit(fade_surface, (0, 0))
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + 3)
            else:
                self.statemachine.change_state(Menu)

    def exit(self) -> None:
        pass

    def handle_printer_writing(self, printer: DialogPrinter, now: int, delay: int):
        if not self.waiting:
            printer.update()
            assets.SFX_MASTER.audios["intro_talking"].play(-1)

            if printer.finished:
                self.waiting = True
                self.delay_timer = now
                assets.SFX_MASTER.audios["intro_talking"].stop()
        else:
            if now - self.delay_timer >= delay:
                self.waiting = False
                self.printer_fase += 1
