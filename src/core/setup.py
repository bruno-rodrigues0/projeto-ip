import pygame

from components.config import Config
import core.constants as const


pygame.init()
config = Config()
config.load_file()
window_setup = config.get_window_setup()

window = pygame.display.set_mode(**window_setup)

clock = pygame.time.Clock()

print("Setup complete")
