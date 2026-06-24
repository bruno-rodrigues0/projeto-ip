import pygame
import sys

from pathlib import Path

# Pygame constants
WINDOW_WIDTH = 1200 #! CHANGE TO 1920
WINDOW_HEIGHT = 675 #! CHANGE TO 1080
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CENTRE = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    ROOT_DIR = Path(sys._MEIPASS)
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent

CAPTION = "Ayuwoke Time CINmulator"

BASE_DIALOGS = [
  "É o Ayuwoke. Hee-Hee",
  "Você sente que vai passar por um tempo ruim.",
  "Michael Jackson faz Moonwalk enquanto olha pra você. É assustador."
]

# Colour constants
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
GRAY = pygame.Color(16, 16, 16)
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
ORANGE = pygame.Color(233, 117, 34)
GREEN = pygame.Color(0, 255, 0)
CYAN = pygame.Color(0, 255, 255)
BLUE = pygame.Color(0, 0, 255)
MAGENTA = pygame.Color(255, 0, 255)

print("Loaded constants")
