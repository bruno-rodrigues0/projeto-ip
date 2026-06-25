import pygame

from core import assets
from entities.enemy_attack import EnemyAttack, Projectile

class Projectile01(Projectile):
    def move(self) -> None: # aqui vc pode inventar qualquer regra de movimentação
        self.ax += 5

# WARN ataque generico de exemplo
class Attack01(EnemyAttack):
    initial_time: int
    attack_time = 2 # em segundos, serve como alternativa para finished (se o tempo == attack_time, finaliza o turno)
    finished = False

    def __init__(self) -> None:
        self.initial_time = pygame.time.get_ticks()
        self.create_projectiles()

    def create_projectiles(self) -> None:
        for i in range(5):
            projectile = Projectile01(assets.S_ENEMY_ATTACK, 400 - 30 * i, 320 + 40 * i)
            projectile.ax = 20 * (i + 1)
            self.projectiles.append(projectile)

    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move()
            proj.update(dt)




