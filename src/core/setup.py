import os
import pygame

# Força a janela do Pygame a abrir e se recriar sempre no centro da tela
os.environ['SDL_VIDEO_CENTERED'] = '1'

from components.config import Config


pygame.init()
pygame.joystick.init()
config = Config()
config.load_file()
window_setup = config.get_window_setup()

window = pygame.display.set_mode(**window_setup)

clock = pygame.time.Clock()

print("Setup complete")
