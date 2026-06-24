from re import sub

import pygame
import copy
import core.constants as const
import core.assets as assets
import scenes.menu

from decimal import Decimal
from components.config import Config
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action

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
        menu_options = {
            "VOLUME GERAL": int(config.config["master_volume"] * 100),
            "MÚSICA": int(config.config["music_volume"] * 100),
            "EFEITOS SONOROS": int(config.config["effect_volume"] * 100),
            "TELA CHEIA": "ATIVADO" if config.config["fullscreen"] else "DESATIVADO",
            "CRT": "ATIVADO" if config.config["crt"] else "DESATIVADO",
            "ABERRAÇÃO CROMÁTICA": "ATIVADO" if config.config["chromatic"] else "DESATIVADO",
            "FPS": "ILIMITADO" if config.config["fps"] == 0  else config.config["fps"],
            "VSYNC": "ATIVADO" if config.config["vsync"] else "DESATIVADO",
            "SALVAR": "SALVAR"
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


        if self.selected_option == list(menu_options.keys()).index("VOLUME GERAL"):
            master_valume = Decimal(str(config.config["master_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["master_volume"] =  float(master_valume + Decimal("0.05"))
                if config.config["master_volume"] > 1:
                    config.config["master_volume"] = 1
                assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["master_volume"] =  float(master_valume - Decimal("0.05"))
                if config.config["master_volume"] < 0:
                    config.config["master_volume"] = 0
                assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index("MÚSICA"):
            master_valume = Decimal(str(config.config["music_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["music_volume"] =  float(master_valume + Decimal("0.05"))
                if config.config["music_volume"] > 1:
                    config.config["music_volume"] = 1
                assets.SFX_MASTER.set_music_volume(config.config["music_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["music_volume"] =  float(master_valume - Decimal("0.05"))
                if config.config["music_volume"] < 0:
                    config.config["music_volume"] = 0
                assets.SFX_MASTER.set_music_volume(config.config["music_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index("EFEITOS SONOROS"):
            master_valume = Decimal(str(config.config["effect_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["effect_volume"] =  float(master_valume + Decimal("0.05"))
                if config.config["effect_volume"] > 1:
                    config.config["effect_volume"] = 1
                assets.SFX_MASTER.set_effect_volume(config.config["effect_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()
            elif (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["effect_volume"] =  float(master_valume - Decimal("0.05"))
                if config.config["effect_volume"] > 1:
                    config.config["effect_volume"] = 1
                assets.SFX_MASTER.set_effect_volume(config.config["effect_volume"])
                assets.SFX_MASTER.update_volume()
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index("TELA CHEIA"):
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

        elif self.selected_option == list(menu_options.keys()).index("ABERRAÇÃO CROMÁTICA"):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["chromatic"] = not config.config["chromatic"]
                assets.SFX_MASTER.audios["move_selection"].play()

        elif self.selected_option == list(menu_options.keys()).index("FPS"):
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


        elif self.selected_option == list(menu_options.keys()).index("VSYNC"):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["vsync"] = (config.config["vsync"] + 1) % 2
                assets.SFX_MASTER.audios["move_selection"].play()


        elif self.selected_option == list(menu_options.keys()).index("SALVAR"):
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
                100 + 50 * (i)
            )

            pos_value = (
                500,
                100 + 50 * (i)
            )

            if self.selected_option == i:
                color = const.YELLOW
                heart_pos = (pos_option[0] - 40, pos_option[1] + 7)
            else:
                color = const.ORANGE

            option_text = assets.F_JERSEY10_MEDIUM.render(option, True, color)
            value_text = assets.F_JERSEY10_MEDIUM.render(str(menu_options[option]), True, color)

            surface.blit(option_text, pos_option)
            if option != "SALVAR":
                surface.blit(value_text, pos_value)

        subtitle = assets.F_JERSEY10_MEDIUM.render("VOLTAR [ESC]", True, const.WHITE)
        surface.blit(assets.S_HEART, heart_pos)
        surface.blit(subtitle, (100, const.WINDOW_HEIGHT - 50))


    def exit(self) -> None:
        pass
