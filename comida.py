import random
from typing import List, Tuple


def generar_manzana(columnas: int, filas: int, ocupadas: List[Tuple[int, int]]) -> Tuple[int, int]:
    todas = {(x, y) for x in range(columnas) for y in range(filas)}
    libres = list(todas - set(ocupadas))
    if not libres:
        return 0, 0
    return random.choice(libres)
