import pygame
import numpy as np
from config import (ANCHO_PANTALLA, ALTO_PANTALLA, FPS, BLANCO, GRIS, AZUL, ROJO, VERDE, AMARILLO)
from semaforo import Semaforo
from carro import Carro, bezier


# Clase Simulacion
class Simulacion:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Simulacion de trafico")
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.reloj = pygame.time.Clock()

        semx = ANCHO_PANTALLA / 2
        # 2 semaforos con desfase para que alternen. Semforo 2 mas cerca del cruce 
        self.semaforo_1 = Semaforo([semx, ALTO_PANTALLA / 2 + 50])
        self.semaforo_2 = Semaforo([semx + 120, ALTO_PANTALLA / 2 - 100], offset=60)

        #curva 1: de abajo hacia arriba (cruzaa  la otra)
        self.P0_1 = np.array([semx, ALTO_PANTALLA / 2 + 50])
        self.P1_1 = np.array([semx + 150, ALTO_PANTALLA / 2 + 50])
        self.P2_1 = np.array([ANCHO_PANTALLA + 40.0, ALTO_PANTALLA / 2 - 150])

        # crva 2: de arriba hacia abajo (cruza la otra). Empieza despues
        self.P0_2 = np.array([semx + 120, ALTO_PANTALLA / 2 - 100])
        self.P1_2 = np.array([semx + 120 + 150, ALTO_PANTALLA / 2 - 100])
        self.P2_2 = np.array([ANCHO_PANTALLA + 40.0, ALTO_PANTALLA / 2 + 100])

        self.carros = [
            Carro(0.0, self.P0_1[1], velocidad_inicial=0.0, velocidad_maxima=6.0),
            Carro(150.0, self.P0_1[1], velocidad_inicial=3.0, velocidad_maxima=7.0, color=ROJO),
            Carro(50.0, self.P0_2[1], velocidad_inicial=2.0, velocidad_maxima=5.0, color=VERDE),
            Carro(200.0, self.P0_2[1], velocidad_inicial=4.0, velocidad_maxima=6.0, color=AMARILLO),
        ]

        # asignar curvas y semaforos correspondientes!
        for idx, carro in enumerate(self.carros):
            if idx < 2:
                carro.curva_pts = (self.P0_1, self.P1_1, self.P2_1)
                carro.mi_semaforo = self.semaforo_1
            else:
                carro.curva_pts = (self.P0_2, self.P1_2, self.P2_2)
                carro.mi_semaforo = self.semaforo_2

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
        self.semaforo_1.actualizar()
        self.semaforo_2.actualizar()
        for carro in self.carros:
            carro.actualizar(carro.mi_semaforo, self.carros)

    def _dibujar(self):
        # Fondo verde para simular tipo cesped o algo asi jajaj
        self.pantalla.fill((200, 230, 200))

        # Decoración simple: Árboles
        for arbol_x, arbol_y in [(100, 100), (300, 80), (700, 400), (600, 80), (200, 400), (450, 400), (750, 200)]:
            pygame.draw.circle(self.pantalla, (139, 69, 19), (arbol_x, arbol_y), 5) # Tronco
            pygame.draw.circle(self.pantalla, (34, 139, 34), (arbol_x, arbol_y - 12), 20) # Hojas

        #semaforo 1
        semx1 = int(self.semaforo_1.posicion[0])
        y1 = int(self.semaforo_1.posicion[1])
        pygame.draw.line(self.pantalla, GRIS, (0, y1), (semx1, y1), 40) # Calle más gruesa
        pygame.draw.line(self.pantalla, BLANCO, (0, y1), (semx1, y1), 2) # Línea divisoria

        puntos_curva_1 = [bezier(i / 100, self.P0_1, self.P1_1, self.P2_1) for i in range(101)]
        pygame.draw.lines(self.pantalla, GRIS, False, puntos_curva_1, 40)
        pygame.draw.lines(self.pantalla, BLANCO, False, puntos_curva_1, 2)
        self.semaforo_1.dibujar(self.pantalla)

        # Semaforo 2
        semx2 = int(self.semaforo_2.posicion[0])
        y2 = int(self.semaforo_2.posicion[1])
        pygame.draw.line(self.pantalla, GRIS, (0, y2), (semx2, y2), 40) # Calle gruesa
        pygame.draw.line(self.pantalla, BLANCO, (0, y2), (semx2, y2), 2) # Línea divisoria

        puntos_curva_2 = [bezier(i / 100, self.P0_2, self.P1_2, self.P2_2) for i in range(101)]
        pygame.draw.lines(self.pantalla, GRIS, False, puntos_curva_2, 40)
        pygame.draw.lines(self.pantalla, BLANCO, False, puntos_curva_2, 2)
        self.semaforo_2.dibujar(self.pantalla)

        #semaforos por encima de las calles
        self.semaforo_1.dibujar(self.pantalla)
        self.semaforo_2.dibujar(self.pantalla)

        # Carros (el angulo lo calcula cada carro internamente si sigue una curva)
        for carro in self.carros:
            carro.dibujar(self.pantalla)

        pygame.display.flip()


# entrypoint
if __name__ == "__main__":
    Simulacion().ejecutar();
