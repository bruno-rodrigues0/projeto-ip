import json
import os
import pygame
import platform
import core.constants as const
from pathlib import Path
from typing import Any


class Config:
    config: dict[str, Any] = {
        "master_volume": 0.5,
        "music_volume": 0.5,
        "effect_volume": 0.5,
        "fullscreen": False,
        "crt": False,
        "chromatic": False,
        "fps": 60,
        "vsync": 1,
    }

    def __init__(self):
        self.load_file()


    def get_config_path(self) -> Path:
        """Descobre a pasta correta dependendo do sistema operacional do jogador"""
        game_name = "ayuwoke_time" # Troque pelo nome do seu jogo
        system = platform.system()

        if system == "Windows":
            base_dir = Path(os.getenv("APPDATA"))
        elif system == "Darwin": # macOS
            base_dir = Path.home() / "Library" / "Application Support"
        else: # Linux e outros
            base_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

        config_dir = base_dir / game_name
        config_dir.mkdir(parents=True, exist_ok=True)

        return config_dir / "config.json"


    def load_file(self):
        try:
            file_path = self.get_config_path()
            with open(file_path, "r") as file:
                data = json.load(file)
                for key in self.config:
                    if key not in data.keys():
                        data[key] = self.config[key]
                self.config = data

        except Exception:
            self.save_file()


    def save_file(self):
        file_path = self.get_config_path()
        with open(file_path, "w") as file:
            json.dump(self.config, file, indent=4)

    def apply_config(self):
        pygame.display.set_mode(**self.get_window_setup())

    def get_window_setup(self) -> dict[str, Any]:
        flags = pygame.SCALED | pygame.DOUBLEBUF
        display = int(os.environ.get('DISPLAY', ':0').split(':')[1].split('.')[0])
        window_setup = {
            "size": const.WINDOW_SIZE,
            "flags": pygame.FULLSCREEN | flags if self.config["fullscreen"] else flags,
            "depth": 0,
            "display": display if display else 0,
            "vsync": self.config["vsync"],
        }

        return window_setup

