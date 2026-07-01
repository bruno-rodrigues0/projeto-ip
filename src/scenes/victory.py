import pygame
from components.achievements import AchievementsManager
from components.config import Config
import scenes.menu
import core.constants as const
import core.assets as assets

from scenes.scene import Scene
from scenes.context import Context
from core.input import InputBuffer, InputState, Action
from components.statistics import Statistics
from utilities import languages


class Victory(Scene):
    def enter(self) -> None:
        self.config = Config()
        self.selected_option = 'retry'
        self.interface = languages.INTERFACE[self.config.data["lang"]]


        achievements = AchievementsManager()
        for achievement in achievements.data:
            if not achievements.data[achievement]:
                match achievement:
                    case "you_are_god":
                        if not Context.has_taken_damage and len(Context.used_items) == 0:
                            achievements.data[achievement] = True
                    case "defeat_michael":
                        achievements.data[achievement] = True
                    case "no_damage":
                        if not Context.has_taken_damage:
                            achievements.data[achievement] = True
                    case "no_item":
                        if len(Context.used_items) == 0:
                            achievements.data[achievement] = True
        achievements.save_file()


        final_time = pygame.time.get_ticks()
        session_time = (final_time - Context.start_time) / 1000.0
        min = session_time < 3600
        session_time = session_time / 60 if session_time < 3600 else session_time / 3600
        session_time = f"{session_time:.1f} {'min' if min else 'h'}"
        self.score = {
            self.interface["victory"]["session_time"]: session_time,
            self.interface["stats"]["life_orbs"]: Context.collected_life_orbs,
            self.interface["stats"]["defense_orbs"]: Context.collected_defense_orbs,
            self.interface["stats"]["damage_orbs"]: Context.collected_damage_orbs,
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

        surface.fill(const.BLACK)

        title = assets.F_JERSEY10_LARGE.render(self.interface["victory"]["title"], True, const.YELLOW)
        title_pos = (
            const.WINDOW_CENTRE[0] - title.get_width() // 2,
            80,
        )
        surface.blit(title, title_pos)

        subtitle = assets.F_JERSEY10_MEDIUM.render(self.interface["victory"]["subtitle"], True, const.WHITE)
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

        heart_pos = (0, 0)
        retry_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size(self.interface["initial_menu"]["back_menu"])[0] // 2,
            const.WINDOW_HEIGHT - 130,
        )
        quit_pos = (
            const.WINDOW_CENTRE[0] - assets.F_JERSEY10_MEDIUM.size(self.interface["initial_menu"]["quit"])[0] // 2,
            retry_pos[1] + 50,
        )


        retry_color = const.YELLOW if self.selected_option == 'retry' else const.ORANGE
        quit_color = const.YELLOW if self.selected_option == 'quit' else const.ORANGE

        retry_text = assets.F_JERSEY10_MEDIUM.render(self.interface["initial_menu"]["back_menu"], True, retry_color)
        quit_text = assets.F_JERSEY10_MEDIUM.render(self.interface["initial_menu"]["quit"], True, quit_color)

        if self.selected_option == "retry":
            heart_pos = (retry_pos[0] - 40, retry_pos[1] + 7)
        else:
            heart_pos = (quit_pos[0] - 40, quit_pos[1] + 7)

        surface.blit(assets.S_HEART, heart_pos)
        surface.blit(retry_text, retry_pos)
        surface.blit(quit_text, quit_pos)

    def exit(self) -> None:
        pass


def reset_match() -> None:
    import scenes.game
    import entities.player

    statistics = Statistics()

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

    # Salva os dados
    statistics.data["deaths"] += Context.deaths
    statistics.data["life_orbs"] += Context.collected_life_orbs
    statistics.data["damage_orbs"] += Context.collected_damage_orbs
    statistics.data["defense_orbs"] += Context.collected_defense_orbs
    statistics.save_file()

    # Zera os contadores da partida
    Context.collected_life_orbs = 0
    Context.collected_defense_orbs = 0
    Context.collected_damage_orbs = 0
    Context.deaths = 0
    Context.used_items = []
    Context.battle_state = "battle_menu"
