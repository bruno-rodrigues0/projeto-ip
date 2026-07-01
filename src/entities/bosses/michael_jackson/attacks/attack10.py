import pygame

from core import assets

from entities.enemy_attack import EnemyAttack, Projectile


class DiagonalLaser(Projectile):

    def __init__(self, image, x, y, direcao_x, direcao_y):
        super().__init__(image, x, y)
        self.orig_img = image
        self.dir_x = direcao_x
        self.dir_y = direcao_y
        self.fase_grossa = False


    def move(self, dt: float, estagio: float) -> None:

        if estagio < 1.0:
            self.ax += self.dir_x * 400 * dt
            self.ay += self.dir_y * 400 * dt

        elif 1.0 <= estagio < 1.8:
            pass


        elif estagio >= 1.8 and not self.fase_grossa:
            largura = self.orig_img.get_width() * 10
            altura = self.orig_img.get_height() * 10
            self.image = pygame.transform.scale(self.orig_img, (largura, altura)).convert_alpha()
            self.x -= (largura - self.orig_img.get_width()) // 2
            self.y -= (altura - self.orig_img.get_height()) // 2
            self.fase_grossa = True


class Attack10(EnemyAttack):
    attack_time = 4
    running_time = 0.0


    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0
        self.create_projectiles()


    def create_projectiles(self) -> None:

        self.projectiles.append(DiagonalLaser(assets.S_LASER_D1, 279, 100, 1, 1))
        self.projectiles.append(DiagonalLaser(assets.S_LASER_D2, 723, 100, -1, 1))


    def update(self, dt: float) -> None:
        self.running_time += dt

        for proj in self.projectiles:

            if isinstance(proj, DiagonalLaser):

                proj.move(dt, self.running_time)

            proj.update(dt)