import pygame

import core.constants as const

# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load("src/assets/icon.png")
MENU_SPRITE = pygame.image.load("src/assets/img/menu_sprite.png")
HEART_SPRITE = pygame.image.load("src/assets/img/heart2.png")
COIN_SPRITE = pygame.image.load("src/assets/img/coin.png")
ARENA_SPRITE = pygame.Surface((5, 280))
ARENA_SPRITE.fill(const.WHITE)

# Load audio (ogg for web compatibility)
DEBUG_THEME = pygame.mixer.music.load("src/assets/sfx/theme.ogg")

# Load fonts (ttf for web compatibility)
DEBUG_FONT_SMALL = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 18)
DEBUG_FONT = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 28)
DEBUG_FONT_MEDIUM = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 36)

print("Loaded assets")
