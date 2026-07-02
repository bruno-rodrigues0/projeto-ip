import core.assets as assets
from components.animation import AnimationPlayer
from entities.boss import Boss
from entities.bosses.michael_jackson.attacks.attack_list import ATTACK_LIST



BOSS_MICHAEL_JACKSON = Boss(
    "Michael Jackson",
    800,
    AnimationPlayer("idle", assets.S_MICHAEL_BATTLE, 0.3),
    ATTACK_LIST,
)
