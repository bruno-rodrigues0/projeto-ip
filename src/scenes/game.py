import pygame
from random import randint

from components.config import Config
import core.constants as const
import core.assets as assets
import scenes.menu

from core.input import InputBuffer, InputState, Action
from entities.player import Player
from scenes.scene import Scene
from scenes.context import Context
from scenes.states.act import Act, Check, Talk
from components.dialog_printer import DialogPrinter, DialogConfig
from scenes.states.attack import Attack
from scenes.states.battle_menu import BattleMenu
from scenes.states.fight import Fight
from scenes.states.item import Item, ItemUsed
from components.animation import AnimationPlayer
from utilities import languages


MAX_VEL = 200

MICHAEL_ANIMATION = AnimationPlayer("idle", assets.S_MICHAEL_BATTLE, .3)
PLAYER = Player(
    pygame.transform.scale_by(assets.S_HEART, 0.8),
    const.WINDOW_CENTRE[0] - 5,
    const.WINDOW_CENTRE[1] + 60,
    100
)

# Mapa de estado → classe do subestado, usado para despachar on_enter e execute
_STATE_MAP = {
    "battle_menu": BattleMenu,
    "attack":      Attack,
    "act":         Act,
    "check":       Check,
    "talk":        Talk,
    "fight":       Fight,
    "item":        Item,
    "item_used":   ItemUsed,
}


class Game(Scene):
    """Main battle loop."""

    def enter(self) -> None:
        pygame.mixer.music.unpause()
        self.config = Config()
        self.lang_dialog = languages.DIALOGS[self.config.config["lang"]]
        self.lang_inter = languages.INTERFACE[self.config.config["lang"]]
        self.selected_option = 0
        self.action_option = 0
        self.has_collectable = False
        self.initial_time = pygame.time.get_ticks()
        self.player = PLAYER  # referência para subestados acessarem via game.player

        self.printer = DialogPrinter.simple(
            self.lang_dialog["fight_menu"][randint(0, len(self.lang_dialog["fight_menu"]) - 1)],
            DialogConfig.BATTLE,
        )

        self._prev_battle_state = Context.battle_state
        _STATE_MAP[Context.battle_state].enter(self)

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        # Pause
        if action_buffer[Action.OPTIONS] == InputState.PRESSED:
            Context.last_scene = Game  # type: ignore
            Context.paused = True
            self.statemachine.change_state(scenes.menu.Menu)

        # Detecta mudança de subestado e dispara on_enter UMA VEZ
        if Context.battle_state != self._prev_battle_state:
            self._prev_battle_state = Context.battle_state
            _STATE_MAP[Context.battle_state].enter(self)

        # Draw base
        surface.fill(const.BLACK)

        michael_y = const.WINDOW_CENTRE[1] - (270 if Context.battle_state == "fight" else 200)
        surface.blit(
            MICHAEL_ANIMATION.get_frame(),
            (const.WINDOW_CENTRE[0] - assets.S_MICHAEL_BATTLE[0].get_width() // 2, michael_y)
        )
        MICHAEL_ANIMATION.update(dt)

        for i in range(0, 6, 2):
            surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        state = Context.battle_state
        match state:
            case "battle_menu":
                BattleMenu.execute(self, surface, dt, action_buffer)
            case "attack":
                Attack.execute(self, surface, dt, action_buffer)
            case "check":
                Check.execute(self, surface, dt, action_buffer)
            case "talk":
                Talk.execute(self, surface, dt, action_buffer)
            case "fight":
                Fight.execute(self, surface, dt, action_buffer, PLAYER)
            case "act":
                Act.execute(self, surface, dt, action_buffer)
            case "item":
                Item.execute(self, surface, dt, action_buffer)
            case "item_used":
                ItemUsed.execute(self, surface, dt, action_buffer)

        draw_hp(surface, PLAYER)

    def exit(self) -> None:
        pygame.mixer.music.pause()


def draw_hp(surface: pygame.Surface, player: Player) -> None:
    hp_text = assets.F_JERSEY10.render("HP", True, const.WHITE)
    hp_initial_pos = (
        const.WINDOW_CENTRE[0] - (hp_text.get_size()[0] + 10 + 150 + 77) // 2,
        const.WINDOW_CENTRE[1] + 210,
    )
    hp_yellow = pygame.draw.rect(
        surface, const.YELLOW,
        (hp_initial_pos[0] + hp_text.get_size()[0] + 10, hp_initial_pos[1], 150 * player.hp_percent, 30),
    )
    hp_red = pygame.draw.rect(
        surface, const.RED,
        (hp_yellow.right, hp_yellow.y, 150 * (1 - player.hp_percent), 30),
    )
    hp_values = assets.F_JERSEY10.render(f"{str(player.current_hp).rjust(3)} / {player.max_hp}", True, const.WHITE)
    surface.blit(hp_text, hp_initial_pos)
    surface.blit(hp_values, (hp_red.right + 10, hp_red.y))
