import pygame
from random import randint

import core.constants as const
import core.assets as assets
import scenes.menu

from entities.attacks.attack01 import Attack01
from core.input import InputBuffer, InputState, Action
from entities.player import Player
from scenes.scene import Scene
from scenes.context import Context
from scenes.states.act import Act, Check, Talk
from components.dialog_printer import DialogPrinter
from scenes.states.attack import Attack
from scenes.states.battle_menu import BattleMenu
from scenes.states.fight import Fight
from scenes.states.item import Item, ItemUsed
from components.animation import AnimationPlayer


MAX_VEL = 200

# Scene objects
MICHAEL_ANIMATION = AnimationPlayer("idle", assets.S_MICHAEL_BATTLE, .3)
PLAYER = Player(
    pygame.transform.scale_by(assets.S_HEART, 0.8),
    const.WINDOW_CENTRE[0],
    const.WINDOW_CENTRE[1],
    100
)

class Game(Scene):
    """
    Main battle loop.
    """

    def enter(self) -> None:
        pygame.mixer.music.unpause()
        self.selected_option = 0
        self.action_option = 0
        self.printer = DialogPrinter(const.BASE_DIALOGS[randint(0, len(const.BASE_DIALOGS) - 1)], 40, 30)
        self.has_collectable = False
        self.initial_time = pygame.time.get_ticks()


    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        global BATTLE_MENU_DIALOGS, dialog_index

        # Pause logic
        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            Context.last_scene = Game # type: ignore
            Context.paused = True
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore


        # Draw
        surface.fill(const.BLACK)

        if Context.battle_state == "fight":
            surface.blit(MICHAEL_ANIMATION.get_frame(), (const.WINDOW_CENTRE[0] - assets.S_MICHAEL_BATTLE[0].get_width() // 2, const.WINDOW_CENTRE[1] - 270))
        else:
            surface.blit(MICHAEL_ANIMATION.get_frame(), (const.WINDOW_CENTRE[0] - assets.S_MICHAEL_BATTLE[0].get_width() // 2, const.WINDOW_CENTRE[1] - 200))
        MICHAEL_ANIMATION.update(dt)

        # Display player's HP
        hp_text = assets.F_JERSEY10.render("HP", True, const.WHITE)
        hp_initial_pos = (
            const.WINDOW_CENTRE[0] - (hp_text.get_size()[0] + 10 + 150 + 77) // 2,
            const.WINDOW_CENTRE[1] + 210,
        )

        hp_yellow_bar_rect = pygame.draw.rect(
            surface,
            const.YELLOW,
            (
                hp_initial_pos[0] + hp_text.get_size()[0] + 10,
                hp_initial_pos[1],
                150 * PLAYER.hp_percent,
                30,
            ),
        )
        hp_red_bar_rect = pygame.draw.rect(
            surface,
            const.RED,
            (
                hp_yellow_bar_rect.right,
                hp_yellow_bar_rect.y,
                150 * (1 - PLAYER.hp_percent),
                30,
            ),
        )

        hp_values_text = assets.F_JERSEY10.render(
            f"{str(PLAYER.current_hp).rjust(3)} / {PLAYER.max_hp}", True, const.WHITE
        )

        for i in range(0, 6, 2):
            surface.blit(assets.S_MENU_OPTIONS[i], (const.WINDOW_CENTRE[0] - 300 + 112 * i, 600))

        if Context.battle_state == "battle_menu":
            BattleMenu.execute(self, surface, dt, action_buffer)
        elif Context.battle_state == "attack":
            Attack.execute(self, surface, dt, action_buffer)
        elif Context.battle_state == "check":
            Check.execute(self, surface, dt, action_buffer)
        elif Context.battle_state == "talk":
            Talk.execute(self, surface, dt, action_buffer)
        elif Context.battle_state == "fight":
            Fight.execute(self, surface, dt, action_buffer, PLAYER)
        elif Context.battle_state == "act":
            Act.execute(self, surface, dt, action_buffer)
        elif Context.battle_state == "item":
            Item.execute(self, surface, dt, action_buffer, PLAYER)
        elif Context.battle_state == "item_used":
            ItemUsed.execute(self, surface, dt, action_buffer)

        surface.blit(hp_text, hp_initial_pos)
        surface.blit(
            hp_values_text, (hp_red_bar_rect.right + 10, hp_red_bar_rect.y)
        )

    def exit(self) -> None:
        pygame.mixer.music.pause()
