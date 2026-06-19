import pygame

import core.constants as const
from utilities.sprite import slice_sheet

# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load("src/assets/icon.png")
COIN_SPRITE = pygame.image.load("src/assets/img/coin.png")

FRISK_SPRITE = slice_sheet("src/assets/img/frisk.png", 34, 58)
for i, frame in enumerate(FRISK_SPRITE):
    FRISK_SPRITE[i] = pygame.transform.scale_by(frame, 1.4)
MICHEAL_SPRITE = pygame.transform.scale_by(
    pygame.image.load("src/assets/img/michael.png"),
    .4
)

HEART_SPRITE = pygame.image.load("src/assets/img/heart2.png")

MENU_SPRITE = pygame.image.load("src/assets/img/menu_sprite.png")
ARENA_SPRITE = pygame.Surface((5, 280))
ARENA_SPRITE.fill(const.WHITE)
LAST_CORRIDOR = pygame.transform.scale(
    pygame.image.load("src/assets/img/last_corridor.jpg"),
    (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
)

# Load audio (ogg for web compatibility)
DEBUG_THEME = pygame.mixer.music.load("src/assets/sfx/theme.ogg")
UNDERTALE_SOUND = pygame.mixer.Sound("src/assets/sfx/undertale.mp3")
ENEMY_ENCOUNTER_SOUND = pygame.mixer.Sound("src/assets/sfx/enemy_encounter.mp3")
TALKING_SOUND = pygame.mixer.Sound("src/assets/sfx/talking_double.mp3")
HEE_HEE_SOUND = pygame.mixer.Sound("src/assets/sfx/hee-hee.mp3")
AUW_SOUND = pygame.mixer.Sound("src/assets/sfx/auw.mp3")

# Load fonts (ttf for web compatibility)
DEBUG_FONT_SMALL = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 18)
DEBUG_FONT = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 28)
DEBUG_FONT_MEDIUM = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 36)

print("Loaded assets")
