import pygame
import math
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile
import core.constants as const


class ProjectileBounce(Projectile):
    def __init__(self, image, x, y, vx, vy):
        super().__init__(image, x, y)
        self.vx = vx  # funciona! SimulatedObject usa vx/vy diretamente
        self.vy = vy

    def move(self, factor=1):
        left = 490
        right = 710
        top = 307
        bottom = 527

        margin   = 150
        strength = 400

        self.ax = 0
        self.ay = 0

        if self.x < left + margin:
            self.ax += strength * (1 - (self.x - left) / margin) * factor
        if self.x > right - margin:
            self.ax -= strength * (1 - (right - self.x) / margin) * factor
        if self.y < top + margin:
            self.ay += strength * (1 - (self.y - top) / margin) * factor
        if self.y > bottom - margin:
            self.ay -= strength * (1 - (bottom - self.y) / margin) * factor


class Attack05(EnemyAttack):
    attack_time = 10
    running_time: float = 0.0

    def __init__(self):
        super().__init__()
        self.running_time = 0.0
        self.create_projectiles()

    def create_projectiles(self):
        left = 450 # 490
        right = 760 # 710
        top = 257 # 307
        bottom = 587 # 527
        cx = (left + right) // 2
        cy = (top + bottom) // 2

        spawns = [
            (left, cy, 250, 100),
            (right, cy, -200, 150),
            (cx, bottom, 180, -250),
            (cx, top, -100, 200),
            (left, top, 220, 80),
            (right, bottom, -250, -180),
            (right, top,    -200,  200)
        ]
        for x, y, vx, vy in spawns:
            self.projectiles.append(
                ProjectileBounce(assets.S_CIRCLE_ATTACK, x, y, vx, vy)
            )

    def update(self, dt: float):
        self.running_time += dt
        for proj in self.projectiles:
            if self.running_time < 1:
                proj.move(0.3)
            else:
                proj.move()
            proj.update(dt)
