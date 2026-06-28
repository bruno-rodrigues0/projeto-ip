import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class Projectile01(Projectile):
    def move(self, dt:float):
        self.ax -= 240 * dt
        self.ay += 60 * dt


class Projectile02(Projectile):
    def move(self, dt:float):
        self.ax -= 600 * dt
        self.ay += 180.5 * dt


class Projectile03(Projectile):
    def move(self, dt:float):
        self.ax -= 480 * dt
        self.ay -= 240 * dt


class Projectile04(Projectile):
    def move(self, dt:float):
        self.ax += 300 * dt
        self.ay -= 120 * dt


class Projectile05(Projectile):
    def move(self, dt:float):
        self.ax += 540 * dt
        self.ay -= 30 * dt


class Projectile06(Projectile):
    def move(self, dt:float):
        self.ax += 180 * dt
        self.ay += 120 * dt


class Attack02(EnemyAttack):
    initial_time: int
    attack_time = 3
    running_time = 0.0

    def __init__(self) -> None:
        super().__init__()
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
            proj.move(dt)
            proj.update(dt)

