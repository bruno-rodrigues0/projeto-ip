import json
import pygame
import core.constants as const
from typing import Any


class Config:
    config: dict[str, Any] = {
        "master_volume": 0.5,
        "fullscreen": False,
        "fps": 60,
        "vsync": 1,
    }

    def __init__(self):
        self.load_file()

    def load_file(self):
        try:
            with open("src/data/config.json", "r") as file:
                data = json.load(file)
                self.config = data
        except Exception:
            print("No config file.")

    def save_file(self):
        with open("src/data/config.json", "w") as file:
            json.dump(self.config, file, indent=4)

    def apply_config(self):
        pygame.display.set_mode(**self.get_window_setup())

    def get_window_setup(self) -> dict[str, Any]:
        window_setup = {
            "size": const.WINDOW_SIZE,
            "flags": pygame.FULLSCREEN if self.config["fullscreen"] else 0,
            "depth": 0,
            "display": 0,
            "vsync": self.config["vsync"],
        }

        return window_setup

