from typing import Literal
import pygame.mixer
import core.assets as assets


class ItemInfo:
    name: str
    type: str
    buff: int
    dialog: str
    sound: pygame.mixer.Sound
    buff_count: int

    def __init__(
        self,
        name: str,
        type: Literal["healing", "damage", "defense"],
        buff: int,
        dialog: str,
        sound: pygame.mixer.Sound,
        buff_count=1,
    ):
        self.name = name
        self.type = type
        self.buff = buff
        self.dialog = dialog
        self.sound = sound
        self.buff_count = buff_count


# Initial items
cake_item = ItemInfo(
    "Bolo",
    "healing",
    99,
    "... Então você decidiu comer o bolo?",
    assets.SFX_MASTER.audios["healing_item"]),

strength_item = ItemInfo(
    "Bíceps",
    "damage",
    1,
    "Você usou toda sua força! Seu ataque aumentou em 1.",
    assets.SFX_MASTER.audios["damage_item"],
    1
)
hee_hee_item = ItemInfo(
    "Hee-Hee",
    "damage",
    50,
    "Você imita 'Hee-Hee!' Perfeitamente. Seu ataque subiu em 50 no próximo turno!",
    assets.SFX_MASTER.audios["hee_hee"],
    2
)
moonwalk_item = ItemInfo(
    "Moonwalk",
    "defense",
    30,
    "Você faz o Moonwalk e se afasta do Michael. Sua defesa aumentou em 30!",
    assets.SFX_MASTER.audios["defense_item"],
    2
)


AVALIABLE_ITEMS = [cake_item, strength_item, hee_hee_item, moonwalk_item]
