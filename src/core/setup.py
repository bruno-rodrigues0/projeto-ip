import pygame
import core.constants as const

# faz o setup inicial do pygame
pygame.init()
pygame.font.init()
window: pygame.Surface = pygame.display.set_mode(**const.WINDOW_SETUP)
clock: pygame.time.Clock = pygame.time.Clock()

