import pygame
import core.constants as const

from components.file_manager import FileManager
from typing import Any


class Config(FileManager):
    file_name = "config.json"
    data: dict[str, Any] = {
        "master_volume": 0.5,
        "music_volume": 0.5,
        "effect_volume": 0.5,
        "lang": "pt_br",
        "fullscreen": False,
        "crt": False,
        "chromatic": False,
        "fps": 60,
        "vsync": 1,
    }

    def apply_config(self):
        pygame.display.set_mode(**self.get_window_setup())

    def get_window_setup(self) -> dict[str, Any]:
        flags = pygame.SCALED | pygame.DOUBLEBUF
        window_setup = {
            "size": const.WINDOW_SIZE,
            "flags": pygame.FULLSCREEN | flags if self.data["fullscreen"] else flags,
            "depth": 0,
            "display": 0,
            "vsync": self.data["vsync"],
        }

        return window_setup

