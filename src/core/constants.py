import pygame


# Pygame constants
WINDOW_WIDTH = 1200 #! CHANGE TO 1920
WINDOW_HEIGHT = 675 #! CHANGE TO 1080
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CENTRE = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

WINDOW_SETUP = {
    "size": WINDOW_SIZE,
    "flags": 0,
    "depth": 0,
    "display": 0,
    "vsync": 1,
}

CAPTION = "My New Pygame Project"
FPS = 0  # 0 = Uncapped -> let VSYNC decide best tick speed if enabled
MAX_DT = 1/FPS if FPS else 1/60

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
