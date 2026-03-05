import pygame
import numpy as np


# CONFIG GENERAL

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 500
FPS = 30

# COLOR

BLANCO = (245, 245, 245)
GRIS = (170, 170, 170)
AZUL = (40, 120, 255)
VERDE = (0, 200, 0)
AMARILLO = (240, 200, 0)
ROJO = (220, 0, 0)

# CICLO DEL SEMAFORO

CICLO_SEMAFORO = 90
TICKS_VERDE = 30
TICKS_AMARILLO = 30
TICKS_ROJO = 30

# PARAMETROS DE MOVIMIENTO

aceleracion = 0.5
frenado = 1
distancia_colision = 90
distancia_semaforo = 100


# ==============================
# FUNCIONES DEL SEMÁFORO
# ==============================

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


# ==============================
# FUNCIONES MATEMÁTICAS
# ==============================

def distancia(punto1, punto2):
    diferencia = punto1 - punto2
    return np.sqrt(diferencia[0]**2 + diferencia[1]**2)


def dibujar_carro(pantalla, posicion, ancho=40, alto=20, color=AZUL):
    esquina_x = posicion[0] - ancho/2
    esquina_y = posicion[1] - alto/2
    rectangulo = pygame.Rect(esquina_x, esquina_y, ancho, alto)
    pygame.draw.rect(pantalla, color, rectangulo)