import pygame
import numpy as np
import math

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

P0 = np.array([100, 300])
P1 = np.array([400, 100])
P2 = np.array([700, 300])


def bezier(t, p0, p1, p2):
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2


def bezier_tangente(t, p0, p1, p2):
    return 2 * (1 - t) * (p1 - p0) + 2 * t * (p2 - p1)


pygame.init()
pygame.display.set_caption("Bézier curves")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()

step = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Dibujar la curva completa
    points = [bezier(i / 50, P0, P1, P2) for i in range(51)]
    pygame.draw.lines(screen, (100, 100, 100), False, points, 2)

    # Animar un círculo a lo largo de la curva
    step += 1
    if step > 50:
        step = 0
    center = bezier(step / 50, P0, P1, P2) + [0, 1]
    pygame.draw.circle(screen, (0, 200, 200), center, 10)

    # Calcular ángulo de la tangente en la posición actual
    tangente = bezier_tangente(step / 50, P0, P1, P2)
    angulo = math.atan2(tangente[1], tangente[0])

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
