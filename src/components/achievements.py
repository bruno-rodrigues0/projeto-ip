import pygame

from components.file_manager import FileManager

class AchievementsManager(FileManager):
    file_name = "achievements.json"
    data = {
        "you_are_god": False,
        "defeat_michael": False,
        "defeat_chapolin": False,
        "no_item": False,
        "shit": False,
    }
