from typing import List, Tuple

# Direcciones
ARRIBA: Tuple[int, int] = (0, -1)
ABAJO: Tuple[int, int] = (0, 1)
IZQUIERDA: Tuple[int, int] = (-1, 0)
DERECHA: Tuple[int, int] = (1, 0)


class Serpiente:
	def __init__(self, inicio: Tuple[int, int]) -> None:
		self.cuerpo: List[Tuple[int, int]] = [inicio]
		self.direccion: Tuple[int, int] = DERECHA

	def cabeza(self) -> Tuple[int, int]:
		return self.cuerpo[0]

	def establecer_direccion(self, nueva: Tuple[int, int]) -> None:
		# Evita girar 180° inmediatamente
		opuesta = (-self.direccion[0], -self.direccion[1])
		if nueva != opuesta:
			self.direccion = nueva

	def mover(self, crecer: bool = False) -> None:
		dx, dy = self.direccion
		x, y = self.cabeza()
		nueva_cabeza = (x + dx, y + dy)
		self.cuerpo.insert(0, nueva_cabeza)
		if not crecer:
			self.cuerpo.pop()

	def se_colisiona_con_su_cuerpo(self) -> bool:
		return self.cabeza() in self.cuerpo[1:]

	def ocupa(self) -> List[Tuple[int, int]]:
		return list(self.cuerpo)

