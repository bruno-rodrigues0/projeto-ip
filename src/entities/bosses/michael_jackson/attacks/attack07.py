import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class ZigZagProjectile(Projectile):


    def __init__(self, image, x, y, speed_x, speed_y):
        super().__init__(image, x, y)
        self.ax = float(x)
        self.ay = float(y)
        self.speed_x = speed_x
        self.speed_y = speed_y


    def move(self, dt: float):
        self.ax += self.speed_x * dt
        self.ay += self.speed_y * dt

        if self.ay <= 300:
            self.speed_y = abs(self.speed_y)
        elif self.ay >= 500:
            self.speed_y = -abs(self.speed_y)

        if self.ax <= 450:
            self.speed_x = abs(self.speed_x)
        elif self.ax >= 750:
            self.speed_x = -abs(self.speed_x)


    def update(self, dt: float):
        self.rect.x = int(self.ax)
        self.rect.y = int(self.ay)


class Attack07(EnemyAttack):
    def __init__(self, arena_rect=None) -> None:
        super().__init__()
        self.attack_time = 6


        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 400, 380, 145, 145))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 350, 390, 200, -150))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 390, 300, 155, 255))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 420, 310, 160, -160))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 380, 320, 205, 265))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 350, 330, 170, -170))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 410, 240, 175, 275))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 400, 350, 200, -180))


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)
