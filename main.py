import pygame
from config import (ANCHO_PANTALLA, ALTO_PANTALLA, FPS, BLANCO, GRIS, AZUL, ROJO)
from semaforo import Semaforo
from carro import Carro


# Clase Simulacion
class Simulacion:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Etapa 1 - Simulación de Tráfico")
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.reloj = pygame.time.Clock()

        self.semaforo = Semaforo([ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2])

        self.carros = [
            Carro(0.0, ALTO_PANTALLA / 2, velocidad_inicial=0.0, velocidad_maxima=6.0),
            Carro(150.0, ALTO_PANTALLA / 2,velocidad_inicial=3.0, velocidad_maxima=7.0, color=ROJO),
        ]

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

        # Carretera
        y = ALTO_PANTALLA // 2;
        pygame.draw.line(self.pantalla, GRIS, (0, y), (ANCHO_PANTALLA, y), 4)

        # Semaforo
        self.semaforo.dibujar(self.pantalla)

        # Carros
        for carro in self.carros:
            carro.dibujar(self.pantalla);

        pygame.display.flip()


# entrypoint
if __name__ == "__main__":
    Simulacion().ejecutar();