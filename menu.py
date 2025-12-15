import os
import pygame
from audio import GestorAudio
from ventana import principal
from cursores import GestorCursores

ANCHO, ALTO = 800, 400


def cargar_imagen(ruta: str, ancho: int, alto: int):
    """Carga y escala una imagen ya con convert/convert_alpha para blits rápidos."""
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
    if not os.path.exists(ruta_completa):
        return None
    try:
        img = pygame.image.load(ruta_completa)
        if img.get_alpha() is not None:
            img = img.convert_alpha()
        else:
            img = img.convert()
        return pygame.transform.scale(img, (ancho, alto))
    except pygame.error:
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
        self.assets = None
        self.gestor_cursores = None

    def _inicializar(self, pantalla: pygame.Surface):
        if not pygame.get_init():
            pygame.init()
        self.fuente_titulo = self.fuente_titulo or pygame.font.SysFont("consolas", 36)
        self.fuente_opcion = self.fuente_opcion or pygame.font.SysFont("consolas", 24)
        # Carga única de assets convertidos para reuso en el juego
        if self.assets is None:
            fondo = cargar_imagen("assets/images/fondo.png", ANCHO, ALTO)
            manzana = cargar_imagen("assets/images/manzana.png", 20, 20)
            notificacion = None
            icono = None
            ruta_notif = os.path.join(os.path.dirname(__file__), "assets", "images", "notificacion.png")
            ruta_icono = os.path.join(os.path.dirname(__file__), "assets", "images", "iconito.png")
            if os.path.exists(ruta_notif):
                try:
                    tmp = pygame.image.load(ruta_notif)
                    notificacion = tmp.convert_alpha() if tmp.get_alpha() else tmp.convert()
                except Exception:
                    notificacion = None
            if os.path.exists(ruta_icono):
                try:
                    tmp = pygame.image.load(ruta_icono)
                    icono = tmp.convert_alpha() if tmp.get_alpha() else tmp.convert()
                except Exception:
                    icono = None
            self.assets = {
                "fondo": fondo,
                "manzana": manzana,
                "manzana_base": manzana.copy() if manzana else None,
                "notificacion": notificacion,
                "icono": icono,
            }
        self.fondo = self.assets.get("fondo") if self.assets else None
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
            
            self.gestor_audio.reanudar_musica()
            self.gestor_audio.set_volumen_musica(1.0)
            self.gestor_audio.set_volumen_efecto(1.0)
        else:
            
            self.gestor_audio.pausar_musica()
            self.gestor_audio.set_volumen_musica(0.0)
            self.gestor_audio.set_volumen_efecto(0.0)

    def mostrar(self) -> str:
        if not pygame.get_init():
            pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Menú - Serpiente")
        self._inicializar(pantalla)

        if self.gestor_cursores is None:
            self.gestor_cursores = GestorCursores()
        self.gestor_cursores.establecer_cursor_menu()
        try:
            if self.assets and self.assets.get("icono"):
                pygame.display.set_icon(self.assets["icono"])
            else:
                ruta_icono = os.path.join(os.path.dirname(__file__), "assets", "images", "iconito.png")
                if os.path.exists(ruta_icono):
                    icono = pygame.image.load(ruta_icono)
                    pygame.display.set_icon(icono)
        except Exception:
            pass
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
            resultado = principal(
                gestor_audio=menu.gestor_audio,
                gestor_cursores=menu.gestor_cursores,
                assets=menu.assets,
            )
            if resultado == "salir":
                break
            continue
        elif accion == "salir":
            break
