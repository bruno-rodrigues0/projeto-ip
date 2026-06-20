import pygame
from components import camera
from components.camera import Camera, camera_follow, camera_to_screen, camera_to_screen_parallax, camera_update
import core.constants as const
import core.assets as assets
import scenes.game
import scenes
import random

from components.dialog_printer import DialogPrinter
from entities.player import Player
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from components.animation import AnimationPlayer
from scenes.context import Context


MAX_VEL = 150

PLAYER_ANIMATION = AnimationPlayer("walk", assets.S_FRISK, .2)
PLAYER = Player(assets.S_FRISK[1], 50, 500, 100)


class IntroDialog(Scene):
    """
    Shows introduction dialog box.
    """

    def enter(self) -> None:
        assets.SFX_ENEMY_ENCOUNTER.set_volume(.4)
        assets.SFX_ENEMY_ENCOUNTER.play()
        assets.SFX_TALKING_LONG.play(-1)
        self.dialog_box = pygame.Surface((const.WINDOW_WIDTH - 90, 150))
        self.dialog_box.fill(const.BLACK)
        self.skip = False
        self.camera = Camera.empty()
        self.camera.offset = pygame.Vector2(0, const.WINDOW_HEIGHT // 2)
        self.camera.motion.position = pygame.Vector2(PLAYER.x - 400, const.WINDOW_HEIGHT // 2)
        self.skip_timeout = 0
        self.text_index = 0
        self.printer = DialogPrinter(
            text=Context.dialog_text[self.text_index],
            char_limit=85,
            typing_delay=10
        )

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:

        # Skip intro logic
        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and not self.skip
        ):
            self.skip = True
            self.skip_timeout = pygame.time.get_ticks()
        elif (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and self.skip
        ):
            self.statemachine.change_state(scenes.game.Game) # type: ignore


        # Dialog
        if not self.printer.finished:
            if action_buffer[Action.START] == InputState.PRESSED:
                self.printer.skip()
                assets.SFX_TALKING_LONG.stop()
            else:
                self.printer.update()

            value = random.randint(0, 1)

            if (
                self.printer.char_index == 0
                and len(self.printer.lines_completed) == len(self.printer.lines_formatted)
            ):
                if value == 1:
                    assets.SFX_HEE_HEE.play()
                else:
                    assets.SFX_AUW.play()
        else:
            assets.SFX_TALKING_LONG.stop()

            if action_buffer[Action.START] == InputState.PRESSED:
                self.text_index += 1
                if self.text_index >= len(Context.dialog_text):
                    self.statemachine.change_state(scenes.game.Game) # type: ignore
                    return
                else:
                    assets.SFX_TALKING_LONG.play(-1)
                    self.printer.change_text(Context.dialog_text[self.text_index], 85)

        camera_update(self.camera, dt)

        # Draw
        assert PLAYER.image is not None
        surface.blit(assets.S_CORRIDOR, camera_to_screen(self.camera, 0, 0))
        surface.blit(PLAYER.image, camera_to_screen(self.camera, PLAYER.x, PLAYER.y))
        surface.blit(assets.S_MICHAEL, camera_to_screen(self.camera, 1500, 350))
        for i in range(4):
            surface.blit(assets.S_PILLAR, camera_to_screen_parallax(self.camera, 200 + 700 * i, 0, 1.5))

        surface.blit(self.dialog_box, (45, 10))
        self.printer.draw(surface, assets.F_JERSEY10, (200, 20))
        surface.blit(pygame.transform.scale_by(assets.S_MICHAEL_CLOSE, .2), (60, 20))


        # Skip intro timeout logic
        elapsed_time = pygame.time.get_ticks()

        if elapsed_time - self.skip_timeout > 3000: # 3s
            self.skip = False

        if self.skip:
            skip_text = assets.F_JERSEY10.render("ESC para pular", True, const.WHITE)
            surface.blit(skip_text, (20, const.WINDOW_HEIGHT - 40))


    def exit(self) -> None:
        assets.SFX_TALKING_LONG.stop()


class Intro(Scene):
    """
    Introduction scene in the last corridor.
    """

    def enter(self) -> None:
        self.dir = "right"
        assets.SFX_UNDERTALE.play()
        self.skip = False
        self.skip_timeout = 0
        self.camera = Camera.empty()
        self.camera.offset = pygame.Vector2(0, const.WINDOW_HEIGHT // 2)
        self.camera.motion.position = pygame.Vector2(0, const.WINDOW_HEIGHT // 2)

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:

        # Skip intro logic
        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and not self.skip
        ):
            self.skip = True
            self.skip_timeout = pygame.time.get_ticks()
        elif (
            action_buffer[Action.OPTIONS] == InputState.PRESSED and self.skip
        ):
            self.statemachine.change_state(scenes.game.Game) # type: ignore


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
        if next_pos[0] <= 0 or next_pos[0] >= assets.S_CORRIDOR.width:
            PLAYER.vx = 0


        # Player walking/idle animation logic
        PLAYER_ANIMATION.update(dt)
        PLAYER.update(dt)
        frisk_frame = PLAYER_ANIMATION.get_frame()

        if PLAYER.x > 400:
            camera_follow(self.camera, PLAYER.x - 400, const.WINDOW_HEIGHT // 2, 35)
        else:
            camera_follow(self.camera, 0, const.WINDOW_HEIGHT // 2, 35)
        camera_update(self.camera, dt)

        if PLAYER.vx == 0:
            PLAYER_ANIMATION.reset()
            assert PLAYER.image is not None
            frisk_frame = PLAYER.image

        if self.dir == "left":
            frisk_frame = pygame.transform.flip(frisk_frame, True, False)

        surface.blit(assets.S_CORRIDOR, camera_to_screen(self.camera, 0, 0))
        surface.blit(frisk_frame, camera_to_screen(self.camera, PLAYER.x, PLAYER.y))
        surface.blit(assets.S_MICHAEL, camera_to_screen(self.camera, 1500, 350))


        # Skip intro timeout logic
        elapsed_time = pygame.time.get_ticks()

        if elapsed_time - self.skip_timeout > 3000: # 3s
            self.skip = False

        if self.skip:
            skip_text = assets.F_JERSEY10.render("ESC para pular", True, const.WHITE)
            surface.blit(skip_text, (20, const.WINDOW_HEIGHT - 40))

        # Pilars
        for i in range(4):
            surface.blit(assets.S_PILLAR, camera_to_screen_parallax(self.camera, 200 + 700 * i, 0, 1.5))

        # Go to dialog
        if PLAYER.x >= 1160:
            Context.dialog_text = [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
            ]

            self.statemachine.change_state(IntroDialog) # type: ignore


    def exit(self) -> None:
        pass
