import pygame

class SimulatedObject(pygame.sprite.Sprite):
    x: float
    y: float
    vx: float = 0
    vy: float = 0
    ax: float = 0
    ay: float = 0

    def __init__(self, image: pygame.surface.Surface, x: float, y: float) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float) -> None:
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        assert self.image is not None
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def get_pos(self) -> tuple[float, float]:
        return (self.x, self.y)

    def get_next_pos(self, dt: float) -> tuple[float, float]:
        return (self.x + self.vx * dt, self.y + self.vy * dt)
