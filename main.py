import pygame
import numpy as np


#config de pantalla 
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 500
FPS = 30

#colores
BLANCO = (245, 245, 245)
GRIS = (170, 170, 170)
AZUL = (40, 120, 255)
VERDE = (0, 200, 0)
AMARILLO = (240, 200, 0)
ROJO = (220, 0, 0)

#ciclos semaforos

CICLO_SEMAFORO = 90
TICKS_VERDE = 30
TICKS_AMARILLO = 30
TICKS_ROJO = 30

#parametros movimiento

aceleracion = 0.5
frenado = 1
distancia_colision = 90
distancia_semaforo = 100


#semaforo

def obtener_estado_semaforo(contador):
    contador = contador % CICLO_SEMAFORO
    if contador < TICKS_VERDE:
        return "verde"
    elif contador < TICKS_VERDE + TICKS_AMARILLO:
        return "amarillo"
    else:
        return "rojo"


def obtener_color_semaforo(estado):
    if estado == "verde":
        return VERDE
    elif estado == "amarillo":
        return AMARILLO
    else:
        return ROJO


#posiciones y dibujo de carro

def distancia(punto1, punto2):
    diferencia = punto1 - punto2
    return np.sqrt(diferencia[0]**2 + diferencia[1]**2)


def dibujar_carro(pantalla, posicion, ancho=40, alto=20, color=AZUL):
    esquina_x = posicion[0] - ancho/2
    esquina_y = posicion[1] - alto/2
    rectangulo = pygame.Rect(esquina_x, esquina_y, ancho, alto)
    pygame.draw.rect(pantalla, color, rectangulo)

    #carros data

numero_carros = 2

posiciones = np.array([
    [0.0, ALTO_PANTALLA / 2],
    [150.0, ALTO_PANTALLA / 2]
], dtype=float)

velocidades = np.array([0.0, 3.0], dtype=float)
velocidades_maximas = np.array([6.0, 7.0], dtype=float)

#info semaforo

posicion_semaforo = np.array(
    [ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2],
    dtype=float
)

contador_semaforo = 0
estado_semaforo = "verde"

#MAIN

pygame.init()
pygame.display.set_caption("Etapa 1 - Simulación de Tráfico")
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
reloj = pygame.time.Clock()

ejecutar = True
while ejecutar:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutar = False

    contador_semaforo = (contador_semaforo + 1) % CICLO_SEMAFORO
    estado_semaforo = obtener_estado_semaforo(contador_semaforo)

    #movimiento del cochecito

    for i in range(numero_carros):

        debe_frenar = False

        # Semáforo
        distancia_al_semaforo = distancia(posiciones[i], posicion_semaforo)
        esta_cerca_semaforo = distancia_al_semaforo < distancia_semaforo
        esta_antes_semaforo = posiciones[i][0] < posicion_semaforo[0]

        if estado_semaforo == "rojo" and esta_cerca_semaforo and esta_antes_semaforo:
            debe_frenar = True

        # Colisiones
        for j in range(numero_carros):
            if i != j and posiciones[j][0] > posiciones[i][0]:
                distancia_a_otro = posiciones[j][0] - posiciones[i][0]
                if distancia_a_otro < distancia_colision:
                    debe_frenar = True

        # Velocidad
        if debe_frenar:
            velocidades[i] -= frenado
            if velocidades[i] < 0:
                velocidades[i] = 0
        else:
            velocidades[i] += aceleracion
            if velocidades[i] > velocidades_maximas[i]:
                velocidades[i] = velocidades_maximas[i]

        # Posición
        posiciones[i][0] += velocidades[i]

        # Reinicio de posición
        if posiciones[i][0] > ANCHO_PANTALLA + 40:
            posiciones[i][0] = -40

    #dibujo

    pantalla.fill(BLANCO)

    y_carretera = ALTO_PANTALLA / 2
    pygame.draw.line(pantalla, GRIS, (0, y_carretera), (ANCHO_PANTALLA, y_carretera), 4)

    # Semáforo
    color_semaforo = obtener_color_semaforo(estado_semaforo)

    pygame.draw.circle(
        pantalla,
        (210, 210, 210),
        (int(posicion_semaforo[0]), int(posicion_semaforo[1])),
        distancia_semaforo,
        1
    )

    pygame.draw.circle(
        pantalla,
        color_semaforo,
        (int(posicion_semaforo[0]), int(posicion_semaforo[1])),
        12,
        0
    )

    # Carros
    colores = np.array([AZUL, (255, 100, 0)], dtype=object)

    for i in range(numero_carros):
        dibujar_carro(pantalla, posiciones[i], color=colores[i])

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()