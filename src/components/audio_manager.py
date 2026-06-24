import pygame

class AudioManager:
    audios: dict[str, pygame.mixer.Sound] = {}
    master_volume = 0.5
    music_volume = 0.5
    effects_volume = 0.5

    def load(self, name:str, src: str):
        self.audios[name] = pygame.mixer.Sound(src)

    def set_master_volume(self, value: float):
        self.master_volume = value

    def set_music_volume(self, value: float):
        self.music_volume = value

    def set_effect_volume(self, value: float):
        self.effects_volume = value

    def update_volume(self):
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        for key in self.audios:
            self.audios[key].set_volume(self.effects_volume * self.master_volume)


