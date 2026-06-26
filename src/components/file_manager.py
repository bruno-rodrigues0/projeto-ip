import os
import json
import platform

from abc import ABC
from pathlib import Path
from typing import Any


class FileManager(ABC):
    game_name: str = "ayuwoke_time"
    file_name: str
    data: dict[str, Any]

    def __init__(self) -> None:
        self.load_file()

    def get_data_path(self) -> Path:
        system = platform.system()

        if system == "Windows":
            base_dir = Path(os.getenv("APPDATA"))
        elif system == "Darwin": # macOS
            base_dir = Path.home() / "Library" / "Application Support"
        else: # Linux
            base_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

        config_dir = base_dir / self.game_name
        config_dir.mkdir(parents=True, exist_ok=True)

        return config_dir / self.file_name

    def save_file(self) -> None:
        file_path = self.get_data_path()
        with open(file_path, "w") as file:
            json.dump(self.data, file, indent=4)


    def load_file(self) -> None:
        try:
            file_path = self.get_data_path()
            with open(file_path, "r") as file:
                data = json.load(file)
                for key in self.data:
                    if key not in data.keys():
                        data[key] = self.data[key]
                self.data = data

        except Exception:
            self.save_file()



