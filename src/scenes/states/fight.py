import random

import pygame
from random import randint

import core.assets as assets
import core.constants as const
from core.input import InputBuffer, InputState, Action
from components.statemachine import State
from components.object import SimulatedObject
from components.dialog_printer import DialogPrinter
from entities.attacks.attack_list import ATTACK_LIST
from entities.collectable import Collectable
from entities.attacks.attack02 import Attack02
from entities.player import Player
from scenes.context import Context

MAX_VEL = 220


# Scene objects
COLLECTABLE = Collectable(
    assets.S_COLLECTABLE,
    const.WINDOW_CENTRE[0],
    const.WINDOW_CENTRE[1] - 25,
    "healing",
    5,
    assets.SFX_MASTER.audios["healing_item"]
)

offset = assets.S_ARENA.get_size()[1] // 2
ARENA_RECT = pygame.Rect(
    const.WINDOW_CENTRE[0] - offset,
    const.WINDOW_CENTRE[1] - offset + 80,
    assets.S_ARENA.get_height(),
    assets.S_ARENA.get_height()
)

ARENA_WALL01 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    ARENA_RECT.topleft[0],
    ARENA_RECT.topleft[1],
)
ARENA_WALL02 = SimulatedObject(
    assets.S_ARENA,
    ARENA_RECT.topleft[0],
    ARENA_RECT.topleft[1],
)
ARENA_WALL03 = SimulatedObject(
    assets.S_ARENA,
    ARENA_RECT.topright[0],
    ARENA_RECT.topright[1],
)
ARENA_WALL04 = SimulatedObject(
    pygame.transform.rotate(assets.S_ARENA, 90),
    ARENA_RECT.bottomleft[0],
    ARENA_RECT.bottomleft[1] - 5,
)

ARENA = [ARENA_WALL01, ARENA_WALL02, ARENA_WALL03, ARENA_WALL04]

E_ATTACK = ATTACK_LIST[randint(0, len(ATTACK_LIST) - 1)]()

ellapsed_time = 0

collectable_group = pygame.sprite.Group()
arena_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

for wall in ARENA:
    arena_group.add(wall)

for proj in E_ATTACK.projectiles:
    enemy_group.add(proj)


class Fight(State):
    def enter(self) -> None:
        pass

    def execute(
        self,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
        PLAYER: Player,
    ) -> None:
        global E_ATTACK, ellapsed_time
        ellapsed_time += dt

        PLAYER.move(action_buffer, arena_group, MAX_VEL, dt)
        E_ATTACK.update(dt)
        PLAYER.update(dt)

        # finaliza o turno de ataque
        if ellapsed_time >= E_ATTACK.attack_time:
            ellapsed_time = 0
            enemy_group.empty()
            collectable_group.empty()
            self.has_collectable = False
            E_ATTACK.projectiles.clear()
            E_ATTACK = ATTACK_LIST[randint(0, len(ATTACK_LIST) - 1)]()
            for proj in E_ATTACK.projectiles:
                enemy_group.add(proj)
            PLAYER.update_buffs() # reseta os buffs de turno
            PLAYER.x, PLAYER.y = (value - 5 for value in ARENA_RECT.center)
            Context.battle_state = "battle_menu"
            self.printer = DialogPrinter(const.BASE_DIALOGS[randint(0, len(const.BASE_DIALOGS) - 1)], 40, 30)
            return


        # Spawn chance of a collectable item (33% for 2 seconds)
        if int(ellapsed_time) % 2 == 0:
            if random.random() <= 0.01 and not self.has_collectable:
                self.has_collectable = True
                spawn_collectable(dt)

        # Collect items
        if self.has_collectable:
            collected = pygame.sprite.spritecollide(PLAYER, collectable_group, True)

            for item in collected:
                collectable_group.remove(item)
                self.has_collectable = False
                item.sound.play()
                if item.type == "healing":
                    PLAYER.heal(item.buff)
                    Context.collected_life_orbs += 1
                elif item.type == "defense":
                    PLAYER.buff_defense(item.buff, 1)
                    Context.collected_defense_orbs += 1

        # If have a collectable item in scene
        if self.has_collectable:
            COLLECTABLE.update(dt)

            collectable_group.draw(surface)
            if COLLECTABLE.y >= ARENA_RECT.bottomleft[1] - 5:
                self.has_collectable = False
                collectable_group.remove(COLLECTABLE)

        # Colide with enemy
        collided_enemies = pygame.sprite.spritecollide(PLAYER, enemy_group, False)

        for _enemy in collided_enemies:
            PLAYER.take_damage(1)

        surface.blit(PLAYER.image, PLAYER.get_pos())
        arena_group.draw(surface)
        collectable_group.draw(surface)
        enemy_group.draw(surface)

    def exit(self) -> None:
        pass


def spawn_collectable(dt: float) -> None:
    global COLLECTABLE, ARENA_RECT

    types = ["healing", "defense"]
    COLLECTABLE.type = types[randint(0, 1)]

    assert COLLECTABLE.image is not None
    if COLLECTABLE.type == "healing":
        COLLECTABLE.image.fill(const.RED)
    else:
        COLLECTABLE.image.fill(const.CYAN)

    COLLECTABLE.x_ref = randint(ARENA_RECT.topleft[0] + 50, ARENA_RECT.topright[0] - 50)
    COLLECTABLE.y = const.WINDOW_CENTRE[1] - 30
    COLLECTABLE.update(dt)

    collectable_group.add(COLLECTABLE)
