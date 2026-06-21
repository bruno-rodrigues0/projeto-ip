import pygame

from components.audio_manager import AudioManager
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
S_MICHAEL_CLOSE = pygame.image.load("src/assets/img/michael_close.png")
S_MICHAEL_BATTLE = slice_sheet("src/assets/img/lord.png", 65, 161)
for i, sprite in enumerate(S_MICHAEL_BATTLE):
    S_MICHAEL_BATTLE[i] = pygame.transform.scale_by(sprite, 1.4)
S_MICHAEL_BATTLE.append(S_MICHAEL_BATTLE[1])
S_HEART = pygame.image.load("src/assets/img/heart2.png")


S_ARENA = pygame.Surface((5, 220))
S_ARENA.fill(const.WHITE)
S_CORRIDOR = pygame.transform.scale(
    pygame.image.load("src/assets/img/last_corridor.jpg"),
    (3000, 675),
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
SFX_MASTER = AudioManager()
pygame.mixer.music.load("src/assets/sfx/theme.ogg")
SFX_MASTER.load("move_selection", "src/assets/sfx/move_selection.mp3")
SFX_MASTER.load("select_option", "src/assets/sfx/select-option.mp3")
SFX_MASTER.load("undertale", "src/assets/sfx/undertale.mp3")
SFX_MASTER.load("enemy_encounter", "src/assets/sfx/enemy_encounter.mp3")
SFX_MASTER.load("talking_long", "src/assets/sfx/talking_double.mp3")
SFX_MASTER.load("hee_hee", "src/assets/sfx/hee-hee.mp3")
SFX_MASTER.load("auw", "src/assets/sfx/auw.mp3")
SFX_MASTER.load("damage_item", "src/assets/sfx/damage-item.mp3")
SFX_MASTER.load("healing_item", "src/assets/sfx/healing-item.mp3")
SFX_MASTER.load("damage_taken", "src/assets/sfx/damage-taken.mp3")
SFX_MASTER.load("defense_item", "src/assets/sfx/defense-item.mp3")
SFX_MASTER.load("no_items", "src/assets/sfx/no-items.mp3")

# Load fonts (ttf for web compatibility)
F_JERSEY10_SMALL = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 18)
F_JERSEY10 = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 28)
F_JERSEY10_MEDIUM = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 36)
F_JERSEY10_LARGE = pygame.font.Font("src/assets/fonts/Jersey10-Regular.ttf", 80)

print("Loaded assets")
