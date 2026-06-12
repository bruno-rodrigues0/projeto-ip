import pygame

import core.constants as const
import core.assets as asset
from core.input import InputBuffer, InputState, Action
from components.object import SimulatedObject

from scenes import scene
from scenes.scene import Scene
import scenes.menu

MAX_X = const.WINDOW_WIDTH - asset.PLAYER_SPRITE.get_width()
MAX_Y = const.WINDOW_HEIGHT - asset.PLAYER_SPRITE.get_height()
MAX_VEL = 100

PLAYER_OBJECT = SimulatedObject(0, 0, 0, 0, 0, 0)
COIN_OBJECT = SimulatedObject(600, 300, 0, 0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, player_object, x_inicial, y_inicial):
        super().__init__()
        
        self.image = image.convert_alpha()
        self.object = player_object
        
        self.rect = self.image.get_rect(topleft=(x_inicial, y_inicial))

    def update(self, dt):
        self.object.update(dt)
        self.rect = self.image.get_rect(topleft=(self.object.x, self.object.y))



PLAYER = Player(asset.PLAYER_SPRITE, PLAYER_OBJECT, 0, 0)
COIN = Player(asset.COIN_SPRITE, COIN_OBJECT, 600, 300)

class Game(Scene):
    def enter(self) -> None:
        pygame.mixer.music.play(-1)

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
        mouse_buffer: InputBuffer
    ) -> None:

        # Go to menu
        if (action_buffer[Action.A] == InputState.PRESSED):
            self.statemachine.change_state(scenes.menu.Menu)

        # Move in X axis
        if (
            action_buffer[Action.RIGHT] == InputState.HELD
            and action_buffer[Action.LEFT] == InputState.NOTHING
        ):
            PLAYER.object.vx = MAX_VEL
        elif (
            action_buffer[Action.LEFT] == InputState.HELD
            and action_buffer[Action.RIGHT] == InputState.NOTHING
        ):
            PLAYER.object.vx = -MAX_VEL
        else:
            PLAYER.object.vx = 0

        # Move in Y axis
        if (
            action_buffer[Action.UP] == InputState.HELD
            and action_buffer[Action.DOWN] == InputState.NOTHING
        ):
            PLAYER.object.vy = -MAX_VEL
        elif (
            action_buffer[Action.DOWN] == InputState.HELD
            and action_buffer[Action.UP] == InputState.NOTHING
        ):
            PLAYER.object.vy = MAX_VEL
        else:
            PLAYER.object.vy = 0

        collided = pygame.sprite.collide_rect(PLAYER, COIN)

        PLAYER.update(dt)
        surface.fill(const.MAGENTA)
        surface.blit(asset.PLAYER_SPRITE, PLAYER.object.get_pos())
        if not collided:
            surface.blit(asset.COIN_SPRITE, COIN.object.get_pos())

    def exit(self) -> None:
        pygame.mixer.music.stop()
