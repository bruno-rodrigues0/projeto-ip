import pygame
from decimal import Decimal
import math
from components.config import Config
import core.constants as const
import core.assets as assets

from scenes import menu
from scenes.scene import Scene
from core.input import InputBuffer, InputState, Action
from scenes.context import Context

config = Config()

class Settings(Scene):
    def enter(self) -> None:
        self.selected_option = 0

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer
    ) -> None:
        global config
        menu_options = {
            "VOLUME": int(config.config["master_volume"] * 100),
            "TELA CHEIA": "ATIVADO" if config.config["fullscreen"] else "DESATIVADO",
            "FPS": "ILIMITADO" if config.config["fps"] == 0  else config.config["fps"],
            "VSYNC": "ATIVADO" if config.config["vsync"] else "DESATIVADO",
            "SALVAR": "SALVAR"
        }

        if (
            action_buffer[Action.OPTIONS] == InputState.PRESSED
        ):
            self.statemachine.change_state(Context.last_scene) # type: ignore

        if action_buffer[Action.DOWN] == InputState.PRESSED:
            self.selected_option = (self.selected_option + 1) % len(menu_options)
            assets.SFX_MASTER.audios["move_selection"].play()

        if action_buffer[Action.UP] == InputState.PRESSED:
            self.selected_option = (self.selected_option - 1) % len(menu_options)
            assets.SFX_MASTER.audios["move_selection"].play()


        if self.selected_option == list(menu_options.keys()).index("VOLUME"):
            master_valume = Decimal(str(config.config["master_volume"])[:5])
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                config.config["master_volume"] =  float(master_valume + Decimal("0.05"))
                if config.config["master_volume"] > 1:
                    config.config["master_volume"] = 1
                assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
                assets.SFX_MASTER.audios["move_selection"].play()
            if (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["master_volume"] =  float(master_valume - Decimal("0.05"))
                if config.config["master_volume"] < 0:
                    config.config["master_volume"] = 0
                assets.SFX_MASTER.set_master_volume(config.config["master_volume"])
                assets.SFX_MASTER.audios["move_selection"].play()


        elif self.selected_option == list(menu_options.keys()).index("TELA CHEIA"):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["fullscreen"] = not config.config["fullscreen"]


        elif self.selected_option == list(menu_options.keys()).index("FPS"):
            values = [0, 60, 120, 240]
            fps = config.config["fps"]
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED
            ):
                new_value = values[(values.index(fps) + 1) % len(values)]
                config.config["fps"] = new_value

            if (
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                new_value = values[(values.index(fps) - 1) % len(values)]
                config.config["fps"] = new_value


        elif self.selected_option == list(menu_options.keys()).index("VSYNC"):
            if (
                action_buffer[Action.RIGHT] == InputState.PRESSED or
                action_buffer[Action.LEFT] == InputState.PRESSED
            ):
                config.config["vsync"] = (config.config["vsync"] + 1) % 2


        elif self.selected_option == list(menu_options.keys()).index("SALVAR"):
            if action_buffer[Action.START] == InputState.PRESSED:
                config.apply_config()
                config.save_file()

        surface.fill(const.BLACK)
        heart_pos = (0, 0)

        for i, option in enumerate(menu_options):
            pos_option = (
                100,
                100 + 50 * (i)
            )

            pos_value = (
                300,
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

        surface.blit(assets.S_HEART, heart_pos)


    def exit(self) -> None:
        pass
