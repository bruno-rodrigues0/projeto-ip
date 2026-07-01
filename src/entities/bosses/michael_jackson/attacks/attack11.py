import pygame

import math

from entities.enemy_attack import EnemyAttack, Projectile


class HalfMoonLaser(Projectile):

    def __init__(self, t_start, start_x, start_y, end_x, end_y):
        self.size = 180
        self.img_thin = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.img_thick = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        pygame.draw.arc(self.img_thin, (255, 255, 255), (0, 0, self.size, self.size), 0, math.pi * 2, 2)
        pygame.draw.arc(self.img_thick, (255, 255, 255), (0, 0, self.size, self.size), 0, math.pi * 2, 60)

        super().__init__(self.img_thin, start_x, start_y)

        self.start_x = start_x
        self.start_y = start_y
        self.target_x = end_x
        self.target_y = end_y

        self.t_spawn = t_start
        self.t_move = t_start + 0.5
        self.t_warn = self.t_move + 0.5
        self.t_attack = self.t_warn + 1.8


    def move(self, dt: float, running_time=0.0):
        if running_time < self.t_spawn or running_time >= self.t_attack:
            self.x = self.y = -2000

            if hasattr(self, 'rect') and self.rect:
                self.rect.x = self.rect.y = -2000
            return

        if running_time < self.t_move:
            self.image = self.img_thin

        else:
            self.image = self.img_thick

        if running_time >= self.t_warn:
            self.x, self.y = self.target_x, self.target_y

        else:
            local_time = max(0.0, running_time - self.t_move)
            pct = min(1.0, local_time / 0.5)

            self.x = self.start_x + (self.target_x - self.start_x) * pct
            self.y = self.start_y + (self.target_y - self.start_y) * pct

        if hasattr(self, 'rect') and self.rect:
            self.rect.x, self.rect.y = int(self.x), int(self.y)


class Attack11(EnemyAttack):
    attack_time = 5
    running_time = 0.0

    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0

        self.projectiles.append(HalfMoonLaser(0.0, start_x=310, start_y=180, end_x=580, end_y=390))
        self.projectiles.append(HalfMoonLaser(3.5, start_x=715, start_y=180, end_x=280, end_y=390))


    def update(self, dt: float):
        self.running_time += dt

        for proj in self.projectiles:
            if hasattr(proj, 'move'):
                proj.move(dt, self.running_time)

            proj.update(dt)