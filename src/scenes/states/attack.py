import pygame
from components.statemachine import State
import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from scenes.context import Context


class Attack(State):
    """Attack — exibe a barra de ataque."""
    wait_timer = 0.0
    is_waiting = False

    @staticmethod
    def enter(game) -> None:
        Attack.wait_timer = 0.0
        Attack.is_waiting = False

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if Attack.is_waiting:
            Attack.wait_timer -= dt
            if Attack.wait_timer <= 0:
                game.initial_time = pygame.time.get_ticks()
                Context.battle_state = "fight"
                Attack.is_waiting = False
                Attack.wait_timer = 0.0
                return

        if action_buffer[Action.A] == InputState.PRESSED and not Attack.is_waiting:
            Context.BOSS.take_damage(game.player.damage)
            Attack.wait_timer = 1.0
            Attack.is_waiting = True

        pygame.draw.rect(surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5)
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(assets.S_MENU_OPTIONS[i + 1], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
            else:
                surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))
        surface.blit(assets.S_ATTACK_BAR, (const.WINDOW_CENTRE[0] - 273, 400))
