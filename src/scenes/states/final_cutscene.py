import pygame
import random
from components.statemachine import State
import core.assets as assets
import core.constants as const
import scenes.victory

from components.config import Config
from components.dialog_printer import DialogConfig, DialogPrinter
from core.input import InputBuffer, InputState, Action
from utilities import languages

class DustParticle:
    def __init__(self, surf: pygame.Surface, x: float, y: float) -> None:
        self.surf = surf
        self.x = x
        self.y = y
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-100, -160)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.surf, (self.x, self.y))


class DisintegrateEffect:
    """
    Efeito de desintegração estilo Undertale: o sprite se parte em
    pedaços que sobem até saírem da tela.
    """

    def __init__(
        self,
        sprite: pygame.Surface,
        pos: tuple[int, int],
        chunk_size: int = 3,
    ) -> None:
        self.pos = pos
        self.particles: list[DustParticle] = []

        white_sprite = self._to_white_silhouette(sprite)
        self._build_particles(white_sprite, chunk_size)

    def _to_white_silhouette(self, sprite: pygame.Surface) -> pygame.Surface:
        arr_alpha = pygame.surfarray.pixels_alpha(sprite)
        w = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        w.fill((255, 255, 255, 255))
        pygame.surfarray.pixels_alpha(w)[:] = arr_alpha
        del arr_alpha
        return w

    def _build_particles(self, sprite: pygame.Surface, chunk: int) -> None:
        w, h = sprite.get_size()

        for y in range(0, h, chunk):
            for x in range(0, w, chunk):
                rect_w = min(chunk, w - x)
                rect_h = min(chunk, h - y)
                rect = pygame.Rect(x, y, rect_w, rect_h)
                piece = sprite.subsurface(rect).copy()

                if pygame.transform.average_color(piece)[3] == 0:
                    continue

                self.particles.append(
                    DustParticle(piece, self.pos[0] + x, self.pos[1] + y)
                )

    def update(self, dt: float) -> None:
        for p in self.particles:
            p.update(dt)

    @property
    def finished(self) -> bool:
        return all(p.y < -10 for p in self.particles)

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surface)


class FinalCutscene(State):
    @staticmethod
    def enter(game) -> None:
        config = Config()
        michael_y = const.WINDOW_CENTRE[1] - 200
        game.michael_pos = (
            const.WINDOW_CENTRE[0] - assets.S_MICHAEL_BATTLE[0].get_width() // 2,
            michael_y
        )
        game.dust_effect = DisintegrateEffect(
            assets.S_MICHAEL_BATTLE[0],
            game.michael_pos,
            7,
        )

        dialogs = languages.DIALOGS[config.data["lang"]]
        printer_config = DialogConfig(23, 70, const.BLACK)
        game.printer = DialogPrinter.sequence(
            dialogs["final_cutscene"],
            printer_config
        )
        assets.SFX_MASTER.audios["talking_long_slowed"].play(-1)
        game.dust_sound_played = False

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:
        if action_buffer[Action.A] == InputState.PRESSED:
            advanced = game.printer.advance()

            if advanced:
                assets.SFX_MASTER.audios["talking_long_slowed"].play(-1)
            else:
                assets.SFX_MASTER.audios["talking_long_slowed"].stop()

        if not game.printer.page_finished:
            game.printer.update()
        else:
            assets.SFX_MASTER.audios["talking_long_slowed"].stop()

        if game.printer.finished:
            if not game.dust_sound_played:
                assets.SFX_MASTER.audios["dust"].play()
                game.dust_sound_played = True
            game.dust_effect.update(dt)
            game.dust_effect.draw(surface)

            if game.dust_effect.finished:
                pygame.time.wait(2000)
                game.statemachine.change_state(scenes.victory.Victory)
        else:
            surface.blit(assets.S_MICHAEL_BATTLE[0], game.michael_pos)

        surface.blit(assets.S_TALK_BOX, (const.WINDOW_CENTRE[0] + 100, 100))
        game.printer.draw(surface, assets.F_JERSEY10_SMALL, (const.WINDOW_CENTRE[0] + 130, 110))
