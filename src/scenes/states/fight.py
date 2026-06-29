import random
import pygame
from random import randint

import core.assets as assets
import core.constants as const
from core.input import InputBuffer
from components.statemachine import State
from components.object import SimulatedObject
from entities.bosses.michael_jackson.attacks.attack_list import ATTACK_LIST
from entities.collectable import Collectable
from scenes.context import Context

MAX_VEL = 220

COLLECTABLE = Collectable(
    assets.S_COLLECTABLE,
    const.WINDOW_CENTRE[0],
    const.WINDOW_CENTRE[1] - 25,
    "healing", 5,
    assets.SFX_MASTER.audios["healing_item"]
)

offset = assets.S_ARENA.get_size()[1] // 2
ARENA_RECT = pygame.Rect(
    const.WINDOW_CENTRE[0] - offset,
    const.WINDOW_CENTRE[1] - offset + 80,
    assets.S_ARENA.get_height(),
    assets.S_ARENA.get_height(),
)

ARENA = [
    SimulatedObject(pygame.transform.rotate(assets.S_ARENA, 90), ARENA_RECT.topleft[0], ARENA_RECT.topleft[1]),
    SimulatedObject(assets.S_ARENA, ARENA_RECT.topleft[0], ARENA_RECT.topleft[1]),
    SimulatedObject(assets.S_ARENA, ARENA_RECT.topright[0], ARENA_RECT.topright[1]),
    SimulatedObject(pygame.transform.rotate(assets.S_ARENA, 90), ARENA_RECT.bottomleft[0], ARENA_RECT.bottomleft[1] - 5),
]

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

    @staticmethod
    def enter(game) -> None:
        game.last_collectable_check = -1

    @staticmethod
    def execute(
        game,
        surface: pygame.Surface,
        dt: float,
        action_buffer: InputBuffer,
    ) -> None:
        global E_ATTACK, ellapsed_time
        ellapsed_time += dt

        game.player.move(action_buffer, arena_group, MAX_VEL, dt)
        E_ATTACK.update(dt)
        game.player.update(dt)

        if ellapsed_time >= E_ATTACK.attack_time:
            ellapsed_time = 0
            enemy_group.empty()
            collectable_group.empty()
            game.has_collectable = False
            E_ATTACK.projectiles.clear()
            E_ATTACK = ATTACK_LIST[randint(0, len(ATTACK_LIST) - 1)]()
            for proj in E_ATTACK.projectiles:
                enemy_group.add(proj)
            game.player.update_buffs()
            game.player.x, game.player.y = (v - 5 for v in ARENA_RECT.center)
            Context.battle_state = "battle_menu"
            return

        current_second = int(ellapsed_time)
        if (
            current_second != game.last_collectable_check
            and not game.has_collectable
        ):
            game.last_collectable_check = current_second
            if random.random() <= 0.2:
                game.has_collectable = True
                spawn_collectable(dt)

        if game.has_collectable:
            collected = pygame.sprite.spritecollide(game.player, collectable_group, True)
            for item in collected:
                collectable_group.remove(item)
                game.has_collectable = False
                item.sound.play()

                if item.type == "healing":
                    game.player.heal(item.buff)
                    Context.collected_life_orbs += 1
                elif item.type == "defense":
                    game.player.buff_defense(item.buff, 1)
                    Context.collected_defense_orbs += 1
                elif item.type == "damage":
                    game.player.buff_damage(item.buff, 2)
                    Context.collected_damage_orbs += 1

        if game.has_collectable:
            COLLECTABLE.update(dt)
            collectable_group.draw(surface)

            if COLLECTABLE.y >= ARENA_RECT.bottomleft[1] - 5:
                game.has_collectable = False
                collectable_group.remove(COLLECTABLE)

        # Colide with enemy
        collided_enemies = pygame.sprite.spritecollide(game.player, enemy_group, False, pygame.sprite.collide_mask)

        for _enemy in collided_enemies:
            game.player.take_damage(1 * dt)

        surface.blit(game.player.image, game.player.get_pos())
        arena_group.draw(surface)
        collectable_group.draw(surface)
        enemy_group.draw(surface)

def spawn_collectable(dt: float) -> None:
    global COLLECTABLE
    assert COLLECTABLE.image is not None

    types = {
        "healing": assets.S_LIFE,
        "defense": assets.S_SHIELD,
        "damage": assets.S_SWORD
    }

    COLLECTABLE.type = list(types.keys())[randint(0, 2)]
    COLLECTABLE.image = types[COLLECTABLE.type]
    COLLECTABLE.x_ref = randint(ARENA_RECT.topleft[0] + 50, ARENA_RECT.topright[0] - 50)
    COLLECTABLE.y = const.WINDOW_CENTRE[1] - 30
    COLLECTABLE.update(dt)

    collectable_group.add(COLLECTABLE)
