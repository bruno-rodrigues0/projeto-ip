import pygame
import core.constants as const
import core.assets as assets
import scenes

from components.camera import Camera, camera_follow, camera_to_screen, camera_to_screen_parallax, camera_update
from components.config import Config
from components.dialog_printer import DialogPrinter, DialogConfig
from entities.player import Player
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from components.animation import AnimationPlayer
from scenes.context import Context, reset_match
from utilities import languages


MAX_VEL = 150

PLAYER_ANIMATION = AnimationPlayer("walk", assets.S_FRISK, .2)
PLAYER = Player(assets.S_FRISK[1], 50, 500, 100)
FLOWEY_SPRITE = assets.S_FLOWEY[0]


class FloweyDialog(Scene):
    """Mostra a caixa de diálogo da sequência secreta do Flowey."""

    def enter(self) -> None:
        assets.SFX_MASTER.audios["enemy_encounter"].set_volume(.4)
        assets.SFX_MASTER.audios["enemy_encounter"].play()
        assets.SFX_MASTER.audios["talking_long"].play(-1)

        self.dialog_box = pygame.Surface((const.WINDOW_WIDTH - 90, 150))
        self.dialog_box.fill(const.BLACK)

        self.laugh_time = 0
        self.fade_alpha = 0
        self.camera = Camera.empty()
        self.camera.offset = pygame.Vector2(0, const.WINDOW_HEIGHT // 2)
        self.camera.motion.position = pygame.Vector2(PLAYER.x - 400, const.WINDOW_HEIGHT // 2)

        self.config = Config()
        self.lang_dialog = languages.DIALOGS[self.config.data["lang"]]
        self.printer = DialogPrinter.sequence(
            self.lang_dialog["flowey_dialog"],
            DialogConfig.INTRO,
        )

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        if action_buffer[Action.A] == InputState.PRESSED:
            advanced = self.printer.advance()
            if advanced:
                assets.SFX_MASTER.audios["talking_long"].play(-1)
            else:
                assets.SFX_MASTER.audios["talking_long"].stop()

        if not self.printer.page_finished:
            self.printer.update()
        else:
            assets.SFX_MASTER.audios["talking_long"].stop()

        camera_update(self.camera, dt)

        assert PLAYER.image is not None
        visible_area = pygame.Rect(self.camera.motion.position.x, 0, const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
        surface.blit(assets.S_CORRIDOR, (0, 0), visible_area)
        surface.blit(PLAYER.image, camera_to_screen(self.camera, PLAYER.x, PLAYER.y))
        surface.blit(assets.S_FLOWEY[0], camera_to_screen(self.camera, 1500, 430))
        if surface.get_rect().colliderect(assets.S_PILLAR.get_rect()):
            for i in range(4):
                surface.blit(assets.S_PILLAR, camera_to_screen_parallax(self.camera, 200 + 700 * i, 0, 1.5))

        surface.blit(self.dialog_box, (45, 10))
        self.printer.draw(surface, assets.F_JERSEY10, (200, 20))
        surface.blit(assets.S_FLOWEY_NICE[0], (70, 45))

        if self.printer.finished:
            if self.laugh_time == 0:
                assets.SFX_MASTER.audios["flowey_laugh"].play()
            self.laugh_time += dt

            fade_surface = pygame.Surface((surface.get_width(), surface.get_height()))
            fade_surface.fill(const.BLACK)
            fade_surface.set_alpha(self.fade_alpha)

            surface.blit(fade_surface, (0, 0))
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + int(self.laugh_time))
            else:
                reset_match()
                self.statemachine.change_state(scenes.menu.Menu) # type: ignore


    def exit(self) -> None:
        PLAYER.x = 50
        PLAYER.y = 500
        assets.SFX_MASTER.audios["talking_long"].stop()


class FloweyIntro(Scene):
    """Cena secreta baseada no intro, com o player andando pelo corredor e o Flowey no fim."""

    def enter(self) -> None:
        self.dir = "right"
        assets.SFX_MASTER.audios["undertale"].play()
        self.config = Config()
        self.lang_inter = languages.INTERFACE[self.config.data["lang"]]
        self.lang_dialog = languages.DIALOGS[self.config.data["lang"]]
        self.skip_timeout = 0
        self.camera = Camera.empty()
        self.camera.offset = pygame.Vector2(0, const.WINDOW_HEIGHT // 2)
        self.camera.motion.position = pygame.Vector2(0, const.WINDOW_HEIGHT // 2)

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
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
        if next_pos[0] <= 0 or next_pos[0] >= assets.S_CORRIDOR.get_width():
            PLAYER.vx = 0

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

        visible_area = pygame.Rect(self.camera.motion.position.x, 0, const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
        surface.blit(assets.S_CORRIDOR, (0, 0), visible_area)
        surface.blit(frisk_frame, camera_to_screen(self.camera, PLAYER.x, PLAYER.y))
        surface.blit(assets.S_FLOWEY[0], camera_to_screen(self.camera, 1500, 430))

        for i in range(4):
            if surface.get_rect().colliderect(assets.S_PILLAR.get_rect()):
                surface.blit(assets.S_PILLAR, camera_to_screen_parallax(self.camera, 200 + 700 * i, 0, 1.5))

        if PLAYER.x >= 1160:
            Context.dialog_text = self.lang_dialog["intro"]
            self.statemachine.change_state(FloweyDialog)  # type: ignore

    def exit(self) -> None:
        pass

