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
S_FLOWEY = slice_sheet(ROOT_DIR / "src/assets/img/flowey.png", 50, 25)
for i, frame in enumerate(S_FLOWEY):
    S_FLOWEY[i] = pygame.transform.scale_by(frame, 2.2).convert_alpha()
S_FLOWEY_NICE = slice_sheet(ROOT_DIR / "src/assets/img/flowey_nice.png", 84, 44)
for i, frame in enumerate(S_FLOWEY_NICE):
    S_FLOWEY_NICE[i] = pygame.transform.scale_by(frame, 1.3).convert_alpha()
S_MICHAEL = pygame.transform.scale_by(
    pygame.image.load(ROOT_DIR / "src/assets/img/michael.png"), 0.4
).convert_alpha()
S_MICHAEL_CLOSE = pygame.image.load(ROOT_DIR / "src/assets/img/michael_close.png").convert_alpha()
S_MICHAEL_BATTLE = slice_sheet(ROOT_DIR / "src/assets/img/lord.png", 65, 161)
for i, sprite in enumerate(S_MICHAEL_BATTLE):
    S_MICHAEL_BATTLE[i] = pygame.transform.scale_by(sprite, 1.4).convert_alpha()
S_MICHAEL_BATTLE.append(S_MICHAEL_BATTLE[1])
S_HEART = pygame.image.load(ROOT_DIR / "src/assets/img/heart.png").convert_alpha()
S_HEART_BREAK = pygame.image.load(ROOT_DIR / "src/assets/img/heart_break.png").convert_alpha()
S_FRAGMENTS = slice_sheet(ROOT_DIR / "src/assets/img/fragments.png", 11, 10)
S_KNIFE = slice_sheet(ROOT_DIR / "src/assets/img/knife.png", 26, 110)
for i, frame in enumerate(S_KNIFE):
    S_KNIFE[i] = pygame.transform.scale_by(frame, 2.3).convert_alpha()
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
).convert_alpha()

S_SHIELD = pygame.image.load(ROOT_DIR / "src/assets/img/shield.png").convert_alpha()
S_SWORD = pygame.image.load(ROOT_DIR / "src/assets/img/sword.png").convert_alpha()
S_LIFE = pygame.image.load(ROOT_DIR / "src/assets/img/life.png").convert_alpha()

# WARN sprite generico pra teste, adicione sprites para cada ataque
S_ENEMY_ATTACK = pygame.Surface((25, 25)).convert_alpha()
S_ENEMY_ATTACK.fill(const.WHITE)
S_MOONWALK_ATTACK = slice_sheet(ROOT_DIR / "src/assets/img/moonwalk.png", 98, 191)
for i, frame in enumerate(S_MOONWALK_ATTACK):
    S_MOONWALK_ATTACK[i] = pygame.transform.scale_by(frame, 0.6).convert_alpha()

# Load audio (ogg for web compatibility)
SFX_MASTER = AudioManager()
pygame.mixer.music.load(ROOT_DIR / "src/assets/sfx/smooth-criminal.ogg")
SFX_MASTER.load("move_selection", ROOT_DIR / "src/assets/sfx/move_selection.mp3")
SFX_MASTER.load("select_option", ROOT_DIR / "src/assets/sfx/select-option.mp3")
SFX_MASTER.load("undertale", ROOT_DIR / "src/assets/sfx/undertale.mp3")
SFX_MASTER.load("enemy_encounter", ROOT_DIR / "src/assets/sfx/enemy_encounter.mp3")
SFX_MASTER.load("talking_long", ROOT_DIR / "src/assets/sfx/talking_double.mp3")
SFX_MASTER.load("intro_talking", ROOT_DIR / "src/assets/sfx/intro_talking.mp3")
SFX_MASTER.load("intro_menu_sound", ROOT_DIR / "src/assets/sfx/intro_menu_sound.mp3")
SFX_MASTER.load("hee_hee", ROOT_DIR / "src/assets/sfx/hee-hee.mp3")
SFX_MASTER.load("auw", ROOT_DIR / "src/assets/sfx/auw.mp3")
SFX_MASTER.load("damage_item", ROOT_DIR / "src/assets/sfx/damage-item.mp3")
SFX_MASTER.load("healing_item", ROOT_DIR / "src/assets/sfx/healing-item.mp3")
SFX_MASTER.load("damage_taken", ROOT_DIR / "src/assets/sfx/damage-taken.mp3")
SFX_MASTER.load("defense_item", ROOT_DIR / "src/assets/sfx/defense-item.mp3")
SFX_MASTER.load("no_items", ROOT_DIR / "src/assets/sfx/no-items.mp3")
SFX_MASTER.load("player_attack", ROOT_DIR / "src/assets/sfx/player_attack.mp3")
SFX_MASTER.load("soul_shatter", ROOT_DIR / "src/assets/sfx/soul_shatter.mp3")

# Load fonts (ttf for web compatibility)
F_JERSEY10_SMALL = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 18)
F_JERSEY10 = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 28)
F_JERSEY10_MEDIUM = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 36)
F_JERSEY10_MEDIUM_LARGE = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 54)
F_JERSEY10_LARGE = pygame.font.Font(ROOT_DIR / "src/assets/fonts/Jersey10-Regular.ttf", 80)

S_CIRCLE_ATTACK = pygame.Surface((24, 24)).convert_alpha()
S_CIRCLE_ATTACK.fill((0, 0, 0, 0))
pygame.draw.circle(S_CIRCLE_ATTACK, const.WHITE, (12, 12), 12)
S_HEE_HEE_ATTACK = F_JERSEY10_MEDIUM.render("HEE-HEE!", True, const.WHITE)
S_CRESCENDO_ATTACK = F_JERSEY10_MEDIUM.render("CRESCENDO", True, const.WHITE)
S_AUW_ATTACK = F_JERSEY10_MEDIUM.render("AUW!", True, const.WHITE)
S_ANNIE_ATTACK = F_JERSEY10_MEDIUM.render("ANNIE?", True, const.WHITE)
S_AYUWOKI_ATTACK = F_JERSEY10_MEDIUM.render("AYUWOKI?", True, const.WHITE)
S_SMOOTH_ATTACK = F_JERSEY10_MEDIUM.render("SMOOTH", True, const.WHITE)
S_CRESCENDO_ATTACK = F_JERSEY10_MEDIUM.render("CRIMINAL", True, const.WHITE)

print("Loaded assets")
