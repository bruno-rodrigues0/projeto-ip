import pygame
from pygame.mixer_music import set_volume

class AudioManager:
    audios: dict[str, pygame.mixer.Sound] = {}
    master_volume = 0.5

    def load(self, name:str, src: str):
        self.audios[name] = pygame.mixer.Sound(src)

    def set_master_volume(self, value: float):
        self.master_volume = value
        pygame.mixer.music.set_volume(self.master_volume)
        for key in self.audios:
            self.audios[key].set_volume(self.master_volume)

