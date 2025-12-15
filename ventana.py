import os
import pygame
import math
from serpiente import ARRIBA, ABAJO, IZQUIERDA, DERECHA
from juego import Juego
from audio import GestorAudio
from cursores import GestorCursores

ANCHO, ALTO = 800, 400
TAMANO_CELDA = 20
COLUMNAS = ANCHO // TAMANO_CELDA
FILAS = ALTO // TAMANO_CELDA
FONDO = (20, 20, 20)
COLOR_SERPIENTE = (0, 51, 102)
COLOR_MANZANA = (231, 76, 60)


def cargar_imagen(ruta: str, ancho: int, alto: int):
    """Carga una imagen (si existe) y la escala; None si falla."""
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
    except Exception:
        return None


def principal(gestor_audio: GestorAudio | None = None, gestor_cursores: GestorCursores | None = None, assets: dict | None = None):
    pygame.init()
    pantalla = pygame.display.get_surface() or pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Serpiente en Python")

    gestor_cursores = gestor_cursores or GestorCursores()
    gestor_cursores.establecer_cursor_juego()

    # Ícono (silencioso si no existe)
    icono = assets.get("icono") if assets else None
    if icono is None:
        icono = cargar_imagen("assets/images/iconito.png", 32, 32)
    if icono:
        try:
            pygame.display.set_icon(icono)
        except Exception:
            pass

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 18)
    juego = Juego(COLUMNAS, FILAS)
    gestor_audio = gestor_audio or GestorAudio()
    ultimo_puntaje = None
    texto_puntaje = None

    # Assets (reuse cache if provided)
    imagen_manzana = None
    imagen_fondo = None
    imagen_manzana_base = None
    imagen_notificacion = None
    if assets:
        imagen_manzana = assets.get("manzana")
        imagen_manzana_base = assets.get("manzana_base") or (imagen_manzana.copy() if imagen_manzana else None)
        imagen_fondo = assets.get("fondo")
        imagen_notificacion = assets.get("notificacion")
    if imagen_manzana is None:
        imagen_manzana = cargar_imagen("assets/images/manzana.png", TAMANO_CELDA, TAMANO_CELDA)
        imagen_manzana_base = imagen_manzana.copy() if imagen_manzana else None
    if imagen_fondo is None:
        imagen_fondo = cargar_imagen("assets/images/fondo.png", ANCHO, ALTO)
    if imagen_notificacion is None:
        ruta_notif = os.path.join(os.path.dirname(__file__), "assets", "images", "notificacion.png")
        if os.path.exists(ruta_notif):
            try:
                tmp = pygame.image.load(ruta_notif)
                imagen_notificacion = tmp.convert_alpha() if tmp.get_alpha() else tmp.convert()
            except Exception:
                imagen_notificacion = None

    radio_segmento = TAMANO_CELDA // 2 - 2

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    juego.establecer_direccion(ARRIBA)
                elif evento.key == pygame.K_DOWN:
                    juego.establecer_direccion(ABAJO)
                elif evento.key == pygame.K_LEFT:
                    juego.establecer_direccion(IZQUIERDA)
                elif evento.key == pygame.K_RIGHT:
                    juego.establecer_direccion(DERECHA)

        estado = juego.paso()
        if estado.get('reinicio'):
            gestor_audio.reproducir_sonido('perder')
            gestor_cursores.establecer_cursor_perdio()
            if imagen_fondo:
                pantalla.blit(imagen_fondo, (0, 0))
            else:
                pantalla.fill(FONDO)
            if imagen_notificacion:
                rect_notif = imagen_notificacion.get_rect(center=(ANCHO // 2, ALTO // 2))
                pantalla.blit(imagen_notificacion, rect_notif.topleft)
            pygame.display.flip()
            pygame.time.delay(1200)
            return "menu"

        
        if estado.get('crecio'):
            gestor_audio.reproducir_sonido('comer')
            gestor_cursores.establecer_cursor_comer()  # Cursor especial al comer
            
        if imagen_fondo:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill(FONDO)
        
        mx, my = juego.manzana
        cx = mx * TAMANO_CELDA + TAMANO_CELDA // 2
        cy = my * TAMANO_CELDA + TAMANO_CELDA // 2
        if imagen_manzana_base:
            t = pygame.time.get_ticks() / 1000.0
            periodo = 1.2
            escala = 1.5 + 0.15 * math.sin(2 * math.pi * t / periodo)
            frame = pygame.transform.rotozoom(imagen_manzana_base, 0, escala)
            rect = frame.get_rect(center=(cx, cy))
            pantalla.blit(frame, rect.topleft)
        else:
            t = pygame.time.get_ticks() / 1000.0
            periodo = 1.2
            escala = 1.0 + 0.10 * math.sin(2 * math.pi * t / periodo)
            radio = max(4, int((TAMANO_CELDA // 2) * escala))
            pygame.draw.circle(pantalla, COLOR_MANZANA, (cx, cy), radio)
        
        segmentos = list(juego.serpiente.ocupa())

        cuerpo_color = COLOR_SERPIENTE

        for idx, (sx, sy) in enumerate(segmentos):
            px = (sx * TAMANO_CELDA + TAMANO_CELDA // 2)
            py = (sy * TAMANO_CELDA + TAMANO_CELDA // 2)

            pygame.draw.circle(pantalla, cuerpo_color, (int(px), int(py)), radio_segmento)

            # Añadir ojos a la cabeza 
            if idx == 0 and len(segmentos) > 1:
                siguiente = segmentos[1]
                dir_x = siguiente[0] - sx
                dir_y = siguiente[1] - sy
                
                ojo_radio = max(2, TAMANO_CELDA // 10)
                offset = TAMANO_CELDA // 4
                
                if dir_x > 0:  # DERECHA
                    ox1, oy1 = px - offset, py - offset
                    ox2, oy2 = px - offset, py + offset
                elif dir_x < 0:  # IZQUIERDA
                    ox1, oy1 = px + offset, py - offset
                    ox2, oy2 = px + offset, py + offset
                elif dir_y > 0:  # ABAJO
                    ox1, oy1 = px - offset, py - offset
                    ox2, oy2 = px + offset, py - offset
                else:  # ARRIBA
                    ox1, oy1 = px - offset, py + offset
                    ox2, oy2 = px + offset, py + offset
                
                pygame.draw.circle(pantalla, (255, 255, 255), (int(ox1), int(oy1)), ojo_radio)
                pygame.draw.circle(pantalla, (255, 255, 255), (int(ox2), int(oy2)), ojo_radio)
                pup_radio = max(1, ojo_radio // 2)
                pygame.draw.circle(pantalla, (30, 30, 30), (int(ox1), int(oy1)), pup_radio)
                pygame.draw.circle(pantalla, (30, 30, 30), (int(ox2), int(oy2)), pup_radio)
        
        x_icon = 10
        y_icon = 10
        if imagen_manzana:
            pantalla.blit(imagen_manzana, (x_icon, y_icon))
        else:
            rect_icon = pygame.Rect(x_icon, y_icon, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, COLOR_MANZANA, rect_icon)

        conteo = estado.get('puntaje', 0)
        if conteo != ultimo_puntaje:
            ultimo_puntaje = conteo
            texto_puntaje = fuente.render(f"x {conteo}", True, (255, 255, 255))
        if texto_puntaje:
            pantalla.blit(texto_puntaje, (x_icon + TAMANO_CELDA + 6, y_icon + (TAMANO_CELDA - texto_puntaje.get_height()) // 2))
        pygame.display.flip()
        reloj.tick(10)
