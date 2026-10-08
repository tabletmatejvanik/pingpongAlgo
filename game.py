import pygame

pygame.init()

# Window
WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Pong")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Main loop
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    window.fill(BLACK)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()