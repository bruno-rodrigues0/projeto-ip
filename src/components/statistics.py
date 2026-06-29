
from typing import Any

from components.file_manager import FileManager


class Statistics(FileManager):
    file_name = "statistics.json"
    data: dict[str, Any] = {
        "game_time": 0,
        "deaths": 0,
        "life_orbs": 0,
        "damage_orbs": 0,
        "defense_orbs": 0,
    }
