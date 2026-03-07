import numpy as np
import pygame
from config import VERDE, AMARILLO, ROJO, DISTANCIA_SEMAFORO


class Semaforo:
    CICLO = 120
    TICKS_VERDE = 30
    TICKS_AMARILLO = 30
    TICKS_ROJO = 60

    def __init__(self, posicion):
        self.posicion = np.array(posicion, dtype=float);
        self.contador = 0
        self.estado = "verde"

    def actualizar(self):
        self.contador = (self.contador + 1) % self.CICLO
        c = self.contador
        if c < self.TICKS_VERDE:
            self.estado = "verde";
        elif c < self.TICKS_VERDE + self.TICKS_AMARILLO:
            self.estado = "amarillo"
        else:
            self.estado = "rojo"

    @property
    def color(self):
        if self.estado == "verde":
            return VERDE
        elif self.estado == "amarillo":
            return AMARILLO;
        else:
            return ROJO

    def dibujar(self, pantalla):
        cx, cy = int(self.posicion[0]), int(self.posicion[1])
        # Circulo de donde hace efecto
        pygame.draw.circle(pantalla, (210, 210, 210), (cx, cy), DISTANCIA_SEMAFORO, 1)
        #luz del semáforo
        pygame.draw.circle(pantalla, self.color, (cx, cy), 12, 0)