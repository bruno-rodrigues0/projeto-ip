import pygame
import numpy as np

def change_speed(sound: pygame.mixer.Sound, speed: float) -> pygame.mixer.Sound:
    """
    speed < 1.0 = mais lento (e mais grave)
    speed > 1.0 = mais rápido (e mais agudo)
    """
    array = pygame.sndarray.array(sound)  # pega os samples originais

    indices = np.round(np.arange(0, len(array), speed)).astype(int)
    indices = indices[indices < len(array)]

    new_array = array[indices]
    return pygame.sndarray.make_sound(new_array)
