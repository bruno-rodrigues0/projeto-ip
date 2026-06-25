from typing import Hashable, Literal
import pygame.mixer
from components.config import Config
import core.assets as assets
from utilities import languages


dialog = languages.DIALOGS[Config().config["lang"]]
interface = languages.INTERFACE[Config().config["lang"]]

class ItemInfo:
    name: str
    tag: str
    type: str
    buff: int
    dialog: str
    sound: pygame.mixer.Sound
    buff_count: int

    def __init__(
        self,
        name: str,
        tag: str,
        type: Literal["healing", "damage", "defense"],
        buff: int,
        dialog: str,
        sound: pygame.mixer.Sound,
        buff_count=1,
    ):
        self.name = name
        self.tag = tag
        self.type = type
        self.buff = buff
        self.dialog = dialog
        self.sound = sound
        self.buff_count = buff_count


# Initial items
cake_item = ItemInfo(
    interface["items"]["cake"],
    "cake",
    "healing",
    99,
    dialog["items"]["cake"],
    assets.SFX_MASTER.audios["healing_item"]
)

strength_item = ItemInfo(
    interface["items"]["strength"],
    "strength",
    "damage",
    1,
    dialog["items"]["strength"],
    assets.SFX_MASTER.audios["damage_item"],
    1
)
hee_hee_item = ItemInfo(
    interface["items"]["hee_hee"],
    "hee_hee",
    "damage",
    50,
    dialog["items"]["hee_hee"],
    assets.SFX_MASTER.audios["hee_hee"],
    2
)
moonwalk_item = ItemInfo(
    interface["items"]["moonwalk"],
    "moonwalk",
    "defense",
    30,
    dialog["items"]["moonwalk"],
    assets.SFX_MASTER.audios["defense_item"],
    2
)



AVALIABLE_ITEMS = [cake_item, cake_item, strength_item, hee_hee_item, moonwalk_item]
