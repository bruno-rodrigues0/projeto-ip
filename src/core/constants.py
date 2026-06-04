
import pygame

# Pygame constants
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 820
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CENTRE = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

WINDOW_SETUP = {
    "size": WINDOW_SIZE,
    "flags": 0,
    "depth": 0,
    "display": 0,
    "vsync": 1,
}

CAPTION = "Projeto IP"
FPS = 0  # 0 = não capado -> deixa o vsync decidir o melhor frame rate para cada monitor

# Colour constants
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
GREEN = pygame.Color(0, 255, 0)
CYAN = pygame.Color(0, 255, 255)
BLUE = pygame.Color(0, 0, 255)
MAGENTA = pygame.Color(255, 0, 255)
