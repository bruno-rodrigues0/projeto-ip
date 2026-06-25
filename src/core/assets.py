import pygame
import core.constants as const

from components.audio_manager import AudioManager
from core.constants import ROOT_DIR
from utilities.sprite import slice_sheet

# Load sprites (png, webp or jpg for web compatibility)
ICON = pygame.image.load(ROOT_DIR / "src/assets/icon.png")


S_COIN = pygame.image.load(ROOT_DIR / "src/assets/img/coin.png").convert_alpha()
S_FRISK = slice_sheet(ROOT_DIR / "src/assets/img/frisk.png", 34, 58)
for i, frame in enumerate(S_FRISK):
    S_FRISK[i] = pygame.transform.scale_by(frame, 1.4).convert_alpha()
S_MICHAEL = pygame.transform.scale_by(
    pygame.image.load(ROOT_DIR / "src/assets/img/michael.png"), 0.4
).convert_alpha()
S_MICHAEL_CLOSE = pygame.image.load(ROOT_DIR / "src/assets/img/michael_close.png").convert_alpha()
S_MICHAEL_BATTLE = slice_sheet(ROOT_DIR / "src/assets/img/lord.png", 65, 161)
for i, sprite in enumerate(S_MICHAEL_BATTLE):
    S_MICHAEL_BATTLE[i] = pygame.transform.scale_by(sprite, 1.4).convert_alpha()
S_MICHAEL_BATTLE.append(S_MICHAEL_BATTLE[1])
S_HEART = pygame.image.load(ROOT_DIR / "src/assets/img/heart.png").convert_alpha()
S_COLLECTABLE = pygame.Surface((8, 8)).convert_alpha()
S_COLLECTABLE.fill(const.RED)
S_TALK_BOX = pygame.image.load(ROOT_DIR / "src/assets/img/talk.png").convert_alpha()


S_ARENA = pygame.Surface((5, 220))
S_ARENA.fill(const.WHITE)
S_CORRIDOR = pygame.transform.scale(
    pygame.image.load(ROOT_DIR / "src/assets/img/last_corridor.jpg").convert(),
    (3000, 675),
)
S_MENU_OPTIONS = slice_sheet(ROOT_DIR / "src/assets/img/menu_options.png", 110, 42)
for i, menu_option in enumerate(S_MENU_OPTIONS):
    S_MENU_OPTIONS[i] = pygame.transform.scale_by(menu_option, 1.4).convert_alpha()
S_ATTACK_BAR = pygame.image.load(ROOT_DIR / "src/assets/img/attack_bar.png").convert_alpha()
S_PILLAR = pygame.image.load(ROOT_DIR / "src/assets/img/pillar.png").convert_alpha()
S_PILLAR = pygame.transform.scale(
    S_PILLAR,
    (
        S_PILLAR.get_width() * (const.WINDOW_WIDTH * 2.5 / const.WINDOW_HEIGHT),
        const.WINDOW_HEIGHT + 300,
    ),
)

# WARN sprite generico pra teste, adicione sprites para cada ataque
S_ENEMY_ATTACK = pygame.Surface((10, 10)).convert_alpha()
S_ENEMY_ATTACK.fill(const.WHITE)

# Load audio (ogg for web compatibility)
SFX_MASTER = AudioManager()
pygame.mixer.music.load(ROOT_DIR / "src/assets/sfx/theme.ogg")
SFX_MASTER.load("move_selection", ROOT_DIR / "src/assets/sfx/move_selection.mp3")
SFX_MASTER.load("select_option", ROOT_DIR / "src/assets/sfx/select-option.mp3")
SFX_MASTER.load("undertale", ROOT_DIR / "src/assets/sfx/undertale.mp3")
SFX_MASTER.load("enemy_encounter", ROOT_DIR / "src/assets/sfx/enemy_encounter.mp3")
SFX_MASTER.load("talking_long", ROOT_DIR / "src/assets/sfx/talking_double.mp3")
SFX_MASTER.load("hee_hee", ROOT_DIR / "src/assets/sfx/hee-hee.mp3")
SFX_MASTER.load("auw", ROOT_DIR / "src/assets/sfx/auw.mp3")
SFX_MASTER.load("damage_item", ROOT_DIR / "src/assets/sfx/damage-item.mp3")
SFX_MASTER.load("healing_item", ROOT_DIR / "src/assets/sfx/healing-item.mp3")
SFX_MASTER.load("damage_taken", ROOT_DIR / "src/assets/sfx/damage-taken.mp3")
SFX_MASTER.load("defense_item", ROOT_DIR / "src/assets/sfx/defense-item.mp3")
SFX_MASTER.load("no_items", ROOT_DIR / "src/assets/sfx/no-items.mp3")

# Load fonts (ttf for web compatibility)
F_JERSEY10_SMALL = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 18)
F_JERSEY10 = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 28)
F_JERSEY10_MEDIUM = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 36)
F_JERSEY10_LARGE = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 80)

print("Loaded assets")
