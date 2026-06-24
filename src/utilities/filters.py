import pygame


def chromatic_distortion(surface: pygame.Surface, offset_x:int=3, offset_y:int=0):
    """
    Aplica aberração cromática deslocando os canais Vermelho e Azul.
    """
    width, height = surface.get_size()

    red = pygame.Surface((width, height))
    green = pygame.Surface((width, height))
    blue = pygame.Surface((width, height))

    red.blit(surface, (0, 0))
    green.blit(surface, (0, 0))
    blue.blit(surface, (0, 0))

    red.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
    green.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
    blue.fill((0, 0, 255), special_flags=pygame.BLEND_RGB_MULT)

    filtered = pygame.Surface((width, height))

    filtered.blit(red, (-offset_x, -offset_y))
    filtered.blit(green, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    filtered.blit(blue, (offset_x, offset_y), special_flags=pygame.BLEND_RGB_ADD)

    return filtered

def create_crt_mask(width: int, height: int) -> pygame.Surface:
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 4):
        pygame.draw.line(mask, (0, 0, 0, 90), (0, y), (width, y), 2)
    return mask
