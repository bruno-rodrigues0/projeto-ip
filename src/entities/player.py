from entities.game_object import GameObject
import pygame

class Player(GameObject):
    
    def __init__(self, surface: pygame.Surface, dim: pygame.Vector2):
        rect = pygame.Rect(self.pos.x, self.pos.y, dim.x, dim.y)
        pygame.draw.rect(surface, "red", rect)
