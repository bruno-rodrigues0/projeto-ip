import pygame
import core.constants as const
import core.setup as setup
from entities.player import Player

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
    player_dim = pygame.Vector2(30, 30)
    while True:
        elapsed_time = clock.tick(const.FPS)
        dt = elapsed_time / 1000.0
        dt = min(dt, const.MAX_DT)

        running = to_quit()

        if not running:
            terminate(surface)

        surface.fill(const.WHITE)

        player = Player(surface, player_dim)
        mouse = pygame.mouse.get_pos()
        player.pos.x = mouse[0] - player_dim.x / 2
        player.pos.y = mouse[1] - player_dim.x / 2

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     player.vel.y = -300
        # elif keys[pygame.K_s]:
        #     player.vel.y = 300
        # elif keys[pygame.K_a]:
        #     player.vel.x = -300
        # elif keys[pygame.K_d]:
        #     player.vel.x = 300
        # else:
        #     player.vel.x = 0
        #     player.vel.y = 0

        player.update(dt)
        pygame.display.flip()

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

