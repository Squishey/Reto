import pygame
import numpy as np
from config import (ANCHO_PANTALLA, ALTO_PANTALLA, FPS, BLANCO, GRIS, AZUL, ROJO)
from semaforo import Semaforo
from carro import Carro, bezier


# Clase Simulacion
class Simulacion:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Etapa 1 - Simulación de Tráfico")
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.reloj = pygame.time.Clock()

        self.semaforo = Semaforo([ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2])

        # La curva comienza justo donde está el semáforo
        semx = ANCHO_PANTALLA / 2
        semy = ALTO_PANTALLA / 2
        self.P0 = np.array([semx,                          semy])
        self.P1 = np.array([semx + (ANCHO_PANTALLA - semx) * 0.5, semy - 120])
        self.P2 = np.array([ANCHO_PANTALLA + 40.0,         semy - 150])

        self.carros = [
            Carro(0.0, ALTO_PANTALLA / 2, velocidad_inicial=0.0, velocidad_maxima=6.0),
            Carro(150.0, ALTO_PANTALLA / 2, velocidad_inicial=3.0, velocidad_maxima=7.0, color=ROJO),
        ]

        # Ambos carros tienen la curva configurada; se activa automáticamente al pasar el semáforo
        for carro in self.carros:
            carro.curva_pts = (self.P0, self.P1, self.P2)

    def ejecutar(self):
        running = True;
        while running:
            running = self._procesar_eventos()
            self._actualizar()
            self._dibujar()
            self.reloj.tick(FPS)
        pygame.quit()

    def _procesar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
        return True;

    def _actualizar(self):
        self.semaforo.actualizar()
        for carro in self.carros:
            carro.actualizar(self.semaforo, self.carros)

    def _dibujar(self):
        self.pantalla.fill(BLANCO)

        # Carretera recta hasta el semáforo
        semx = int(self.semaforo.posicion[0])
        y = ALTO_PANTALLA // 2
        pygame.draw.line(self.pantalla, GRIS, (0, y), (semx, y), 4)

        # Tramo curvo como continuación de la misma calle, después del semáforo
        puntos_curva = [bezier(i / 50, self.P0, self.P1, self.P2) for i in range(51)]
        pygame.draw.lines(self.pantalla, GRIS, False, puntos_curva, 4)

        # Semaforo
        self.semaforo.dibujar(self.pantalla)

        # Carros (el ángulo lo calcula cada carro internamente si sigue una curva)
        for carro in self.carros:
            carro.dibujar(self.pantalla)

        pygame.display.flip()


# entrypoint
if __name__ == "__main__":
    Simulacion().ejecutar();