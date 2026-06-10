from dataclasses import dataclass

import pygame

class Rect:
    pass

@dataclass
class GameObject:
    pos = pygame.Vector2(0, 0)
    vel = pygame.Vector2(1, 1)
    acc = pygame.Vector2(1, 1)

    def update(self, dt: float) -> None:
        self.vel.x += self.acc.x * dt
        self.vel.y += self.acc.y * dt
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

    def get_center(self) -> pygame.Vector2:
        return pygame.Vector2(self.pos.x / 2, self.pos.y / 2)

    def get_pos(self) -> pygame.Vector2:
        return self.pos



