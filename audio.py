import os
import pygame


class GestorAudio:
    def __init__(self):
        self.sonido_comer = None
        self.sonido_perder = None
        self.inicializado = False
        try:
            pygame.mixer.init()
            self.inicializado = True
        except:
            pass
        
        if self.inicializado:
            self._cargar_audios()

    def _cargar_audios(self):
        self.cargar_efecto("assets/audio/efecto.wav", "comer")
        self.cargar_efecto("assets/audio/perdio.wav", "perder")
        self.cargar_musica("assets/audio/soundtrack.wav")

    def cargar_efecto(self, ruta: str, nombre: str = "efecto") -> bool:
        if not self.inicializado:
            return False
        ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
        if not os.path.exists(ruta_completa):
            return False
        try:
            if nombre == "comer":
                self.sonido_comer = pygame.mixer.Sound(ruta_completa)
            elif nombre == "perder":
                self.sonido_perder = pygame.mixer.Sound(ruta_completa)
            return True
        except:
            return False

    def cargar_musica(self, ruta: str) -> bool:
        if not self.inicializado:
            return False
        ruta_completa = os.path.join(os.path.dirname(__file__), ruta)
        if not os.path.exists(ruta_completa):
            return False
        try:
            pygame.mixer.music.load(ruta_completa)
            pygame.mixer.music.play(-1)
            return True
        except:
            return False

    def reproducir_sonido(self, efecto: str = "comer") -> bool:
        if efecto == "comer" and self.sonido_comer:
            self.sonido_comer.play()
            return True
        if efecto == "perder" and self.sonido_perder:
            self.sonido_perder.play()
            return True
        return False

    def detener_musica(self):
        if self.inicializado:
            pygame.mixer.music.stop()

    def pausar_musica(self):
        if self.inicializado:
            pygame.mixer.music.pause()

    def reanudar_musica(self):
        if self.inicializado:
            pygame.mixer.music.unpause()

    def set_volumen_musica(self, volumen: float):
        if self.inicializado:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volumen)))

    def set_volumen_efecto(self, volumen: float):
        if self.sonido_comer:
            self.sonido_comer.set_volume(max(0.0, min(1.0, volumen)))
        if self.sonido_perder:
            self.sonido_perder.set_volume(max(0.0, min(1.0, volumen)))
