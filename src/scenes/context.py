from scenes.scene import Scene
from components.items_info import ItemInfo, AVALIABLE_ITEMS
from entities.bosses.bosses_info import AVALIABLE_BOSSES
from entities.boss import Boss


class Context:
    """
    Persistent data betwen scenes.
    """

    start_time: int = 0
    used_items: list[ItemInfo] = []
    dialog_text: list[str] = []
    collected_life_orbs: int = 0
    collected_defense_orbs: int = 0
    collected_damage_orbs: int = 0
    last_scene: Scene
    paused: bool = False
    battle_state: str = "battle_menu"
    item_used: ItemInfo
    items = AVALIABLE_ITEMS
    deaths: int = 0
    boss_idx: int = 0
    BOSS: Boss = AVALIABLE_BOSSES[boss_idx]
