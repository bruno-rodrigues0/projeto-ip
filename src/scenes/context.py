import pygame
import core.assets as assets
import core.constants as const

from components.statistics import Statistics
from entities.player import Player
from scenes.scene import Scene
from components.items_info import ItemInfo, AVALIABLE_ITEMS
from entities.bosses.bosses_info import AVALIABLE_BOSSES
from entities.boss import Boss


class Context:
    """
    Persistent data betwen scenes.
    """

    start_time: int = 0
    has_taken_damage: bool = False
    is_first_attack = True
    used_items: list[ItemInfo] = []
    dialog_text: list[str] = []
    collected_life_orbs: int = 0
    collected_defense_orbs: int = 0
    collected_damage_orbs: int = 0
    last_scene: Scene | None
    paused: bool = False
    battle_state: str = "battle_menu"
    item_used: ItemInfo | None
    items = AVALIABLE_ITEMS.copy()
    deaths: int = 0
    boss_idx: int = 0
    BOSS: Boss = AVALIABLE_BOSSES[boss_idx]
    PLAYER = Player(
        pygame.transform.scale_by(assets.S_HEART, 0.8),
        const.WINDOW_CENTRE[0] - 5,
        const.WINDOW_CENTRE[1] + 60,
        100
    )

    @staticmethod
    def reset () -> None:
        Context.start_time = 0
        Context.has_taken_damage = False
        Context.is_first_attack = True
        Context.used_items = []
        Context.dialog_text = []
        Context.collected_life_orbs = 0
        Context.collected_defense_orbs = 0
        Context.collected_damage_orbs = 0
        Context.last_scene = None
        Context.paused = False
        Context.battle_state = "battle_menu"
        Context.item_used = None
        Context.items = AVALIABLE_ITEMS.copy()
        Context.deaths = 0
        Context.boss_idx = 0
        Context.BOSS = AVALIABLE_BOSSES[Context.boss_idx]

def reset_match() -> None:

    statistics = Statistics()

    pygame.mixer.music.rewind()
    Context.PLAYER.x = const.WINDOW_CENTRE[0]
    Context.PLAYER.y = const.WINDOW_CENTRE[1] + 60
    Context.PLAYER.current_hp = Context.PLAYER.max_hp
    Context.PLAYER.hp_percent = 1.0
    Context.PLAYER.damage = Context.PLAYER._initial_damage
    Context.PLAYER.defense = Context.PLAYER._initial_defense

    Context.BOSS.current_hp = Context.BOSS.max_hp

    statistics.data["deaths"] += Context.deaths
    statistics.data["life_orbs"] += Context.collected_life_orbs
    statistics.data["damage_orbs"] += Context.collected_damage_orbs
    statistics.data["defense_orbs"] += Context.collected_defense_orbs
    statistics.save_file()

    Context.reset()
