import pygame

import core.constants as const
from utilities.sprite import slice_sheet

# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load("src/assets/icon.png")


S_COIN = pygame.image.load("src/assets/img/coin.png")
S_FRISK = slice_sheet("src/assets/img/frisk.png", 34, 58)
for i, frame in enumerate(S_FRISK):
    S_FRISK[i] = pygame.transform.scale_by(frame, 1.4)
S_MICHAEL = pygame.transform.scale_by(
    pygame.image.load("src/assets/img/michael.png"), 0.4
)
S_HEART = pygame.image.load("src/assets/img/heart2.png")


S_MENU = pygame.image.load("src/assets/img/menu_sprite.png")
S_ARENA = pygame.Surface((5, 280))
S_ARENA.fill(const.WHITE)
S_CORRIDOR = pygame.transform.scale(
    pygame.image.load("src/assets/img/last_corridor.jpg"),
    (const.WINDOW_WIDTH * 3, const.WINDOW_HEIGHT),
)
S_MENU_OPTIONS = slice_sheet("src/assets/img/menu_options.png", 110, 42)
for i, menu_option in enumerate(S_MENU_OPTIONS):
    S_MENU_OPTIONS[i] = pygame.transform.scale_by(menu_option, 1.4)
S_ATTACK_BAR = pygame.image.load("src/assets/img/attack_bar.png")
S_PILLAR = pygame.image.load("src/assets/img/pillar.png")
S_PILLAR = pygame.transform.scale(
    S_PILLAR,
    (
        S_PILLAR.get_width() * (const.WINDOW_WIDTH * 2.5 / const.WINDOW_HEIGHT),
        const.WINDOW_HEIGHT + 300,
    ),
)

# Load audio (ogg for web compatibility)
pygame.mixer.music.load("src/assets/sfx/theme.ogg")
SFX_UNDERTALE = pygame.mixer.Sound("src/assets/sfx/undertale.mp3")
SFX_ENEMY_ENCOUNTER = pygame.mixer.Sound("src/assets/sfx/enemy_encounter.mp3")
SFX_TALKING_LONG = pygame.mixer.Sound("src/assets/sfx/talking_double.mp3")
SFX_HEE_HEE = pygame.mixer.Sound("src/assets/sfx/hee-hee.mp3")
SFX_AUW = pygame.mixer.Sound("src/assets/sfx/auw.mp3")
SFX_DAMAGE_ITEM = pygame.mixer.Sound("src/assets/sfx/damage-item.mp3")
SFX_HEALING_ITEM = pygame.mixer.Sound("src/assets/sfx/healing-item.mp3")
SFX_DAMAGE_TAKEN = pygame.mixer.Sound("src/assets/sfx/damage-taken.mp3")
SFX_DEFENSE_ITEM = pygame.mixer.Sound("src/assets/sfx/defense-item.mp3")
SFX_NO_ITEMS = pygame.mixer.Sound("src/assets/sfx/no-items.mp3")

# Load fonts (ttf for web compatibility)
F_JERSEY10_SMALL = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 18)
F_JERSEY10 = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 28)
F_JERSEY10_MEDIUM = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 36)

print("Loaded assets")
