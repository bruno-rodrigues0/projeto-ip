#assets

'''
#laser funcional?
def create_laser_surface(width=100, height=8):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 50, 50), (0, 0, width, height))
    pygame.draw.rect(surface, (255, 255, 255), (0, 2, width, height - 4))
    return surface

def create_vertical_laser(width=10, height=200):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height))
    return surface

def create_diagonal_laser_1(size=200, thickness=10):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.line(surface, (255, 255, 255), (0, 0), (size, size), thickness)
    return surface

def create_diagonal_laser_2(size=200, thickness=10):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.line(surface, (255, 255, 255), (0, size), (size, 0), thickness)
    return surface

S_LASER = create_laser_surface(120, 10)

S_LASER_H_WHITE = pygame.Surface((200, 10))
S_LASER_H_WHITE.fill((255, 255, 255))

S_LASER_V = create_vertical_laser(10, 200)
S_LASER_D1 = create_diagonal_laser_1(200, 10)
S_LASER_D2 = create_diagonal_laser_2(200, 10)

S_HALF_MOON_THIN = pygame.Surface((180, 180), pygame.SRCALPHA)
S_HALF_MOON_THICK = pygame.Surface((180, 180), pygame.SRCALPHA)
pygame.draw.arc(S_HALF_MOON_THIN, (255, 255, 255), (0, 0, 180, 180), 0, math.pi * 2, 2)
pygame.draw.arc(S_HALF_MOON_THICK, (255, 255, 255), (0, 0, 180, 180), 0, math.pi * 2, 60)
'''


#questão 7

'''
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
        self.move(dt)
        self.rect.x = int(self.ax)
        self.rect.y = int(self.ay)


class Attack07(EnemyAttack):
    def __init__(self, arena_rect=None) -> None:
        super().__init__()
        self.attack_time = 6


        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 400, 380, 145, 145))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 350, 390, 300, -150))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 390, 300, 155, 255))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 420, 310, 160, -160))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 380, 320, 405, 265))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 350, 330, 170, -170))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 410, 240, 175, 375))
        self.projectiles.append(ZigZagProjectile(assets.S_CIRCLE_ATTACK, 400, 350, 200, -180))


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.update(dt)
'''

#questão 8

'''
import pygame
import math
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


S_LASER = pygame.Surface((40, 10))
S_LASER.fill((255, 255, 255))


class LaserProjectile(Projectile):

    def move(self, dt: float, factor=1):
        self.ax -= 150 * factor * dt
        self.ay = 0


class Attack08(EnemyAttack):
    attack_time = 6
    running_time: float = 0.0


    def __init__(self) -> None:
        super().__init__()
        self.running_time = 0.0
        self.create_projectiles()


    def create_projectiles(self) -> None:
    
        for i in range(50):
        
            x = 1200 + (i * 90)
            y = int(400 + math.sin(i) * 160)
        
            self.projectiles.append(LaserProjectile(S_LASER, x, y))


    def update(self, dt: float) -> None:
    
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)

        self.running_time += dt
'''

#questão 9

'''
import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile
from random import choice

class ProjectileChuva(Projectile):

    def __init__(self, image, x, y):

        super().__init__(image, x, y)

    def move(self, dt: float) -> None:
        self.ay += 120 * dt


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


    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)
'''

#questão 10

'''
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
            # Passa o tempo de execução para o projétil saber o que fazer
            if isinstance(proj, DiagonalLaser):
                proj.move(dt, self.running_time)
            proj.update(dt) 
'''

#questão 11

'''
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
        self.t_warn = self.t_move + 0.6
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
            pct = min(1.0, local_time / 0.6)
            
            self.x = self.start_x + (self.target_x - self.start_x) * pct
            self.y = self.start_y + (self.target_y - self.start_y) * pct
            
        if hasattr(self, 'rect') and self.rect: 
            self.rect.x, self.rect.y = int(self.x), int(self.y)


class Attack11(EnemyAttack):
    attack_time = 6
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
'''
