import numpy as np
import pygame
from config import AZUL, ACELERACION, FRENADO, DISTANCIA_COLISION, DISTANCIA_SEMAFORO, ANCHO_PANTALLA


class Carro:
    def __init__(self, x, y, velocidad_inicial, velocidad_maxima, color=AZUL, ancho=40, alto=20):
        self.posicion = np.array([x, y], dtype=float)
        self.velocidad = velocidad_inicial
        self.velocidad_maxima = velocidad_maxima
        self.color = color
        self.ancho = ancho
        self.alto = alto

    # Logica movimiento
    def _debe_frenar(self, semaforo, otros_carros):
        dist_sem = self._distancia(self.posicion, semaforo.posicion)
        cerca = dist_sem < DISTANCIA_SEMAFORO
        antes = self.posicion[0] < semaforo.posicion[0]

        if semaforo.estado == "rojo" and cerca and antes:
            return True

        for otro in otros_carros:
            if otro is self:
                continue
            if otro.posicion[0] > self.posicion[0]:
                if otro.posicion[0] - self.posicion[0] < DISTANCIA_COLISION:
                    return True

        return False

    def actualizar(self, semaforo, otros_carros):
        if self._debe_frenar(semaforo, otros_carros):
            self.velocidad -= FRENADO
            if self.velocidad < 0:
                self.velocidad = 0
        else:
            self.velocidad += ACELERACION
            if self.velocidad > self.velocidad_maxima:
                self.velocidad = self.velocidad_maxima

        self.posicion[0] += self.velocidad

        # Reinicio al salir de pantalla
        if self.posicion[0] > ANCHO_PANTALLA + 40:
            self.posicion[0] = -40

# ------------------------------------------------------------!
    # Dibujar con matriz de rotación (etapa 2)
# -----------------------------------------------------------!
    def dibujar(self, pantalla, angulo=0):
        vertices = np.array([
            [-self.ancho / 2, -self.alto / 2],
            [ self.ancho / 2, -self.alto / 2],
            [ self.ancho / 2,  self.alto / 2],
            [-self.ancho / 2,  self.alto / 2]
        ])

        rad = np.radians(angulo)
        R = np.array([
            [np.cos(rad), -np.sin(rad)],
            [np.sin(rad),  np.cos(rad)]
        ])

        rotado     = vertices @ R.T
        trasladado = rotado + self.posicion

        pygame.draw.polygon(pantalla, self.color, trasladado)


    def _distancia(self, p1, p2):
        d = p1 - p2
        return np.sqrt(d[0] ** 2 + d[1] ** 2)
