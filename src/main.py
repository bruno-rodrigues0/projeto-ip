import pygame

from utils.constants import FPS, GAME_NAME, SCREEN_HEIGH, SCREEN_WIDTH, SCREEN_BG

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGH))
    pygame.display.set_caption(GAME_NAME)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SCREEN_BG)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

