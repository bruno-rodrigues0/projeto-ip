import pygame

_cache = {}

def chromatic_distortion(surface: pygame.Surface, offset_x: int = 3, offset_y: int = 0):
    width, height = surface.get_size()

    if 'red' not in _cache or _cache['red'].get_size() != (width, height):
        _cache['red'] = pygame.Surface((width, height)).convert()
        _cache['green'] = pygame.Surface((width, height)).convert()
        _cache['blue'] = pygame.Surface((width, height)).convert()
        _cache['filtered'] = pygame.Surface((width, height)).convert()

    red = _cache['red']
    green = _cache['green']
    blue = _cache['blue']
    filtered = _cache['filtered']


    red.blit(surface, (0, 0))
    green.blit(surface, (0, 0))
    blue.blit(surface, (0, 0))


    red.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
    green.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
    blue.fill((0, 0, 255), special_flags=pygame.BLEND_RGB_MULT)


    filtered.blit(red, (-offset_x, -offset_y))
    filtered.blit(green, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    filtered.blit(blue, (offset_x, offset_y), special_flags=pygame.BLEND_RGB_ADD)

    return filtered


def create_crt_mask(width: int, height: int) -> pygame.Surface:
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(0, height, 4):
        pygame.draw.line(mask, (0, 0, 0, 90), (0, y), (width, y), 2)
    return mask
