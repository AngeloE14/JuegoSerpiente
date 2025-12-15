# Juego Serpiente 🐍🍎

Un juego clásico de Snake implementado en Python utilizando Pygame, con gráficos mejorados, efectos de sonido y una interfaz de usuario pulida.

## 📝 Descripción

Este proyecto es una implementación moderna del juego clásico Snake, donde el jugador controla una serpiente que debe comer manzanas para crecer, evitando chocar con las paredes o con su propio cuerpo. El juego incluye:

- **Interfaz gráfica atractiva**: Fondo personalizado, sprites animados y efectos visuales
- **Sistema de audio**: Música de fondo y efectos de sonido para diferentes acciones
- **Menú interactivo**: Navegación fácil con opciones para jugar y controlar el sonido
- **Cursores personalizados**: Diferentes cursores para diferentes estados del juego
- **Animaciones**: La manzana tiene una animación de pulsación suave
- **Ojos de la serpiente**: La cabeza de la serpiente tiene ojos que miran en la dirección del movimiento

## ✨ Características

- 🎮 Mecánicas clásicas del juego Snake
- 🎨 Gráficos personalizados con sprites y fondos
- 🔊 Sistema de audio con música y efectos de sonido
- 🎯 Sistema de puntuación
- 🖱️ Cursores personalizados para diferentes estados del juego
- 📱 Menú principal con opciones
- 🔄 Reinicio automático al perder
- ⌨️ Controles intuitivos con teclado
- 🎭 Animaciones suaves

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje de programación principal
- **Pygame 2.6+**: Biblioteca para desarrollo de juegos y gráficos
- **Arquitectura modular**: Código organizado en módulos separados para fácil mantenimiento

## 📋 Requisitos

- Python 3.10 o superior
- Pygame 2.6 o superior

## 🚀 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/AngeloE14/JuegoSerpiente.git
cd JuegoSerpiente
```

2. Instala las dependencias:
```bash
pip install pygame>=2.6
```

## 🎮 Cómo Jugar

1. Ejecuta el juego:
```bash
python main.py
```

2. En el menú principal:
   - Usa las **flechas** (↑/↓) para navegar entre opciones
   - Presiona **Enter** o **Espacio** para seleccionar
   - Selecciona "Jugar" para comenzar una partida
   - Selecciona "Música" para activar/desactivar el audio
   - Selecciona "Salir" para cerrar el juego

## 🕹️ Controles

### En el Menú
- **↑/↓**: Navegar entre opciones
- **Enter/Espacio**: Seleccionar opción
- **Esc**: Salir del juego

### En el Juego
- **↑**: Mover hacia arriba
- **↓**: Mover hacia abajo
- **←**: Mover hacia la izquierda
- **→**: Mover hacia la derecha
- **Esc**: Volver al menú principal

## 📁 Estructura del Proyecto

```
JuegoSerpiente/
├── main.py              # Punto de entrada de la aplicación
├── menu.py              # Menú principal y lógica de navegación
├── ventana.py           # Ventana principal del juego y renderizado
├── juego.py             # Lógica principal del juego (reglas, colisiones)
├── serpiente.py         # Clase Serpiente y direcciones
├── comida.py            # Generación de manzanas
├── audio.py             # Gestor de música y efectos de sonido
├── cursores.py          # Gestor de cursores personalizados
├── assets/              # Recursos del juego
│   ├── audio/          # Música y efectos de sonido
│   │   ├── efecto.wav
│   │   ├── perdio.wav
│   │   └── soundtrack.wav
│   ├── images/         # Imágenes y sprites
│   │   ├── fondo.png
│   │   ├── manzana.png
│   │   ├── iconito.png
│   │   └── notificacion.png
│   └── cursores_juego/ # Cursores personalizados
└── README.md           # Este archivo
```

## 🎯 Cómo Funciona

### Módulos Principales

- **main.py**: Punto de entrada que inicia la aplicación llamando al menú principal
- **menu.py**: Maneja el menú principal con opciones de juego y configuración de audio
- **ventana.py**: Contiene la lógica de renderizado del juego, incluyendo la serpiente, manzanas y HUD
- **juego.py**: Implementa las reglas del juego, detección de colisiones y sistema de puntuación
- **serpiente.py**: Define la clase Serpiente con sus movimientos y comportamiento
- **comida.py**: Genera posiciones aleatorias para las manzanas
- **audio.py**: Gestiona la carga y reproducción de música y efectos de sonido
- **cursores.py**: Maneja los cursores personalizados para diferentes estados del juego

### Mecánicas del Juego

1. La serpiente comienza en el centro de la pantalla moviéndose hacia la derecha
2. El jugador controla la dirección con las teclas de flecha
3. La serpiente no puede girar 180° instantáneamente (no puede ir directamente de derecha a izquierda)
4. Al comer una manzana, la serpiente crece y se suma un punto
5. El juego termina si la serpiente choca con las paredes o consigo misma
6. Al perder, se muestra una notificación y se regresa al menú principal

## 🎨 Características Visuales

- **Fondo personalizado**: Imagen de fondo temática
- **Animación de manzana**: La manzana pulsa suavemente para llamar la atención
- **Ojos de la serpiente**: La cabeza tiene ojos que miran en la dirección del movimiento
- **Cursores personalizados**: Diferentes cursores para el menú, juego, al comer y al perder
- **Notificación de pérdida**: Imagen especial cuando el jugador pierde

## 🔊 Sistema de Audio

- **Música de fondo**: Soundtrack continuo durante el juego
- **Efecto de comer**: Sonido al comer una manzana
- **Efecto de perder**: Sonido al finalizar el juego
- **Control de volumen**: Opción para activar/desactivar el audio desde el menú

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

Angelo - [AngeloE14](https://github.com/AngeloE14)

## 🙏 Créditos

- Cursores del juego proporcionados por recursos de terceros (ver `assets/cursores_juego/License.txt`)
- Concepto basado en el juego clásico Snake

---

¡Disfruta jugando! 🎮✨