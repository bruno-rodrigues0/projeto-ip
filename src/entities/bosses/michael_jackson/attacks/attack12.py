import math
import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class HomingProjectile(Projectile):
    max_speed = 350
    min_speed = 60
    turn_rate = math.radians(220)  # graus por segundo que ele consegue virar

    def __init__(self, image: pygame.surface.Surface, x: float, y: float, angle: float) -> None:
        super().__init__(image, x, y)
        # velocidade inicial já na direção do ângulo de disparo
        self.vx = math.cos(angle) * self.max_speed
        self.vy = math.sin(angle) * self.max_speed

    def move(self, dt: float) -> None:
        from scenes.context import Context  # import local pra evitar import circular

        if Context.PLAYER is None:
            return

        player_x, player_y = Context.PLAYER.get_pos()
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return

        # Ângulo atual do movimento e ângulo desejado (na direção do jogador)
        current_angle = math.atan2(self.vy, self.vx)
        desired_angle = math.atan2(dy, dx)

        # Diferença entre os dois ângulos, normalizada entre -pi e pi
        angle_diff = (desired_angle - current_angle + math.pi) % (2 * math.pi) - math.pi

        # Limita o quanto o projétil pode virar nesse frame
        max_turn = self.turn_rate * dt
        turn = max(-max_turn, min(max_turn, angle_diff))
        new_angle = current_angle + turn

        # Velocidade atual (escalar)
        current_speed = math.hypot(self.vx, self.vy)

        # Quanto maior o ângulo restante pra virar, mais desacelera (o "drift")
        turn_factor = abs(angle_diff) / math.pi  # 0 = alinhado, 1 = totalmente oposto
        target_speed = self.max_speed - (self.max_speed - self.min_speed) * turn_factor

        # Suaviza a mudança de velocidade também, pra não ser instantâneo
        speed_change_rate = 300  # unidades de velocidade por segundo
        if current_speed < target_speed:
            current_speed = min(current_speed + speed_change_rate * dt, target_speed)
        else:
            current_speed = max(current_speed - speed_change_rate * dt, target_speed)

        self.vx = math.cos(new_angle) * current_speed
        self.vy = math.sin(new_angle) * current_speed
        self.ax = 0
        self.ay = 0


class Attack12(EnemyAttack):
    initial_time: int
    attack_time = 6

    def __init__(self) -> None:
        super().__init__()
        self.initial_time = pygame.time.get_ticks()
        self.create_projectiles()

    def create_projectiles(self) -> None:
        spawn_points = [
            (300, 350, math.radians(0)),
            (850, 350, math.radians(180)),
            (300, 480, math.radians(0)),
            (850, 480, math.radians(180)),
        ]
        for x, y, angle in spawn_points:
            projectile = HomingProjectile(assets.S_CIRCLE_ATTACK, x, y, angle)
            self.projectiles.append(projectile)

    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)