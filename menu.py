import sys
import os
import pygame
from audio import GestorAudio
from ventana import principal

ANCHO, ALTO = 800, 400
TAMANO_CELDA = 20


def cargar_imagen(ruta: str, ancho: int, alto: int):
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
    if os.path.exists(ruta_completa):
        try:
            imagen = pygame.image.load(ruta_completa)
            return pygame.transform.scale(imagen, (ancho, alto))
        except pygame.error:
            return None
    return None


class MenuPrincipal:
    def __init__(self, gestor_audio: GestorAudio | None = None):
        self.gestor_audio = gestor_audio or GestorAudio()
        self.opciones = [
            {"id": "nuevo", "texto": "Jugar"},
            {"id": "sonido", "texto": "Música: "},
            {"id": "salir", "texto": "Salir"},
        ]
        self.seleccion = 0
        self.fuente_titulo = None
        self.fuente_opcion = None
        self.fondo = None
        self.estado_sonido = True

    def _inicializar(self):
        if not pygame.get_init():
            pygame.init()
        self.fuente_titulo = pygame.font.SysFont("consolas", 36)
        self.fuente_opcion = pygame.font.SysFont("consolas", 24)
        self.fondo = cargar_imagen("assets/images/fondo.png", ANCHO, ALTO)
        # Estado inicial del sonido: si música está con volumen > 0
        try:
            self.estado_sonido = True
            pygame.mixer.music.set_volume(1.0)
        except Exception:
            self.estado_sonido = False

    def _dibujar(self, pantalla: pygame.Surface):
        if self.fondo:
            pantalla.blit(self.fondo, (0, 0))
        else:
            pantalla.fill((20, 20, 20))

        titulo = self.fuente_titulo.render("Serpiente", True, (255, 255, 255))
        pantalla.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 60))

        # Render opciones
        base_y = 140
        sep = 44
        for i, opt in enumerate(self.opciones):
            texto = opt["texto"]
            if opt["id"] == "sonido":
                texto += "ON" if self.estado_sonido else "OFF"
            color = (255, 255, 0) if i == self.seleccion else (220, 220, 220)
            surf = self.fuente_opcion.render(texto, True, color)
            x = (ANCHO - surf.get_width()) // 2
            y = base_y + i * sep
            pantalla.blit(surf, (x, y))

    def _toggle_sonido(self):
        self.estado_sonido = not self.estado_sonido
        if self.estado_sonido:
            # Reanudar música y poner volumen estándar
            self.gestor_audio.reanudar_musica()
            self.gestor_audio.set_volumen_musica(1.0)
            self.gestor_audio.set_volumen_efecto(1.0)
        else:
            # Pausar música y silenciar efectos
            self.gestor_audio.pausar_musica()
            self.gestor_audio.set_volumen_musica(0.0)
            self.gestor_audio.set_volumen_efecto(0.0)

    def mostrar(self) -> str:
        self._inicializar()
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Menú - Serpiente")
        # Establecer ícono de la ventana del menú
        try:
            ruta_icono = os.path.join(os.path.dirname(__file__), "assets", "images", "icono.png")
            if os.path.exists(ruta_icono):
                icono = pygame.image.load(ruta_icono)
                pygame.display.set_icon(icono)
            else:
                print(f"  ✗ No encontrado: assets/images/icono.png")
        except Exception as e:
            print(f"  ✗ Error estableciendo icono: {e}")
        reloj = pygame.time.Clock()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "salir"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "salir"
                    elif evento.key == pygame.K_UP:
                        self.seleccion = (self.seleccion - 1) % len(self.opciones)
                    elif evento.key == pygame.K_DOWN:
                        self.seleccion = (self.seleccion + 1) % len(self.opciones)
                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        opt_id = self.opciones[self.seleccion]["id"]
                        if opt_id == "nuevo":
                            return "nuevo"
                        elif opt_id == "sonido":
                            self._toggle_sonido()
                        elif opt_id == "salir":
                            return "salir"

            self._dibujar(pantalla)
            pygame.display.flip()
            reloj.tick(30)


def inicio_aplicacion():
    gestor_audio = GestorAudio()
    menu = MenuPrincipal(gestor_audio)
    while True:
        accion = menu.mostrar()
        if accion == "nuevo":
            resultado = principal()
            if resultado == "salir":
                break
            continue
        elif accion == "salir":
            break
