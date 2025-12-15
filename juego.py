from serpiente import Serpiente, ARRIBA, ABAJO, IZQUIERDA, DERECHA
from comida import generar_manzana
class Juego:
    def __init__(self, columnas: int, filas: int):
        self.columnas = columnas
        self.filas = filas
        self.puntaje = 0
        self.reiniciar()

    def reiniciar(self):
        self.serpiente = Serpiente((self.columnas // 2, self.filas // 2))
        self.manzana = generar_manzana(self.columnas, self.filas, self.serpiente.ocupa())
        self.puntaje = 0

    def establecer_direccion(self, direccion):
        self.serpiente.establecer_direccion(direccion)

    def fuera_de_limites(self, pos):
        x, y = pos
        return x < 0 or x >= self.columnas or y < 0 or y >= self.filas

    def paso(self):
        dx, dy = self.serpiente.direccion
        cx, cy = self.serpiente.cabeza()
        siguiente = (cx + dx, cy + dy)

        if self.fuera_de_limites(siguiente):
            self.reiniciar()
            return {"reinicio": True, "crecio": False, "puntaje": self.puntaje}

        crece = siguiente == self.manzana
        cuerpo = self.serpiente.ocupa()
        
        if siguiente in (cuerpo if crece else cuerpo[:-1]):
            self.reiniciar()
            return {"reinicio": True, "crecio": False, "puntaje": self.puntaje}

        self.serpiente.mover(crecer=crece)
        
        if crece:
            self.puntaje += 1
            self.manzana = generar_manzana(self.columnas, self.filas, self.serpiente.ocupa())

        return {"reinicio": False, "crecio": crece, "puntaje": self.puntaje}
