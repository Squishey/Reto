import math
import numpy as np
import pygame
from config import AZUL, ACELERACION, FRENADO, DISTANCIA_COLISION, DISTANCIA_SEMAFORO, ANCHO_PANTALLA


#Funciones de curva de Bézier cuadrática (adaptadas de curvas.py) ---

def bezier(t, p0, p1, p2):
    """Calcula la posición en la curva de Bézier cuadrática para el parámetro t ∈ [0, 1]."""
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2


def bezier_tangente(t, p0, p1, p2):
    """Derivada de la curva de Bézier: da el vector tangente en t, usado para calcular el ángulo."""
    return 2 * (1 - t) * (p1 - p0) + 2 * t * (p2 - p1)


class Carro:
    def __init__(self, x, y, velocidad_inicial, velocidad_maxima, color=AZUL, ancho=40, alto=20):
        self.posicion = np.array([x, y], dtype=float)
        self.velocidad = velocidad_inicial
        self.velocidad_maxima = velocidad_maxima
        self.color = color
        self.ancho = ancho
        self.alto = alto
        # Tramo curvo: se activa desde main.py asignando en_curva=True y curva_pts=(P0, P1, P2)
        self.en_curva = False
        self.curva_pts = None   # tupla (P0, P1, P2) con arrays de numpy
        self.t = 0.0            # parámetro de posición en la curva, va de 0 a 1

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

        # Transición automática: al llegar al inicio de la curva, activar modo curva
        if not self.en_curva and self.curva_pts is not None:
            if self.posicion[0] >= self.curva_pts[0][0]:
                self.en_curva = True
                self.t = 0.0

        if self.en_curva and self.curva_pts is not None:
            # Avanzar el parámetro t según la velocidad actual
            p0, p1, p2 = self.curva_pts
            dt = self.velocidad / ANCHO_PANTALLA
            self.t += dt
            if self.t > 1.0:
                # Al terminar la curva, reiniciar al inicio de la pista recta
                self.en_curva = False
                self.t = 0.0
                self.posicion = np.array([-40.0, p0[1]], dtype=float)
            else:
                # Actualizar posición usando la ecuación paramétrica de Bézier
                self.posicion = bezier(self.t, p0, p1, p2).astype(float)
        else:
            self.posicion[0] += self.velocidad
            # Reinicio al salir de pantalla
            if self.posicion[0] > ANCHO_PANTALLA + 40:
                self.posicion[0] = -40.0

#
    # Dibujar con matriz de rotación (etapa 2)
#
    def dibujar(self, pantalla, angulo=0):
        # Si el carro sigue una curva, calcular el ángulo a partir de la tangente de Bézier
        if self.en_curva and self.curva_pts is not None:
            p0, p1, p2 = self.curva_pts
            tangente = bezier_tangente(self.t, p0, p1, p2)
            angulo = math.degrees(math.atan2(tangente[1], tangente[0]))

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
