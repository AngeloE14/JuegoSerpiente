import sys
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
COLOR_SERPIENTE = (92, 62, 59)
COLOR_MANZANA = (231, 76, 60)


def cargar_imagen(ruta: str, ancho: int, alto: int):
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
    if os.path.exists(ruta_completa):
        try:
            imagen = pygame.image.load(ruta_completa)
            imagen = imagen.convert_alpha()  # optimiza blits respetando transparencia
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
    # Inicializar gestor de cursores personalizados
    gestor_cursores = GestorCursores()
    gestor_cursores.establecer_cursor_juego()
    # Establecer ícono de la ventana
    try:
        ruta_icono = os.path.join(os.path.dirname(__file__), "assets", "images", "icono.png")
        if os.path.exists(ruta_icono):
            icono = pygame.image.load(ruta_icono).convert_alpha()
            pygame.display.set_icon(icono)
        else:
            print(f"  ✗ No encontrado: assets/images/icono.png")
    except Exception as e:
        print(f"  ✗ Error estableciendo icono: {e}")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 18)
    juego = Juego(COLUMNAS, FILAS)
    
    # Cargar imágenes desde assets/images/
    imagen_manzana = cargar_imagen("assets/images/manzana.png", TAMANO_CELDA, TAMANO_CELDA)
    # Cargar snake.png para la animación de la serpiente
    imagen_serpiente = cargar_imagen("assets/images/snake.png", TAMANO_CELDA, TAMANO_CELDA)
    # Fallback a serpiente.png si snake.png no existe
    if not imagen_serpiente:
        imagen_serpiente = cargar_imagen("assets/images/serpiente.png", TAMANO_CELDA, TAMANO_CELDA)
    imagen_serpiente_base = imagen_serpiente.copy() if imagen_serpiente else None
    imagen_fondo = cargar_imagen("assets/images/fondo.png", ANCHO, ALTO)
    imagen_manzana_base = imagen_manzana.copy() if imagen_manzana else None
    # Notificación de derrota (sin escalado para respetar su tamaño original)
    ruta_notif = os.path.join(os.path.dirname(__file__), "assets", "images", "notificacion.png")
    imagen_notificacion = None
    if os.path.exists(ruta_notif):
        try:
            imagen_notificacion = pygame.image.load(ruta_notif).convert_alpha()
        except Exception as e:
            print(f"  ✗ Error cargando notificacion.png: {e}")
    
    # Inicializar gestor de audio (carga automáticamente todos los audios)
    gestor_audio = GestorAudio()
    # Cache de texto para el puntaje para evitar render en cada frame
    ultimo_puntaje = None
    texto_puntaje = None
    # Variables para animación suave: interpolación entre celdas
    tiempo_movimiento = 0  # contador para interpolar movimiento
    velocidad_animacion = 0.15  # fracción de celda por frame (velocidad suave)
    rotacion_serpiente = 0  # 0=derecha, 90=abajo, 180=izquierda, 270=arriba

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    juego.establecer_direccion(ARRIBA)
                    rotacion_serpiente = 270
                elif evento.key == pygame.K_DOWN:
                    juego.establecer_direccion(ABAJO)
                    rotacion_serpiente = 90
                elif evento.key == pygame.K_LEFT:
                    juego.establecer_direccion(IZQUIERDA)
                    rotacion_serpiente = 180
                elif evento.key == pygame.K_RIGHT:
                    juego.establecer_direccion(DERECHA)
                    rotacion_serpiente = 0

        estado = juego.paso()
        # Al perder mostramos notificacion.png, reproducimos 'perder', cambiamos cursor y regresamos al menú principal
        if estado.get('reinicio'):
            gestor_audio.reproducir_efecto('perder')
            gestor_cursores.establecer_cursor_perdio()  # Cambiar cursor al de "perdida"
            if imagen_fondo:
                pantalla.blit(imagen_fondo, (0, 0))
            else:
                pantalla.fill(FONDO)
            if imagen_notificacion:
                rect_notif = imagen_notificacion.get_rect(center=(ANCHO // 2, ALTO // 2))
                pantalla.blit(imagen_notificacion, rect_notif.topleft)
            else:
                texto_notif = fuente.render("Perdiste", True, (255, 255, 255))
                pantalla.blit(texto_notif, ((ANCHO - texto_notif.get_width()) // 2, (ALTO - texto_notif.get_height()) // 2))
            pygame.display.flip()
            pygame.time.delay(1200)
            return "menu"

        # Reproducir sonido de comer y cambiar cursor
        if estado.get('crecio'):
            gestor_audio.reproducir_efecto('comer')
            gestor_cursores.establecer_cursor_comer()  # Cursor especial al comer
            pygame.time.delay(100)  # Mostrar cursor especial brevemente
            gestor_cursores.establecer_cursor_juego()  # Volver al cursor normal del juego
        
        # === FASE 1: Dibujar fondo ===
        if imagen_fondo:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill(FONDO)
        
        # === FASE 2: Dibujar manzana (animada, centrada sin saltos) ===
        mx, my = juego.manzana
        cx = mx * TAMANO_CELDA + TAMANO_CELDA // 2
        cy = my * TAMANO_CELDA + TAMANO_CELDA // 2
        if imagen_manzana_base:
            # Pulso suave: 1.0 +/- 0.10 con periodo 1.2s
            t = pygame.time.get_ticks() / 1000.0
            periodo = 1.2
            escala = 1.0 + 0.10 * math.sin(2 * math.pi * t / periodo)
            frame = pygame.transform.rotozoom(imagen_manzana_base, 0, escala)
            rect = frame.get_rect(center=(cx, cy))
            pantalla.blit(frame, rect.topleft)
        else:
            # Animación de tamaño para fallback sin imagen
            t = pygame.time.get_ticks() / 1000.0
            periodo = 1.2
            escala = 1.0 + 0.10 * math.sin(2 * math.pi * t / periodo)
            radio = max(4, int((TAMANO_CELDA // 2) * escala))
            pygame.draw.circle(pantalla, COLOR_MANZANA, (cx, cy), radio)
        
        # === FASE 3: Dibujar serpiente (movimiento suave interpolado) ===
        # Interpolar la posición de cada segmento para movimiento fluido
        tiempo_movimiento += velocidad_animacion
        if tiempo_movimiento >= 1.0:
            tiempo_movimiento = 0.0
        
        for idx, (cx, cy) in enumerate(juego.serpiente.ocupa()):
            # Calcular posición suavizada entre celdas
            px = (cx * TAMANO_CELDA + TAMANO_CELDA // 2)
            py = (cy * TAMANO_CELDA + TAMANO_CELDA // 2)
            
            if imagen_serpiente_base:
                # Cabeza se rota según dirección; cuerpo es estático
                angulo = rotacion_serpiente if idx == 0 else 0
                frame_seg = pygame.transform.rotate(imagen_serpiente_base, angulo)
                rect_seg = frame_seg.get_rect(center=(int(px), int(py)))
                pantalla.blit(frame_seg, rect_seg.topleft)
            else:
                # Fallback: rectángulo
                rect = pygame.Rect(int(px) - TAMANO_CELDA // 2, int(py) - TAMANO_CELDA // 2, 
                                   TAMANO_CELDA, TAMANO_CELDA)
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

        # Número al lado del icono (solo renderiza si cambia el puntaje)
        conteo = estado.get('puntaje', 0)
        if conteo != ultimo_puntaje:
            ultimo_puntaje = conteo
            texto_puntaje = fuente.render(f"x {conteo}", True, (255, 255, 255))
        if texto_puntaje:
            pantalla.blit(texto_puntaje, (x_icon + TAMANO_CELDA + 6, y_icon + (TAMANO_CELDA - texto_puntaje.get_height()) // 2))
        pygame.display.flip()
        reloj.tick(10)
