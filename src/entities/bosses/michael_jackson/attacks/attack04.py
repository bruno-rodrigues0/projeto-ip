import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile

# ! CONSERTAR ESSE ATAQUE
class ProjectileUp01(Projectile):
    def move(self, dt:float, factor=1):
        self.ax -= 120 * factor * dt
        self.ay -= 480 * factor * dt


class ProjectileUp02(Projectile):
    def move(self, dt:float, factor=1):
        self.ax += 120 * factor * dt
        self.ay -= 600 * factor * dt


class ProjectileUp03(Projectile):
    def move(self, dt:float, factor=1):
        self.ax -= 240 * factor * dt
        self.ay -= 420 * factor * dt


class ProjectileUp04(Projectile):
    def move(self, dt:float, factor=1):
        self.ax += 240 * factor * dt
        self.ay -= 540 * factor * dt


class Attack04(EnemyAttack):
    attack_time = 6
    running_time: float = 0.0

    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0
        self.create_projectiles()

    def create_projectiles(self) -> None:
        self.projectiles.append(ProjectileUp01(assets.S_CIRCLE_ATTACK, 500, 550))
        self.projectiles.append(ProjectileUp02(assets.S_CIRCLE_ATTACK, 550, 550))
        self.projectiles.append(ProjectileUp03(assets.S_CIRCLE_ATTACK, 650, 550))
        self.projectiles.append(ProjectileUp04(assets.S_CIRCLE_ATTACK, 700, 550))

    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            if self.running_time < 0.65:
                proj.move(dt, 2)
            elif 0.7 <= self.running_time < 1.93:
                proj.move(dt, -3)
            elif 2.1 <= self.running_time < 3.2:
                proj.ax += 2
                proj.move(dt, 6.5)
            elif 3 <= self.running_time < 3.95:
                proj.ax -= 16.5
                proj.move(dt, -15.5)
            elif 4 <= self.running_time:
                proj.ax += 40
                proj.move(dt, 20)


            proj.update(dt)

        self.running_time += dt
