import os
import pygame


class GestorCursores:

    CURSORES_DISPONIBLES = {
        "normal": "tile_0000.png",   # Flecha normal
        "menu": "tile_0001.png",     # Botón/interacción
        "juego": "tile_0085.png",    # Dirección
        "comer": "tile_0090.png",    # Especial (estrella)
        "perdio": "tile_0039.png",   # Error (X)
    }

    def __init__(self):
        self.ruta_base = os.path.join(os.path.dirname(__file__), "assets", "cursores_juego", "cursores")
        self.cursores = {}
        self._cargar_cursores()

    def _cargar_cursores(self):
        """Carga todos los cursores."""
        for nombre, archivo in self.CURSORES_DISPONIBLES.items():
            ruta = os.path.join(self.ruta_base, archivo)
            if not os.path.exists(ruta):
                continue
            try:
                img = pygame.image.load(ruta)
                # Escalar si es necesario (max 32x32)
                if img.get_width() > 32 or img.get_height() > 32:
                    img = pygame.transform.scale(img, (32, 32))
                self.cursores[nombre] = pygame.cursors.Cursor((0, 0), img)
            except Exception:
                pass

    def establecer_cursor(self, nombre: str = "normal"):
        if nombre not in self.cursores:
            nombre = "normal"  
        
        try:
            pygame.mouse.set_cursor(self.cursores[nombre])
        except Exception:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def establecer_cursor_normal(self):
        self.establecer_cursor("normal")

    def establecer_cursor_menu(self):
        self.establecer_cursor("menu")

    def establecer_cursor_juego(self):
        self.establecer_cursor("juego")

    def establecer_cursor_comer(self):
        self.establecer_cursor("comer")

    def establecer_cursor_perdio(self):
        self.establecer_cursor("perdio")

    def resetear_cursor(self):
        """Resetea al cursor del sistema."""
        try:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
