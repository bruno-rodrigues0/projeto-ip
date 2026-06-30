import pygame
import scenes.menu
import core.constants as const
import core.assets as assets

from scenes.scene import Scene
from scenes.context import Context
from core.input import InputBuffer, InputState, Action


class Victory(Scene):
    def enter(self) -> None:
        self.selected_option = 'retry'
        # Guarda o score da partida antes de qualquer reset, para colocar na tela
        self.score = {
            "Orbes de vida": Context.collected_life_orbs,
            "Orbes de defesa": Context.collected_defense_orbs,
            "Orbes de dano": Context.collected_damage_orbs,
        }
        assets.SFX_MASTER.audios["undertale"].play()

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        #troca a opção e confirma
        if action_buffer[Action.DOWN] == InputState.PRESSED:
            self.selected_option = 'quit'
        if action_buffer[Action.UP] == InputState.PRESSED:
            self.selected_option = 'retry'
        if action_buffer[Action.A] == InputState.PRESSED:
            if self.selected_option == 'retry':
                reset_match()
                self.statemachine.change_state(scenes.menu.Menu)  # type: ignore
                return
            else:
                pygame.event.post(pygame.Event(pygame.QUIT))
                return

        # FUNDO preto
        surface.fill(const.BLACK)

        # "VITÓRIA" grande, em amarelo, centralizado
        title = assets.F_JERSEY10_LARGE.render("VITORIA!", True, const.YELLOW)
        title_pos = (
            const.WINDOW_CENTRE[0] - title.get_width() // 2,
            80,
        )
        surface.blit(title, title_pos)

        # Subtítulo
        subtitle = assets.F_JERSEY10_MEDIUM.render("Voce derrotou Michael Jackson", True, const.WHITE)
        surface.blit(
            subtitle,
            (const.WINDOW_CENTRE[0] - subtitle.get_width() // 2, title_pos[1] + 100),
        )

        # SCORE da partida: itens coletados
        score_y = 280
        for i, (label, value) in enumerate(self.score.items()):
            line = assets.F_JERSEY10.render(f"{label}: {value}", True, const.WHITE)
            surface.blit(
                line,
                (const.WINDOW_CENTRE[0] - line.get_width() // 2, score_y + 40 * i),
            )

        # OPÇÕES: amarela na selecionada, branca na outra
        retry_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size("JOGAR DE NOVO")[0] // 2,
            const.WINDOW_HEIGHT - 130,
        )
        quit_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size("SAIR DO JOGO")[0] // 2,
            retry_pos[1] + 50,
        )

        retry_color = const.YELLOW if self.selected_option == 'retry' else const.WHITE
        quit_color = const.YELLOW if self.selected_option == 'quit' else const.WHITE

        retry_text = assets.F_JERSEY10_MEDIUM.render("JOGAR DE NOVO", True, retry_color)
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
    player = scenes.game.PLAYER
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
    Context.battle_state = "battle_menu"
