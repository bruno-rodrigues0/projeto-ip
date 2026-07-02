import random
import math
import pygame
from core import assets
import core.constants as const
from entities.enemy_attack import EnemyAttack, Projectile


def make_circle_surface(radius: int, color) -> pygame.Surface:
    size = max(radius * 2, 1)
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (size // 2, size // 2), radius)
    return surf


class Bomb(Projectile):
    bomb_radius = 8
    max_radius = 50
    explosion_grow_time = 0.35   # quanto tempo o raio demora pra crescer até o máximo
    explosion_hold_time = 0.15   # quanto tempo fica no tamanho máximo (ainda perigoso)

    def __init__(self, image: pygame.surface.Surface, x: float, y: float, fuse_time: float) -> None:
        super().__init__(image, x, y)
        self.center_x = x + self.bomb_radius
        self.center_y = y + self.bomb_radius
        self.fuse_time = fuse_time
        self.timer = 0.0
        self.state = "fuse"  # fuse -> exploding -> holding -> done
        self.blink_timer = 0.0
        self.visible = True

    def move(self, dt: float) -> None:
        pass  # a bomba não se move, só fica parada esperando explodir

    def update(self, dt: float) -> None:
        self.timer += dt

        if self.state == "fuse":
            self.blink_timer += dt
            if self.blink_timer >= 0.15:
                self.blink_timer = 0.0
                self.visible = not self.visible
            color = const.WHITE if self.visible else (0, 0, 0, 0)
            self._set_image(make_circle_surface(self.bomb_radius, color))
            if self.timer >= self.fuse_time:
                self.state = "exploding"
                self.timer = 0.0
            return

        if self.state == "exploding":
            progress = min(self.timer / self.explosion_grow_time, 1.0)
            radius = int(self.bomb_radius + (self.max_radius - self.bomb_radius) * progress)
            self._set_image(make_circle_surface(radius, (255, 80, 0)))
            if self.timer >= self.explosion_grow_time:
                self.state = "holding"
                self.timer = 0.0
            return

        if self.state == "holding":
            self._set_image(make_circle_surface(self.max_radius, (255, 80, 0)))
            if self.timer >= self.explosion_hold_time:
                self.state = "done"
                self.timer = 0.0
            return

        # state == "done": some invisível, sem dano
        self._set_image(make_circle_surface(1, (0, 0, 0, 0)))

    def _set_image(self, surface: pygame.Surface) -> None:
        self.image = surface
        size = surface.get_width()
        self.x = self.center_x - size / 2
        self.y = self.center_y - size / 2
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)


import core.constants as const

class Attack13(EnemyAttack):
    initial_time: int
    attack_time = 5

    def __init__(self) -> None:
        super().__init__()
        self.initial_time = pygame.time.get_ticks()
        self.create_projectiles()

    def create_projectiles(self) -> None:
        from scenes.states.fight import ARENA_RECT  # import local, evita import circular

        margin = 40  # distância mínima da borda da arena
        min_distance = 45  # distância mínima entre bombas (evita sobreposição)
        safe_zone_radius = 55  # área livre no centro, onde o jogador nasce

        min_x = ARENA_RECT.left + margin
        max_x = ARENA_RECT.right - margin
        min_y = ARENA_RECT.top + margin
        max_y = ARENA_RECT.bottom - margin
        center_x, center_y = ARENA_RECT.center

        bomb_count = 7
        positions = []
        attempts = 0

        while len(positions) < bomb_count and attempts < 200:
            attempts += 1
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)

            # Evita nascer em cima de onde o jogador começa
            if math.hypot(x - center_x, y - center_y) < safe_zone_radius:
                continue

            # Evita nascer muito perto de outra bomba já posicionada
            too_close = any(
                math.hypot(x - px, y - py) < min_distance
                for px, py in positions
            )
            if too_close:
                continue

            positions.append((x, y))

        for x, y in positions:
            fuse_time = random.uniform(1.0, 2.2)
            bomb = Bomb(assets.S_CIRCLE_ATTACK, x, y, fuse_time)
            self.projectiles.append(bomb)

    def update(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)