from typing import Hashable, Literal
import pygame.mixer
from components.config import Config
import core.assets as assets
from utilities import languages


dialog = languages.DIALOGS[Config().data["lang"]]
interface = languages.INTERFACE[Config().data["lang"]]

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
bandaid_item= ItemInfo(
    interface["items"]["bandaid"],
    "bandaid",
    "healing",
    40,
    dialog["items"]["bandaid"],
    assets.SFX_MASTER.audios["healing_item"]
)

cake_item = ItemInfo(
    interface["items"]["cake"],
    "cake",
    "healing",
    15,
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
    10,
    dialog["items"]["moonwalk"],
    assets.SFX_MASTER.audios["defense_item"],
    2
)



AVALIABLE_ITEMS = [
    bandaid_item,
    cake_item, cake_item,
    strength_item, strength_item, strength_item,strength_item,strength_item,
    hee_hee_item, hee_hee_item,
    moonwalk_item, moonwalk_item
]
