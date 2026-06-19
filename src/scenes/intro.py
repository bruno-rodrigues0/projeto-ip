import pygame
import core.constants as const
import core.assets as asset
import scenes
import random

from components.dialog_printer import DialogPrinter
from entities.player import Player
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from components.animation import AnimationPlayer
from scenes.context import Context

MAX_VEL = 150

PLAYER_ANIMATION = AnimationPlayer("walk", asset.FRISK_SPRITE, .2)
PLAYER = Player(asset.FRISK_SPRITE[1], 50, 500, 100)


class IntroDialog(Scene):
    def enter(self) -> None:
        asset.ENEMY_ENCOUNTER_SOUND.set_volume(.5)
        asset.ENEMY_ENCOUNTER_SOUND.play()
        asset.TALKING_SOUND.play(-1)
        self.dialog_box = pygame.Surface((const.WINDOW_WIDTH - 90, 150))
        self.dialog_box.fill(const.BLACK)
        self.skip = False
        self.skip_timeout = 0
        self.text_index = 0
        self.printer = DialogPrinter(
            text=Context.dialog_text[self.text_index],
            char_limit=100,
            typing_delay=10
        )

    def execute(
        self, 
        surface: pygame.Surface, 
        dt: float,
        action_buffer: InputBuffer
    ) -> None:

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and not self.skip
        ):
            self.skip = True
            self.skip_timeout = pygame.time.get_ticks()
        elif (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and self.skip
        ):
            self.statemachine.change_state(scenes.game.Game) # type: ignore


        assert PLAYER.image is not None
        surface.blit(asset.LAST_CORRIDOR, (0, 0))
        surface.blit(PLAYER.image, (PLAYER.x, PLAYER.y))
        surface.blit(asset.MICHEAL_SPRITE, (800, 350))
        surface.blit(self.dialog_box, (45, 10))

        if not self.printer.finished:
            if action_buffer[Action.START] == InputState.PRESSED:
                self.printer.skip()
                asset.TALKING_SOUND.stop()
            else:
                self.printer.update()

            value = random.randint(0, 1)

            if (
                self.printer.char_index == 0
                and len(self.printer.lines_completed) == len(self.printer.lines_formatted)
            ):
                if value == 1:
                    asset.HEE_HEE_SOUND.play()
                else:
                    asset.AUW_SOUND.play()
        else:
            asset.TALKING_SOUND.stop()

            if action_buffer[Action.START] == InputState.PRESSED:
                self.text_index += 1
                if self.text_index >= len(Context.dialog_text):
                    self.statemachine.change_state(scenes.game.Game) # type: ignore
                    return
                else:
                    asset.TALKING_SOUND.play(-1)
                    self.printer.change_text(Context.dialog_text[self.text_index], 100)

        self.printer.draw(surface, asset.DEBUG_FONT, (60, 20))

        elapsed_time = pygame.time.get_ticks()

        if elapsed_time - self.skip_timeout > 3000: # 3s
            self.skip = False

        if self.skip:
            skip_text = asset.DEBUG_FONT.render("ESC para pular", True, const.WHITE)
            surface.blit(skip_text, (20, const.WINDOW_HEIGHT - 40))

    def exit(self) -> None:
        pass


class Intro(Scene):
    def enter(self) -> None:
        self.dir = "right"
        asset.UNDERTALE_SOUND.play()
        self.skip = False
        self.skip_timeout = 0

    def execute(
        self, 
        surface: pygame.Surface, 
        dt: float, 
        action_buffer: InputBuffer
    ) -> None:

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and not self.skip
        ):
            self.skip = True
            self.skip_timeout = pygame.time.get_ticks()
        elif (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and self.skip
        ):
            self.statemachine.change_state(scenes.game.Game) # type: ignore

        # Go to dialog
        if PLAYER.x >= 700:
            Context.dialog_text = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", "asdak dlakjd adad aod f asjhf sjlh fahsd fasjh fasjhf ash."]
            self.statemachine.change_state(IntroDialog) # type: ignore

        # Move in X axis
        if (
            action_buffer[Action.RIGHT] == InputState.HELD
            and action_buffer[Action.LEFT] == InputState.NOTHING
        ):
            self.dir = "right"
            PLAYER.vx = MAX_VEL
        elif (
            action_buffer[Action.LEFT] == InputState.HELD
            and action_buffer[Action.RIGHT] == InputState.NOTHING
        ):
            self.dir = "left"
            PLAYER.vx = -MAX_VEL
        else:
            PLAYER.vx = 0

        next_pos = PLAYER.get_next_pos(dt)
        if next_pos[0] <= 0 or next_pos[0] >= const.WINDOW_WIDTH:
            PLAYER.vx = 0


        # Player walking/idle animation logic
        PLAYER_ANIMATION.update(dt)
        PLAYER.update(dt)
        surface.blit(asset.LAST_CORRIDOR, (0, 0))
        frisk_frame = PLAYER_ANIMATION.get_frame() 

        if PLAYER.vx == 0:
            PLAYER_ANIMATION.reset()
            assert PLAYER.image is not None
            frisk_frame = PLAYER.image

        if self.dir == "left":
            frisk_frame = pygame.transform.flip(frisk_frame, True, False)

        
        surface.blit(frisk_frame, (PLAYER.x, PLAYER.y))
        surface.blit(asset.MICHEAL_SPRITE, (800, 350))

        # Skip intro timeout logic
        elapsed_time = pygame.time.get_ticks()

        if elapsed_time - self.skip_timeout > 3000: # 3s
            self.skip = False

        if self.skip:
            skip_text = asset.DEBUG_FONT.render("ESC para pular", True, const.WHITE)
            surface.blit(skip_text, (20, const.WINDOW_HEIGHT - 40))

    def exit(self) -> None:
        pass
