import math
import random
import pygame
from core import assets
from entities.enemy_attack import EnemyAttack, Projectile


class RingSegment(Projectile):
    """Um projétil que ocupa uma posição fixa (slot) em um anel giratório e encolhendo."""

    def __init__(self, image: pygame.surface.Surface, ring: "Ring", base_angle: float) -> None:
        self.ring = ring
        self.base_angle = base_angle
        self.half_w = image.get_width() / 2
        self.half_h = image.get_height() / 2
        x, y = self._compute_pos()
        super().__init__(image, x, y)

    def _compute_pos(self) -> tuple[float, float]:
        angle = self.base_angle + self.ring.rotation
        x = self.ring.center_x + math.cos(angle) * self.ring.radius - self.half_w
        y = self.ring.center_y + math.sin(angle) * self.ring.radius - self.half_h
        return x, y

    def move(self, dt: float) -> None:
        pass  # posição é controlada pelo update, seguindo o anel

    def update(self, dt: float) -> None:
        self.x, self.y = self._compute_pos()
        assert self.image is not None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class Ring:
    """Anel giratório com uma brecha fixa, que encolhe de raio até sumir."""

    rotation_speed = math.radians(35)

    def __init__(self, center_x: float, center_y: float, start_radius: float, num_slots: int, gap_slots: int, shrink_duration: float) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.start_radius = start_radius
        self.radius = start_radius
        self.num_slots = num_slots
        self.slot_angle = (2 * math.pi) / num_slots
        self.rotation = 0.0
        self.timer = 0.0
        self.shrink_duration = shrink_duration
        self.closed = False

        self.gap_slots = gap_slots
        self.gap_start = random.randint(0, num_slots - 1)

        self.segments: dict[int, RingSegment] = {}

    def slot_is_gap(self, slot_index: int) -> bool:
        offset = (slot_index - self.gap_start) % self.num_slots
        return offset < self.gap_slots

    def update(self, dt: float, image: pygame.surface.Surface) -> list["RingSegment"]:
        self.rotation += self.rotation_speed * dt
        self.timer += dt

        progress = min(self.timer / self.shrink_duration, 1.0)
        self.radius = self.start_radius * (1 - progress)
        if progress >= 1.0:
            self.closed = True

        new_segments = []
        for slot in range(self.num_slots):
            if self.slot_is_gap(slot):
                self.segments.pop(slot, None)
                continue
            if slot not in self.segments:
                bullet = RingSegment(image, self, slot * self.slot_angle)
                self.segments[slot] = bullet
                new_segments.append(bullet)

        return new_segments

    def all_bullets(self) -> list["RingSegment"]:
        return list(self.segments.values())


class Attack16(EnemyAttack):
    initial_time: int
    attack_time = 14

    base_radius = 220
    radius_step = 40
    base_num_slots = 14
    gap_slots = 3
    shrink_duration = 1.25  # segundos até o anel sumir de vez

    def __init__(self) -> None:
        super().__init__()
        self.initial_time = pygame.time.get_ticks()
        self.current_ring: Ring | None = None
        self.ring_count = 0
        self.spawn_new_ring()

    def spawn_new_ring(self) -> None:
        from scenes.states.fight import ARENA_RECT

        center_x, center_y = ARENA_RECT.center

        radius = self.base_radius + self.radius_step * self.ring_count
        num_slots = self.base_num_slots + self.ring_count * 2

        self.current_ring = Ring(center_x, center_y, radius, num_slots, self.gap_slots, self.shrink_duration)
        self.ring_count += 1

        self.projectiles = [p for p in self.projectiles if not isinstance(p, RingSegment)]

    def update(self, dt: float) -> None:
        if self.current_ring is None:
            self.spawn_new_ring()
            if self.current_ring is None:
                return

        new_segments = self.current_ring.update(dt, assets.S_CIRCLE_ATTACK)
        for seg in new_segments:
            self.projectiles.append(seg)

        active_ids = {id(seg) for seg in self.current_ring.all_bullets()}
        self.projectiles = [
            p for p in self.projectiles
            if not isinstance(p, RingSegment) or id(p) in active_ids
        ]

        for proj in self.projectiles:
            proj.move(dt)
            proj.update(dt)

        if self.current_ring.closed:
            self.spawn_new_ring()