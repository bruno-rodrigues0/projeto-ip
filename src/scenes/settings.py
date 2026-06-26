from re import sub

import pygame
import copy
import core.constants as const
import core.assets as assets
import scenes.menu

from utilities import languages
from decimal import Decimal
from components.config import Config
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from components.items_info import AVALIABLE_ITEMS

config = Config()

class Settings(Scene):
    def enter(self) -> None:
        self.selected_option = 0
        self.config_backup = copy.deepcopy(config)

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:
        global config
        lang = languages.INTERFACE[config.data["lang"]]
        dialog = languages.DIALOGS[config.data["lang"]]
        enabled = lang["options_menu"]["enabled"]
        disabled = lang["options_menu"]["disabled"]

        menu_options = {
            lang["options_menu"]["master_volume"]: int(config.data["master_volume"] * 100),
            lang["options_menu"]["music_volume"]: int(config.data["music_volume"] * 100),
            lang["options_menu"]["effect_volume"]: int(config.data["effect_volume"] * 100),
            lang["options_menu"]["lang"]: "ENGLISH" if config.data["lang"] == "en_us" else "PORTUGUÊS",
            lang["options_menu"]["fullscreen"]: enabled if config.data["fullscreen"] else disabled,
            lang["options_menu"]["crt"]: enabled if config.data["crt"] else disabled,
            lang["options_menu"]["chromatic"]: enabled if config.data["chromatic"] else disabled,
            lang["options_menu"]["fps"]: lang["options_menu"]["unlimited"] if config.data["fps"] == 0  else config.data["fps"],
            lang["options_menu"]["vsync"]: enabled if config.data["vsync"] else disabled,
            lang["options_menu"]["save"]: lang["options_menu"]["save"]
        }

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            self.statemachine.change_state(scenes.menu.Menu) # type: ignore

        if action_buffer[Action.DOWN] == InputState.PRESSED:
            self.selected_option = (self.selected_option + 1) % len(menu_options)
            assets.SFX_MASTER.audios["move_selection"].play()

        if action_buffer[Action.UP] == InputState.PRESSED:
            self.selected_option = (self.selected_option - 1) % len(menu_options)
            assets.SFX_MASTER.audios["move_selection"].play()


        if self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["master_volume"]):
            master_volume = Decimal(str(config.data["master_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.data["master_volume"] =  float(master_volume + Decimal("0.05"))
                if config.data["master_volume"] > 1:
                    config.data["master_volume"] = 1
                assets.SFX_MASTER.set_master_volume(config.data["master_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["master_volume"] =  float(master_volume - Decimal("0.05"))
                if config.data["master_volume"] < 0:
                    config.data["master_volume"] = 0
                assets.SFX_MASTER.set_master_volume(config.data["master_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["music_volume"]):
            master_volume = Decimal(str(config.data["music_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.data["music_volume"] =  float(master_volume + Decimal("0.05"))
                if config.data["music_volume"] > 1:
                    config.data["music_volume"] = 1
                assets.SFX_MASTER.set_music_volume(config.data["music_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["music_volume"] =  float(master_volume - Decimal("0.05"))
                if config.data["music_volume"] < 0:
                    config.data["music_volume"] = 0
                assets.SFX_MASTER.set_music_volume(config.data["music_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["effect_volume"]):
            master_volume = Decimal(str(config.data["effect_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.data["effect_volume"] =  float(master_volume + Decimal("0.05"))
                if config.data["effect_volume"] > 1:
                    config.data["effect_volume"] = 1
                assets.SFX_MASTER.set_effect_volume(config.data["effect_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["effect_volume"] =  float(master_volume - Decimal("0.05"))
                if config.data["effect_volume"] > 1:
                    config.data["effect_volume"] = 1
                assets.SFX_MASTER.set_effect_volume(config.data["effect_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["lang"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["lang"] = "en_us" if config.data["lang"] == "pt_br" else "pt_br"
                lang = languages.INTERFACE[config.data["lang"]]
                dialog = languages.DIALOGS[config.data["lang"]]
                for i, item in enumerate(AVALIABLE_ITEMS):
                    AVALIABLE_ITEMS[i].dialog = dialog["items"][item.tag]
                    AVALIABLE_ITEMS[i].name = lang["items"][item.tag]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["fullscreen"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["fullscreen"] = not config.data["fullscreen"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index("CRT"):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["crt"] = not config.data["crt"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["chromatic"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["chromatic"] = not config.data["chromatic"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["fps"]):
            values = [0, 60, 120, 240]
            fps = config.data["fps"]
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                new_value = values[(values.index(fps) + 1) % len(values)]
                config.data["fps"] = new_value
                assets.SFX_MASTER.audios["move_selection"].play()

            if (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                new_value = values[(values.index(fps) - 1) % len(values)]
                config.data["fps"] = new_value
                assets.SFX_MASTER.audios["move_selection"].play()


        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["vsync"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.data["vsync"] = (config.data["vsync"] + 1) % 2
                assets.SFX_MASTER.audios["move_selection"].play()


        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["save"]):
            if action_buffer[Action.START] == InputState.PRESSED:
                if (
                    config.data["fullscreen"] != self.config_backup.config["fullscreen"] or
                    config.data["vsync"] != self.config_backup.config["vsync"]
                ):
                    config.apply_config()
                    self.config_backup = copy.deepcopy(config)
                config.save_file()
                assets.SFX_MASTER.audios["select_option"].play()

        surface.fill(const.BLACK)
        heart_pos = (0, 0)

        for i, option in enumerate(menu_options):
            pos_option = (
                100,
                50 + 50 * (i)
            )

            pos_value = (
                500,
                50 + 50 * (i)
            )

            if self.selected_option == i:
                color = const.YELLOW
                heart_pos = (pos_option[0] - 40, pos_option[1] + 7)
            else:
                color = const.ORANGE

            option_text = assets.F_JERSEY10_MEDIUM.render(option, True, color)
            value_text = assets.F_JERSEY10_MEDIUM.render(str(menu_options[option]), True, color)

            surface.blit(option_text, pos_option)
            if option != lang["options_menu"]['save']:
                surface.blit(value_text, pos_value)

        subtitle = assets.F_JERSEY10_MEDIUM.render(f'{lang["options_menu"]["back"]} [ESC]', True, const.WHITE)
        surface.blit(assets.S_HEART, heart_pos)
        surface.blit(subtitle, (100, const.WINDOW_HEIGHT - 50))


    def exit(self) -> None:
        pass
