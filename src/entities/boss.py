import pygame

from random import randint
from entities.enemy_attack import EnemyAttack
from components.animation import AnimationPlayer
import core.assets as assets


class Boss:
    name: str
    max_hp: int
    current_hp: int
    sprite_animation: AnimationPlayer
    attack_list: list[EnemyAttack]
    current_attack: EnemyAttack

    def __init__(
        self,
        name: str,
        max_hp: int,
        sprite_animation: AnimationPlayer,
        attack_list: list[EnemyAttack],
    ):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.sprite_animation = sprite_animation
        self.attack_list = attack_list
        self.current_attack = self.attack_list[randint(0, len(attack_list) - 1)]

    def take_damage(self, player_damage: int):
        assets.SFX_MASTER.audios["player_attack"].play()
        self.current_hp = max(0, self.current_hp - player_damage)

    def change_attack(self, enemy_group: pygame.sprite.Group) -> EnemyAttack:
        enemy_group.empty()
        print(enemy_group)
        self.current_attack.projectiles.clear()

        E_ATTACK = self.attack_list[randint(0, len(self.attack_list) - 1)]
        self.current_attack = E_ATTACK
        for proj in E_ATTACK.projectiles:
            enemy_group.add(proj)

        print(enemy_group)
        return self.current_attack
