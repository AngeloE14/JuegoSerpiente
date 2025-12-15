import sys
import os
import pygame
import math
from serpiente import ARRIBA, ABAJO, IZQUIERDA, DERECHA
from juego import Juego
from audio import GestorAudio

ANCHO, ALTO = 800, 400
TAMANO_CELDA = 20
COLUMNAS = ANCHO // TAMANO_CELDA
FILAS = ALTO // TAMANO_CELDA
FONDO = (20, 20, 20)
COLOR_SERPIENTE = (92, 62, 59)
COLOR_MANZANA = (231, 76, 60)


def cargar_imagen(ruta: str, ancho: int, alto: int):
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
    if os.path.exists(ruta_completa):
        try:
            imagen = pygame.image.load(ruta_completa)
            return pygame.transform.scale(imagen, (ancho, alto))
        except pygame.error as e:
            print(f"  ✗ Error cargando {ruta}: {e}")
            return None
    else:
        print(f"  ✗ No encontrado: {ruta}")
        return None


def principal():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Serpiente en Python")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 18)
    juego = Juego(COLUMNAS, FILAS)
    
    # Cargar imágenes desde assets/images/
    imagen_manzana = cargar_imagen("assets/images/manzana.png", TAMANO_CELDA, TAMANO_CELDA)
    imagen_serpiente = cargar_imagen("assets/images/serpiente.png", TAMANO_CELDA, TAMANO_CELDA)
    imagen_fondo = cargar_imagen("assets/images/fondo.png", ANCHO, ALTO)
    imagen_manzana_base = imagen_manzana.copy() if imagen_manzana else None
    
    # Inicializar gestor de audio (carga automáticamente todos los audios)
    gestor_audio = GestorAudio()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
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
        # Reproducir sonido de comer
        if estado.get('crecio'):
            gestor_audio.reproducir_efecto('comer')
        
        # === FASE 1: Dibujar fondo ===
        if imagen_fondo:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill(FONDO)
        
        # === FASE 2: Dibujar manzana (animada) ===
        mx, my = juego.manzana
        if imagen_manzana_base:
            # pulso usando seno: 1.0 +/- 0.15 (15%) con periodo 1s
            t = pygame.time.get_ticks() / 1000.0
            periodo = 1.0
            escala = 1.0 + 0.15 * math.sin(2 * math.pi * t / periodo)
            frame = pygame.transform.rotozoom(imagen_manzana_base, 0, escala)
            w, h = frame.get_size()
            px = int(mx * TAMANO_CELDA + (TAMANO_CELDA - w) / 2)
            py = int(my * TAMANO_CELDA + (TAMANO_CELDA - h) / 2)
            pantalla.blit(frame, (px, py))
        else:
            rect_manzana = pygame.Rect(mx * TAMANO_CELDA, my * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, COLOR_MANZANA, rect_manzana)
        
        # === FASE 3: Dibujar serpiente (cada segmento) ===
        for (cx, cy) in juego.serpiente.ocupa():
            if imagen_serpiente:
                pantalla.blit(imagen_serpiente, (cx * TAMANO_CELDA, cy * TAMANO_CELDA))
            else:
                rect = pygame.Rect(cx * TAMANO_CELDA, cy * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
                pygame.draw.rect(pantalla, COLOR_SERPIENTE, rect)
        
        # === FASE 4: Indicador de manzanas comidas ===
        # Mostrar un icono de manzana y el número total al lado
        x_icon = 10
        y_icon = 10
        if imagen_manzana:
            pantalla.blit(imagen_manzana, (x_icon, y_icon))
        else:
            rect_icon = pygame.Rect(x_icon, y_icon, TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, COLOR_MANZANA, rect_icon)

        # Número al lado del icono
        conteo = estado.get('puntaje', 0)
        texto = fuente.render(f"x {conteo}", True, (255, 255, 255))
        pantalla.blit(texto, (x_icon + TAMANO_CELDA + 6, y_icon + (TAMANO_CELDA - texto.get_height()) // 2))
        pygame.display.flip()
        reloj.tick(10)
