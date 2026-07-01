import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class ProjectileChuva(Projectile):
    vy = 200

    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def move(self, dt: float) -> None:
        self.ay += 40 * dt


class Attack09(EnemyAttack):
    attack_time = 4
    running_time = 0.0

    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0
        self.create_projectiles()


    def create_projectiles(self) -> None:

        self.projectiles.append(ProjectileChuva(assets.S_AYUWOKI_ATTACK, 500, 150))
        self.projectiles.append(ProjectileChuva(assets.S_HEE_HEE_ATTACK, 560, 40))
        self.projectiles.append(ProjectileChuva(assets.S_SMOOTH_ATTACK, 620, -70))
        self.projectiles.append(ProjectileChuva(assets.S_CRIMINAL_ATTACK, 500, -180))
        self.projectiles.append(ProjectileChuva(assets.S_AYUWOKI_ATTACK, 600, -280))
        self.projectiles.append(ProjectileChuva(assets.S_SMOOTH_ATTACK, 500, -380))


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)
