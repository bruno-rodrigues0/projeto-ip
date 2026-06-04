import pygame
import core.constants as const
import core.setup as setup

def run() -> None:
    """
    Inicia o game loop.
    """

    pygame.display.set_caption(const.CAPTION)
    game_loop(setup.window, setup.clock)

def game_loop(
    surface: pygame.Surface,
    clock: pygame.time.Clock
) -> None:
    """
    Loop do jogo que lida com todos os eventos e renderiza na tela.
    """

    while True:
        running = to_quit()

        if not running:
            terminate(surface)

        surface.fill(const.WHITE)
        pygame.display.flip()
        clock.tick(const.FPS)

def to_quit() -> bool:
    """
    Detect se ESC foi pressionado ou se um evento de QUIT foi acionado.
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False
    return True

def terminate(surface: pygame.Surface) -> None:
    """
    Finaliza o programa.
    """

    surface.fill(const.BLACK)
    pygame.quit()
    raise SystemExit

