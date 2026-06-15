import pygame

from utilities.sprite import slice_sheet

# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load("src/assets/icon.png")
DEBUG_SPRITE = pygame.image.load("src/assets/img/dvd_logo.png")
DEBUG_FRAMES = slice_sheet("src/assets/img/impossible_spin.png", 64, 64)
PLAYER_SPRITE = pygame.image.load("src/assets/img/dvd_logo.png").convert_alpha()
COIN_SPRITE = pygame.image.load("src/assets/img/dvd_logo.png")

# Load audio (ogg for web compatibility)
DEBUG_THEME = pygame.mixer.music.load("src/assets/sfx/theme.ogg")

# Load fonts (ttf for web compatibility)
DEBUG_FONT = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 10)

print("Loaded assets")
