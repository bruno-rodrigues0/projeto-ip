from components.file_manager import FileManager

class AchievementsManager(FileManager):
    file_name = "achievements.json"
    data = {
        "you_are_god": False,
        "defeat_michael": False,
        "no_damage": False,
        "no_item": False,
        "shit": False,
    }
