import random
import pygame
import core.constants as const
import scenes.gameover
import core.assets as assets

from components.statemachine import State
from core.input import InputBuffer



PHASE_HEART_WHOLE = 0
PHASE_HEART_BROKEN = 1
PHASE_FRAGMENTS = 2
PHASE_DONE = 3

WHOLE_DURATION = 1000
BROKEN_DURATION = 1200

GRAVITY = 800.0
FRAGMENT_SPEED_X = (60, 160)
FRAGMENT_SPEED_Y = (-260, -120)


class Fragment:
    """
    Um fragmento individual do coração quebrado, com física simples.
    """

    def __init__(self, image: pygame.Surface, x: float, y: float) -> None:
        self.image = image
        self.x = x
        self.y = y

        direction = random.choice([-1, 1])
        self.vx = direction * random.uniform(*FRAGMENT_SPEED_X)
        self.vy = random.uniform(*FRAGMENT_SPEED_Y)

    def update(self, dt: float) -> None:
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (self.x, self.y))


class GameOverCutscene(State):
    """
    Cutscene de morte do player
    Ao terminar, muda pra cena de Game Over.
    """

    @staticmethod
    def enter(game) -> None:
        game.cutscene_phase = PHASE_HEART_WHOLE
        game.cutscene_timer = 0.0
        game.cutscene_fragments = []
        pygame.mixer.music.stop()
        for audio in assets.SFX_MASTER.audios:
            assets.SFX_MASTER.audios[audio].stop()

        game.heart_pos = (game.player.x, game.player.y)

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        game.cutscene_timer += dt

        surface.fill(const.BLACK)

        if game.cutscene_phase == PHASE_HEART_WHOLE:
            _execute_heart_whole(game, surface)

        elif game.cutscene_phase == PHASE_HEART_BROKEN:
            assets.SFX_MASTER.audios["soul_shatter"].play()
            _execute_heart_broken(game, surface)

        elif game.cutscene_phase == PHASE_FRAGMENTS:
            _execute_fragments(game, surface, dt)

        elif game.cutscene_phase == PHASE_DONE:
            game.statemachine.change_state(scenes.gameover.GameOver)  # type: ignore


def _execute_heart_whole(game, surface: pygame.Surface) -> None:
    surface.blit(assets.S_HEART, game.heart_pos)

    if game.cutscene_timer * 1000 >= WHOLE_DURATION:
        game.cutscene_phase = PHASE_HEART_BROKEN
        game.cutscene_timer = 0.0


def _execute_heart_broken(game, surface: pygame.Surface) -> None:
    surface.blit(assets.S_HEART_BREAK, game.heart_pos)

    if game.cutscene_timer * 1000 >= BROKEN_DURATION:
        game.cutscene_phase = PHASE_FRAGMENTS
        game.cutscene_timer = 0.0
        _spawn_fragments(game)


def _execute_fragments(game, surface: pygame.Surface, dt: float) -> None:
    for fragment in game.cutscene_fragments:
        fragment.update(dt)
        fragment.draw(surface)

    # Termina quando todos os fragmentos saíram da tela por baixo
    if all(f.y > const.WINDOW_HEIGHT for f in game.cutscene_fragments):
        game.cutscene_phase = PHASE_DONE


def _spawn_fragments(game) -> None:
    """Cria um fragmento por sprite do spritesheet S_FRAGMENTS, todos partindo
    da posição do coração."""
    hx, hy = game.heart_pos
    game.cutscene_fragments = [
        Fragment(piece, hx, hy) for piece in assets.S_FRAGMENTS
    ]
