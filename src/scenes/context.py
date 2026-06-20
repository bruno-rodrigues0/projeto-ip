from scenes.scene import Scene

class Context:
    """
    Persistent data betwen scenes.
    """

    used_items: list[str] = []
    dialog_text: list[str] = []
    collected_coins = 0
    collected_life_orbs = 0
    last_scene: Scene
    paused: bool = False
    battle_state: str = "battle_menu"
    item_used: str
    items = [
        'Pie', 'Steak', 'L. Hero', 'L. Hero', 'L. Hero', 'L. Hero', 'L.Hero'
    ]

