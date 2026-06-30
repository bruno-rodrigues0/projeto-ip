import pygame

import core.constants as const
import core.assets as assets
from scenes.scene import Scene
from scenes.context import Context
from core.input import InputBuffer, InputState, Action


class GameOver(Scene):
    def enter(self) -> None:
        self.selected_option = 'retry'
        self.tempo = 0.0                       # digitando
        assets.SFX_MASTER.audios["hee_hee"].play()

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        # troca de opcao
        if action_buffer[Action.DOWN] == InputState.PRESSED:
            self.selected_option = 'quit'
        if action_buffer[Action.UP] == InputState.PRESSED:
            self.selected_option = 'retry'
        if action_buffer[Action.A] == InputState.PRESSED:
            if self.selected_option == 'retry':
                reset_match()
                import scenes.menu
                self.statemachine.change_state(scenes.menu.Menu)  # type: ignore
                return
            else:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return

        # FUNDO preto
        surface.fill(const.BLACK)

        # "GAME OVER" grande, em vermelho, no meio
        game_over_text = assets.F_JERSEY10_LARGE.render("GAME OVER", True, const.RED)
        game_over_pos = (
            const.WINDOW_CENTRE[0] - game_over_text.get_width() // 2,
            const.WINDOW_CENTRE[1] - 150,
        )
        surface.blit(game_over_text, game_over_pos)

        # "-HEE HEE" aparecendo letra por letra
        self.tempo += dt
        texto_completo = "-HEE HEE"
        VELOCIDADE = 8                         # letras por segundo
        n_letras = int(self.tempo * VELOCIDADE)
        texto_visivel = texto_completo[:min(n_letras, len(texto_completo))]

        hee_text = assets.F_JERSEY10_MEDIUM.render(texto_visivel, True, const.WHITE)
        hee_pos = (
            const.WINDOW_CENTRE[0] - hee_text.get_width() // 2,
            game_over_pos[1] + 90,
        )
        surface.blit(hee_text, hee_pos)

        # OPÇÕES: amarela na selecionada, branca na outra
        retry_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size("TENTAR DE NOVO")[0] // 2,
            const.WINDOW_CENTRE[1] + 60,
        )
        quit_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size("SAIR DO JOGO")[0] // 2,
            retry_pos[1] + 50,
        )

        retry_color = const.YELLOW if self.selected_option == 'retry' else const.WHITE
        quit_color = const.YELLOW if self.selected_option == 'quit' else const.WHITE

        retry_text = assets.F_JERSEY10_MEDIUM.render("TENTAR DE NOVO", True, retry_color)
        quit_text = assets.F_JERSEY10_MEDIUM.render("SAIR DO JOGO", True, quit_color)
        surface.blit(retry_text, retry_pos)
        surface.blit(quit_text, quit_pos)

    def exit(self) -> None:
        pass


def reset_match() -> None:
    #zera os coletaveis e a vida do player e do boss
    import scenes.game
    import entities.player

    # Restaura o player
    pygame.mixer.music.rewind()
    player = scenes.game.PLAYER
    player.x = const.WINDOW_CENTRE[0]
    player.y = const.WINDOW_CENTRE[1] + 60
    player.current_hp = player.max_hp
    player.hp_percent = 1.0
    player.damage = player._initial_damage
    player.defense = player._initial_defense

    # Restaura o boss
    Context.BOSS.current_hp = Context.BOSS.max_hp

    # Zera os contadores da partida
    Context.collected_life_orbs = 0
    Context.collected_defense_orbs = 0
    Context.collected_damage_orbs = 0
    Context.used_items = []
    Context.deaths = 0
    Context.battle_state = "battle_menu"
