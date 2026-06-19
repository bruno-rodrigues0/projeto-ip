# Persistent data betwen scenes

from scenes.scene import Scene

class Context:
    used_items: list[str] = []
    dialog_text: list[str] = []
    collected_coins = 0
    collected_life_orbs = 0
    last_scene: Scene
    paused: bool = False

