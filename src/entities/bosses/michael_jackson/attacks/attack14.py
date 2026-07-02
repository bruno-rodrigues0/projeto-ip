import math
import random
import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


def make_warning_surface(radius: int, color) -> pygame.Surface:
    size = radius * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius, width=3)
    return surf


class WarningIndicator(Projectile):
    radius = 14
    warning_time = 0.45  # tempo de aviso antes do disparo real

    def __init__(self, image: pygame.surface.Surface, x: float, y: float, target_x: float, target_y: float) -> None:
        super().__init__(image, x, y)
        self.center_x = x
        self.center_y = y
        self.target_x = target_x
        self.target_y = target_y
        self.timer = 0.0
        self.blink_timer = 0.0
        self.visible = True
        self.ready = False

    def move(self, dt: float) -> None:
        pass

    def update(self, dt: float) -> None:
        self.timer += dt
        self.blink_timer += dt
        if self.blink_timer >= 0.08:
            self.blink_timer = 0.0
            self.visible = not self.visible

        color = (255, 60, 60) if self.visible else (0, 0, 0, 0)
        self.image = make_warning_surface(self.radius, color)
        self.x = self.center_x - self.radius
        self.y = self.center_y - self.radius
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.timer >= self.warning_time:
            self.ready = True


class LinearProjectile(Projectile):
    speed = 400

    def __init__(self, image: pygame.surface.Surface, x: float, y: float, target_x: float, target_y: float) -> None:
        super().__init__(image, x, y)
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy) or 1
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed

    def move(self, dt: float) -> None:
        pass


class Attack14(EnemyAttack):
    initial_time: int
    attack_time = 8
    spawn_interval = 0.5

    def __init__(self) -> None:
        super().__init__()
        self.initial_time = pygame.time.get_ticks()
        self.spawn_timer = 0.0

    def spawn_warning(self) -> None:
        from scenes.states.fight import ARENA_RECT
        from scenes.context import Context

        if Context.PLAYER is None:
            return

        target_x, target_y = Context.PLAYER.get_pos()
        edge = random.choice(["top", "bottom", "left", "right"])
        margin = 40

        if edge == "top":
            x = random.randint(ARENA_RECT.left, ARENA_RECT.right)
            y = ARENA_RECT.top - margin
        elif edge == "bottom":
            x = random.randint(ARENA_RECT.left, ARENA_RECT.right)
            y = ARENA_RECT.bottom + margin
        elif edge == "left":
            x = ARENA_RECT.left - margin
            y = random.randint(ARENA_RECT.top, ARENA_RECT.bottom)
        else:
            x = ARENA_RECT.right + margin
            y = random.randint(ARENA_RECT.top, ARENA_RECT.bottom)

        warning = WarningIndicator(assets.S_CIRCLE_ATTACK, x, y, target_x, target_y)
        self.projectiles.append(warning)

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer -= self.spawn_interval
            self.spawn_warning()

        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)

        # Avisos que já terminaram viram projéteis de verdade
        ready_warnings = [p for p in self.projectiles if isinstance(p, WarningIndicator) and p.ready]
        for w in ready_warnings:
            bullet = LinearProjectile(assets.S_CIRCLE_ATTACK, w.center_x, w.center_y, w.target_x, w.target_y)
            self.projectiles.append(bullet)
            self.projectiles.remove(w)

        # Limpeza de projéteis que já saíram da área jogável
        from scenes.states.fight import ARENA_RECT
        buffer = 150
        self.projectiles = [
            p for p in self.projectiles
            if isinstance(p, WarningIndicator) or (
                ARENA_RECT.left - buffer <= p.x <= ARENA_RECT.right + buffer
                and ARENA_RECT.top - buffer <= p.y <= ARENA_RECT.bottom + buffer
            )
        ]