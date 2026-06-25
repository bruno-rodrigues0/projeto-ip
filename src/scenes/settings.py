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
        lang = languages.INTERFACE[config.config["lang"]]
        dialog = languages.DIALOGS[config.config["lang"]]
        enabled = lang["options_menu"]["enabled"]
        disabled = lang["options_menu"]["disabled"]

        menu_options = {
            lang["options_menu"]["master_volume"]: int(config.config["master_volume"] * 100),
            lang["options_menu"]["music_volume"]: int(config.config["music_volume"] * 100),
            lang["options_menu"]["effect_volume"]: int(config.config["effect_volume"] * 100),
            lang["options_menu"]["lang"]: "ENGLISH" if config.config["lang"] == "en_us" else "PORTUGUÊS",
            lang["options_menu"]["fullscreen"]: enabled if config.config["fullscreen"] else disabled,
            lang["options_menu"]["crt"]: enabled if config.config["crt"] else disabled,
            lang["options_menu"]["chromatic"]: enabled if config.config["chromatic"] else disabled,
            lang["options_menu"]["fps"]: lang["options_menu"]["unlimited"] if config.config["fps"] == 0  else config.config["fps"],
            lang["options_menu"]["vsync"]: enabled if config.config["vsync"] else disabled,
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
            master_volume = Decimal(str(config.config["master_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["master_volume"] =  float(master_volume + Decimal("0.05"))
                if config.config["master_volume"] > 1:
                    config.config["master_volume"] = 1
                assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["master_volume"] =  float(master_volume - Decimal("0.05"))
                if config.config["master_volume"] < 0:
                    config.config["master_volume"] = 0
                assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["music_volume"]):
            master_volume = Decimal(str(config.config["music_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["music_volume"] =  float(master_volume + Decimal("0.05"))
                if config.config["music_volume"] > 1:
                    config.config["music_volume"] = 1
                assets.SFX_MASTER.set_music_volume(config.config["music_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["music_volume"] =  float(master_volume - Decimal("0.05"))
                if config.config["music_volume"] < 0:
                    config.config["music_volume"] = 0
                assets.SFX_MASTER.set_music_volume(config.config["music_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["effect_volume"]):
            master_volume = Decimal(str(config.config["effect_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["effect_volume"] =  float(master_volume + Decimal("0.05"))
                if config.config["effect_volume"] > 1:
                    config.config["effect_volume"] = 1
                assets.SFX_MASTER.set_effect_volume(config.config["effect_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["effect_volume"] =  float(master_volume - Decimal("0.05"))
                if config.config["effect_volume"] > 1:
                    config.config["effect_volume"] = 1
                assets.SFX_MASTER.set_effect_volume(config.config["effect_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["lang"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["lang"] = "en_us" if config.config["lang"] == "pt_br" else "pt_br"
                lang = languages.INTERFACE[config.config["lang"]]
                dialog = languages.DIALOGS[config.config["lang"]]
                for i, item in enumerate(AVALIABLE_ITEMS):
                    AVALIABLE_ITEMS[i].dialog = dialog["items"][item.tag]
                    AVALIABLE_ITEMS[i].name = lang["items"][item.tag]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["fullscreen"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["fullscreen"] = not config.config["fullscreen"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index("CRT"):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["crt"] = not config.config["crt"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["chromatic"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["chromatic"] = not config.config["chromatic"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["fps"]):
            values = [0, 60, 120, 240]
            fps = config.config["fps"]
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                new_value = values[(values.index(fps) + 1) % len(values)]
                config.config["fps"] = new_value
                assets.SFX_MASTER.audios["move_selection"].play()

            if (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                new_value = values[(values.index(fps) - 1) % len(values)]
                config.config["fps"] = new_value
                assets.SFX_MASTER.audios["move_selection"].play()


        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["vsync"]):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["vsync"] = (config.config["vsync"] + 1) % 2
                assets.SFX_MASTER.audios["move_selection"].play()


        elif self.selected_option == list(menu_options.keys()).index(lang["options_menu"]["save"]):
            if action_buffer[Action.START] == InputState.PRESSED:
                if (
                    config.config["fullscreen"] != self.config_backup.config["fullscreen"] or
                    config.config["vsync"] != self.config_backup.config["vsync"]
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
