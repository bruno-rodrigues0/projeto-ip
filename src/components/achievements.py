import json

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

    def load_file(self) -> None:
        try:
            file_path = self.get_data_path()
            with open(file_path, "r") as file:
                data = json.load(file)
                for key in data:
                    if key not in list(self.data.keys()):
                        data.remove(key)

                for key in self.data:
                    if key not in data.keys():
                        data[key] = self.data[key]

                self.data = data

        except Exception:
            self.save_file()
