import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile
from components.animation import AnimationPlayer


class Moonwalk01(Projectile):
    def move(self, dt:float) -> None:
        self.vx = 150

    def update(self, dt: float, animation: AnimationPlayer) -> None:
        super().update(dt)
        animation.update(dt)
        self.image = pygame.transform.flip(animation.get_frame(), True, False).convert_alpha()

class Moonwalk02(Projectile):
    def move(self, dt:float) -> None:
        self.vx = -150

    def update(self, dt: float, animation: AnimationPlayer) -> None:
        super().update(dt)
        animation.update(dt)
        self.image = pygame.transform.flip(animation.get_frame(), False, True).convert_alpha()

class Attack06(EnemyAttack):
    initial_time: int
    attack_time = 5
    animation = AnimationPlayer("moonwalk", assets.S_MOONWALK_ATTACK, .2)

    def __init__(self) -> None:
        super().__init__()
        self.initial_time = pygame.time.get_ticks()
        self.create_projectiles()

    def create_projectiles(self) -> None:
        for i in range(10):
            if i < 5:
                projectile = Moonwalk01(pygame.Surface((0, 0)), 350 - (120 * i), 410)
            else:
                projectile = Moonwalk02(pygame.Surface((0, 0)), 850 + (120 * (i - 5)), 310)
            self.projectiles.append(projectile)


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt, self.animation)
