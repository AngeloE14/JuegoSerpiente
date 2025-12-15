"""Módulo de audio - Manejo centralizado de sonidos y música."""

import os
import pygame


class GestorAudio:
    """Gestiona la carga y reproducción de sonidos y música."""

    def __init__(self):
        self.sonido_comer = None
        self.inicializado = False
        self._inicializar()
        self._cargar_audios()

    def _inicializar(self):
        """Inicializa el mezclador de pygame."""
        try:
            pygame.mixer.init()
            self.inicializado = True
            print("  ✓ Mezclador de audio inicializado")
        except Exception as e:
            print(f"  ✗ Error inicializando audio: {e}")
            self.inicializado = False

    def _cargar_audios(self):
        """Carga automáticamente todos los audios necesarios."""
        if not self.inicializado:
            return
        # Cargar efecto de sonido
        self.cargar_efecto("assets/audio/efecto.wav", "comer")
        # Cargar y reproducir música de fondo
        self.cargar_musica("assets/audio/soundtrack.wav", "música")

    def cargar_efecto(self, ruta: str, nombre: str = "efecto") -> bool:
        """Carga un efecto de sonido.

        Args:
            ruta: Ruta del archivo WAV
            nombre: Nombre descriptivo del efecto

        Retorna:
            True si se cargó correctamente, False si falló
        """
        if not self.inicializado:
            print(f"  ✗ Mezclador no inicializado, no se pudo cargar {nombre}")
            return False

        ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
        if os.path.exists(ruta_completa):
            try:
                if nombre == "comer":
                    self.sonido_comer = pygame.mixer.Sound(ruta_completa)
                print(f"  ✓ {nombre.capitalize()} cargado: {ruta}")
                return True
            except pygame.error as e:
                print(f"  ✗ Error cargando {nombre}: {e}")
                return False
        else:
            print(f"  ✗ No encontrado: {ruta}")
            return False

    def cargar_musica(self, ruta: str, nombre: str = "música") -> bool:
        """Carga y reproduce música de fondo en loop.

        Args:
            ruta: Ruta del archivo de música
            nombre: Nombre descriptivo

        Retorna:
            True si se cargó correctamente, False si falló
        """
        if not self.inicializado:
            print(f"  ✗ Mezclador no inicializado, no se pudo cargar {nombre}")
            return False

        ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
        if os.path.exists(ruta_completa):
            try:
                pygame.mixer.music.load(ruta_completa)
                pygame.mixer.music.play(-1)  # -1 = loop infinito
                print(f"  ✓ {nombre.capitalize()} cargada: {ruta}")
                return True
            except pygame.error as e:
                print(f"  ✗ Error cargando {nombre}: {e}")
                return False
        else:
            print(f"  ✗ No encontrado: {ruta}")
            return False

    def reproducir_efecto(self, efecto: str = "comer") -> bool:
        """Reproduce un efecto de sonido.

        Args:
            efecto: Tipo de efecto ('comer', etc.)

        Retorna:
            True si se reprodujo, False si no existe
        """
        try:
            if efecto == "comer" and self.sonido_comer:
                self.sonido_comer.play()
                return True
            else:
                return False
        except Exception as e:
            print(f"  ✗ Error reproduciendo {efecto}: {e}")
            return False

    def detener_musica(self):
        """Detiene la música de fondo."""
        if self.inicializado:
            pygame.mixer.music.stop()

    def pausar_musica(self):
        """Pausa la música de fondo."""
        if self.inicializado:
            pygame.mixer.music.pause()

    def reanudar_musica(self):
        """Reanuda la música de fondo."""
        if self.inicializado:
            pygame.mixer.music.unpause()

    def set_volumen_musica(self, volumen: float):
        """Establece el volumen de la música (0.0 a 1.0).

        Args:
            volumen: Valor entre 0.0 (silencio) y 1.0 (máximo)
        """
        if self.inicializado:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volumen)))

    def set_volumen_efecto(self, volumen: float):
        """Establece el volumen de los efectos (0.0 a 1.0).

        Args:
            volumen: Valor entre 0.0 (silencio) y 1.0 (máximo)
        """
        if self.sonido_comer and self.inicializado:
            self.sonido_comer.set_volume(max(0.0, min(1.0, volumen)))
