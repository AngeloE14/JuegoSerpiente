from typing import Tuple

from serpiente import Serpiente, ARRIBA, ABAJO, IZQUIERDA, DERECHA
from comida import generar_manzana


class Juego:
    def __init__(self, columnas: int, filas: int) -> None:
        self.columnas = columnas
        self.filas = filas
        self.puntaje = 0
        self.reiniciar()

    def reiniciar(self) -> None:
        inicio = (self.columnas // 2, self.filas // 2)
        self.serpiente = Serpiente(inicio)
        self.manzana = generar_manzana(self.columnas, self.filas, self.serpiente.ocupa())
        self.puntaje = 0

    def establecer_direccion(self, direccion: Tuple[int, int]) -> None:
        self.serpiente.establecer_direccion(direccion)

    def fuera_de_limites(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        return x < 0 or x >= self.columnas or y < 0 or y >= self.filas

    def paso(self) -> dict:
        """Avanza un tick de juego.
        Retorna un dict con claves:
          - 'reinicio': bool, si se reinició por colisión
          - 'crecio': bool, si la serpiente comió y creció
          - 'puntaje': int, puntaje actual
        """
        dx, dy = self.serpiente.direccion
        cx, cy = self.serpiente.cabeza()
        siguiente = (cx + dx, cy + dy)

        # Colisión con pared -> reiniciar
        if self.fuera_de_limites(siguiente):
            self.reiniciar()
            return {"reinicio": True, "crecio": False, "puntaje": self.puntaje}

        # Comer manzana
        crece = siguiente == self.manzana

        # Colisión con el cuerpo: considerar si crece o no
        cuerpo = self.serpiente.ocupa()
        if crece:
            objetivo_ocupado = siguiente in cuerpo
        else:
            objetivo_ocupado = siguiente in cuerpo[:-1]
        if objetivo_ocupado:
            self.reiniciar()
            return {"reinicio": True, "crecio": False, "puntaje": self.puntaje}

        # Movimiento válido
        self.serpiente.mover(crecer=crece)
        if crece:
            self.puntaje += 1
            self.manzana = generar_manzana(self.columnas, self.filas, self.serpiente.ocupa())

        return {"reinicio": False, "crecio": crece, "puntaje": self.puntaje}
