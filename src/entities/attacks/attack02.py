import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class Projectile01(Projectile):
    def move(self):
        self.ax -= 4
        self.ay += 1


class Projectile02(Projectile):
    def move(self):
        self.ax -= 10
        self.ay += 3.5


class Projectile03(Projectile):
    def move(self):
        self.ax -= 8
        self.ay -= 4


class Projectile04(Projectile):
    def move(self):
        self.ax += 5
        self.ay -= 2


class Projectile05(Projectile):
    def move(self):
        self.ax += 9
        self.ay -= 0.5


class Projectile06(Projectile):
    def move(self):
        self.ax += 3
        self.ay += 2


class Attack02(EnemyAttack):
    initial_time: int
    attack_time = 3
    running_time = 0.0

    def __init__(self) -> None:
        self.initial_time = pygame.time.get_ticks()
        self.create_projectiles()


    def create_projectiles(self) -> None:
        self.projectiles.append(Projectile01(assets.S_HEE_HEE_ATTACK, 800, 320))
        self.projectiles.append(Projectile02(assets.S_HEE_HEE_ATTACK, 820, 380))
        self.projectiles.append(Projectile03(assets.S_AUW_ATTACK, 810, 440))
        self.projectiles.append(Projectile04(assets.S_AUW_ATTACK, 400, 430))
        self.projectiles.append(Projectile05(assets.S_HEE_HEE_ATTACK, 410, 370))
        self.projectiles.append(Projectile06(assets.S_AUW_ATTACK, 390, 310))


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move()
            proj.update(dt)
        
