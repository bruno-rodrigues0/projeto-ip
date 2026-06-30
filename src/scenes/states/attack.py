import pygame
from components.statemachine import State
import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from scenes.context import Context


class Attack(State):
    """Attack — exibe a barra de ataque."""

    wait_timer = 1.0
    is_waiting = False
    cursor_x: float = const.WINDOW_CENTRE[0] - 300
    cursor_color: pygame.Color = const.WHITE
    blink_timer: float = 0.0
    player_damage: float | str = ''

    @staticmethod
    def enter(game) -> None:
        Attack.wait_timer = 1.0
        Attack.is_waiting = False
        Attack.cursor_x = const.WINDOW_CENTRE[0] - 300
        Attack.blink_timer: float = 0.0
        Attack.player_damage = ''

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        # Time to play the audio and display the cursor glitch effect
        if Attack.is_waiting:
            Attack.wait_timer -= dt
            Attack.blink_timer += dt

            # Handle the blink effect
            if Attack.blink_timer >= 0.06 and not isinstance(Attack.player_damage, str):
                Attack.blink_timer = 0.0
                if Attack.cursor_color == const.WHITE:
                    Attack.cursor_color = const.RED
                else:
                    Attack.cursor_color = const.WHITE

            if Attack.wait_timer <= 0:
                Attack.cursor_color = const.WHITE
                game.initial_time = pygame.time.get_ticks()
                Context.battle_state = "fight"
                Attack.is_waiting = False
                Attack.wait_timer = 1.0
                return
            
        # Cursor is moving while the player not attack
        else:
            Attack.cursor_x += 600 * dt
            if Attack.cursor_x >= 546 + (const.WINDOW_CENTRE[0] - 273) + 10:
                Attack.player_damage = "MISS"
                Attack.is_waiting = True

        if action_buffer[Action.A] == InputState.PRESSED and not Attack.is_waiting:
            distance = min(abs(Attack.cursor_x - const.WINDOW_CENTRE[0]), 273)
            attack_factor = 1 - (distance / 273)
            player_final_attack = int(game.player.damage * (1 + attack_factor))
            Context.BOSS.take_damage(player_final_attack)
            Attack.wait_timer = 1.0
            Attack.is_waiting = True
            Attack.player_damage = player_final_attack

        # Draw the attack bar
        pygame.draw.rect(
            surface, const.WHITE, (const.WINDOW_CENTRE[0] - 300, 380, 600, 155), 5
        )
        for i in range(0, 6, 2):
            if game.selected_option == i:
                surface.blit(
                    assets.S_MENU_OPTIONS[i + 1],
                    (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600),
                )
            else:
                surface.blit(
                    assets.S_MENU_OPTIONS[i],
                    (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600),
                )
        surface.blit(assets.S_ATTACK_BAR, (const.WINDOW_CENTRE[0] - 273, 400))

        # Draw the cursor
        pygame.draw.rect(
            surface, Attack.cursor_color, (int(Attack.cursor_x), 385, 10, 145)
        )

        # Display the player damage
        if Attack.is_waiting:
            if isinstance(Attack.player_damage, str):
                text_config = (False, const.WHITE,)
            else:
                text_config = (False, const.RED,)
            damage_text = assets.F_JERSEY10_MEDIUM_LARGE.render(str(Attack.player_damage), *text_config)
            surface.blit(damage_text, (const.WINDOW_CENTRE[0] - damage_text.get_width() // 2, 50))
