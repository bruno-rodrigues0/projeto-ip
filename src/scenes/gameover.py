import pygame
from components.achievements import AchievementsManager
from components.config import Config
from components.dialog_printer import DialogConfig, DialogPrinter
import scenes.menu
import core.constants as const
import core.assets as assets

from components.statistics import Statistics
from scenes.scene import Scene
from scenes.context import Context
from core.input import InputBuffer, InputState, Action
from utilities import languages


class GameOver(Scene):
    def enter(self) -> None:
        self.selected_option = 'retry'
        self.config = Config()
        printer_config = DialogConfig(20, 150, const.WHITE)
        self.printer = DialogPrinter(["HEE HEE"], printer_config)
        self.interface = languages.INTERFACE[self.config.data["lang"]]

        achievements = AchievementsManager()

        if Context.is_first_attack:
            achievements.data["shit"] = True

        achievements.save_file()

        pygame.time.wait(10)
        assets.SFX_MASTER.audios["hee_hee"].play()

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        # troca de opcao
        if action_buffer[Action.DOWN] == InputState.PRESSED:
            assets.SFX_MASTER.audios["move_selection"].play()
            self.selected_option = 'quit'
        if action_buffer[Action.UP] == InputState.PRESSED:
            assets.SFX_MASTER.audios["move_selection"].play()
            self.selected_option = 'retry'
        if action_buffer[Action.A] == InputState.PRESSED:
            assets.SFX_MASTER.audios["select_option"].play()
            if self.selected_option == 'retry':
                reset_match()
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


        hee_pos = (
            const.WINDOW_CENTRE[0] - 40,
            game_over_pos[1] + 90,
        )
        self.printer.update()
        self.printer.draw(surface, assets.F_JERSEY10_MEDIUM, hee_pos)

        retry_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size(self.interface["initial_menu"]["back_menu"])[0] // 2,
            const.WINDOW_CENTRE[1] + 60,
        )
        quit_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size(self.interface["initial_menu"]["quit"])[0] // 2,
            retry_pos[1] + 50,
        )

        heart_pos = (0, 0)

        retry_color = const.YELLOW if self.selected_option == 'retry' else const.ORANGE
        quit_color = const.YELLOW if self.selected_option == 'quit' else const.ORANGE

        if self.selected_option == "retry":
            heart_pos = (retry_pos[0] - 40, retry_pos[1] + 7)
        else:
            heart_pos = (quit_pos[0] - 40, quit_pos[1] + 7)

        retry_text = assets.F_JERSEY10_MEDIUM.render(self.interface["initial_menu"]["back_menu"], True, retry_color)
        quit_text = assets.F_JERSEY10_MEDIUM.render(self.interface["initial_menu"]["quit"], True, quit_color)
        surface.blit(assets.S_HEART, heart_pos)
        surface.blit(retry_text, retry_pos)
        surface.blit(quit_text, quit_pos)

    def exit(self) -> None:
        pass


def reset_match() -> None:
    import scenes.game
    import entities.player

    # Restaura o player
    statistics = Statistics()
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

    # Salva os dados
    statistics.data["deaths"] += Context.deaths
    statistics.data["life_orbs"] += Context.collected_life_orbs
    statistics.data["damage_orbs"] += Context.collected_damage_orbs
    statistics.data["defense_orbs"] += Context.collected_defense_orbs
    statistics.save_file()

    Context.reset()
