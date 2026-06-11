from dataclasses import dataclass
import pygame

@dataclass
class GameObject:
    pos = pygame.Vector2(0, 0)

    def get_center(self) -> pygame.Vector2:
        return pygame.Vector2(self.pos.x / 2, self.pos.y / 2)

    def get_pos(self) -> pygame.Vector2:
        return self.pos



