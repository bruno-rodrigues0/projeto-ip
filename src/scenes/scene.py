import pygame
import core.input as input

from components.statemachine import State
from abc import abstractmethod


class Scene(State):
    """
    Scene abstract class.
    """

    @abstractmethod
    def enter(self) -> None: ...

    @abstractmethod
    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: input.InputBuffer,
    ) -> None: ...

    @abstractmethod
    def exit(self) -> None: ...
