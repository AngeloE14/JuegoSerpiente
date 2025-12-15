# Juego Serpiente 🐍🍎

Un juego clásico de Snake (Serpiente) implementado en Python usando Pygame, con gráficos personalizados, efectos de sonido, música de fondo y cursores animados.

## 📋 Descripción

Este es un juego completo de la serpiente con las siguientes características:
- **Interfaz gráfica completa** con menú principal
- **Efectos visuales** incluyendo animaciones de la manzana y ojos para la serpiente
- **Sistema de audio** con música de fondo y efectos de sonido
- **Cursores personalizados** que cambian según el estado del juego
- **Control de volumen** desde el menú principal
- **Sistema de puntaje** en tiempo real

## 🎮 Características del Juego

### Jugabilidad
- Control fluido de la serpiente con las teclas de dirección
- La serpiente crece al comer manzanas
- El juego termina si la serpiente choca con los bordes o consigo misma
- Animaciones suaves y efectos visuales atractivos

### Elementos Visuales
- Fondo personalizado
- Sprite animado de manzana con efecto de pulsación
- Serpiente con ojos que miran en la dirección del movimiento
- Notificación visual al perder
- Cursores temáticos según el estado del juego

### Audio
- Música de fondo en loop
- Efecto de sonido al comer
- Efecto de sonido al perder
- Control de volumen on/off desde el menú

## 🔧 Requisitos

### Software Necesario
- **Python 3.10 o superior**
- **Pygame 2.6 o superior**

### Instalación de Dependencias

```bash
# Instalar Python (si no está instalado)
# Visita: https://www.python.org/downloads/

# Instalar Pygame
pip install pygame
```

## 🚀 Cómo Ejecutar

1. Clona el repositorio:
```bash
git clone https://github.com/AngeloE14/JuegoSerpiente.git
cd JuegoSerpiente
```

2. Asegúrate de tener las dependencias instaladas:
```bash
pip install pygame
```

3. Ejecuta el juego:
```bash
python main.py
```

## 🎯 Controles

### Menú Principal
- **↑/↓ (Flechas)**: Navegar opciones
- **Enter/Espacio**: Seleccionar opción
- **Esc**: Salir del juego

### Durante el Juego
- **↑ (Flecha Arriba)**: Mover arriba
- **↓ (Flecha Abajo)**: Mover abajo
- **← (Flecha Izquierda)**: Mover izquierda
- **→ (Flecha Derecha)**: Mover derecha
- **Esc**: Volver al menú principal

## 📁 Estructura del Proyecto

```
JuegoSerpiente/
├── main.py                 # Punto de entrada de la aplicación
├── menu.py                 # Sistema de menú principal
├── ventana.py             # Lógica principal del juego y renderizado
├── juego.py               # Lógica del juego (colisiones, puntaje)
├── serpiente.py           # Clase Serpiente y direcciones
├── comida.py              # Generación de manzanas
├── audio.py               # Gestor de audio (música y efectos)
├── cursores.py            # Gestor de cursores personalizados
├── assets/                # Recursos del juego
│   ├── images/           # Imágenes y sprites
│   │   ├── fondo.png     # Fondo del juego
│   │   ├── manzana.png   # Sprite de la manzana
│   │   ├── iconito.png   # Icono de la ventana
│   │   └── notificacion.png  # Notificación de game over
│   ├── audio/            # Archivos de audio
│   │   ├── soundtrack.wav    # Música de fondo
│   │   ├── efecto.wav        # Sonido al comer
│   │   └── perdio.wav        # Sonido al perder
│   └── cursores_juego/   # Cursores personalizados
│       ├── cursores/     # Imágenes de cursores
│       └── License.txt   # Licencia de los cursores
├── tools/                # Herramientas de utilidad
│   └── strip_png_iccp.py # Script para limpiar metadatos PNG
├── LICENSE               # Licencia MIT
└── README.md            # Este archivo
```

## 📦 Módulos y Componentes

### main.py
Punto de entrada de la aplicación que inicia el menú principal.

### menu.py
**Clase: `MenuPrincipal`**
- Gestiona el menú principal del juego
- Opciones: Jugar, Control de Música (ON/OFF), Salir
- Maneja la navegación y selección de opciones
- Carga y cachea assets para reutilización

**Función: `inicio_aplicacion()`**
- Bucle principal que alterna entre menú y juego
- Gestiona el flujo de la aplicación

### ventana.py
**Función: `principal()`**
- Bucle principal del juego
- Renderiza la serpiente, manzanas y el puntaje
- Maneja la entrada del usuario
- Implementa animaciones visuales:
  - Pulsación de la manzana
  - Ojos de la serpiente según dirección
- Gestiona estados del juego (jugando, perdió)

### juego.py
**Clase: `Juego`**
- **Atributos**:
  - `columnas`, `filas`: Dimensiones del tablero
  - `puntaje`: Puntaje actual
  - `serpiente`: Instancia de la clase Serpiente
  - `manzana`: Posición actual de la manzana
  
- **Métodos**:
  - `reiniciar()`: Reinicia el juego
  - `establecer_direccion(direccion)`: Cambia dirección de la serpiente
  - `fuera_de_limites(pos)`: Verifica límites del tablero
  - `paso()`: Avanza un paso del juego, retorna estado

### serpiente.py
**Constantes de Dirección**:
- `ARRIBA = (0, -1)`
- `ABAJO = (0, 1)`
- `IZQUIERDA = (-1, 0)`
- `DERECHA = (1, 0)`

**Clase: `Serpiente`**
- **Atributos**:
  - `cuerpo`: Lista de coordenadas (tuplas)
  - `direccion`: Dirección actual de movimiento

- **Métodos**:
  - `cabeza()`: Retorna posición de la cabeza
  - `establecer_direccion(nueva)`: Cambia dirección (evita 180°)
  - `mover(crecer)`: Mueve la serpiente
  - `se_colisiona_con_su_cuerpo()`: Detecta auto-colisión
  - `ocupa()`: Retorna lista de posiciones ocupadas

### comida.py
**Función: `generar_manzana(columnas, filas, ocupadas)`**
- Genera posición aleatoria para la manzana
- Evita posiciones ocupadas por la serpiente
- Retorna tupla (x, y)

### audio.py
**Clase: `GestorAudio`**
- Inicializa pygame.mixer
- Carga efectos de sonido y música
- **Métodos**:
  - `cargar_efecto(ruta, nombre)`: Carga un efecto de sonido
  - `cargar_musica(ruta)`: Carga y reproduce música en loop
  - `reproducir_sonido(efecto)`: Reproduce efecto específico
  - `pausar_musica()`, `reanudar_musica()`: Control de música
  - `set_volumen_musica(volumen)`: Ajusta volumen de música
  - `set_volumen_efecto(volumen)`: Ajusta volumen de efectos

### cursores.py
**Clase: `GestorCursores`**
- Gestiona cursores personalizados del juego
- **Cursores disponibles**:
  - `normal`: Cursor estándar
  - `menu`: Cursor para el menú
  - `juego`: Cursor durante el juego
  - `comer`: Cursor especial al comer (estrella)
  - `perdio`: Cursor al perder (X)

- **Métodos**:
  - `establecer_cursor(nombre)`: Cambia al cursor especificado
  - Métodos específicos para cada tipo de cursor

## 🎨 Assets

### Imágenes
- **fondo.png**: Fondo del juego (800x400 px)
- **manzana.png**: Sprite de la manzana (20x20 px escalable)
- **iconito.png**: Icono de la ventana de la aplicación
- **notificacion.png**: Imagen de game over

### Audio
- **soundtrack.wav**: Música de fondo en loop
- **efecto.wav**: Sonido al comer una manzana
- **perdio.wav**: Sonido al perder el juego

### Cursores
Conjunto de cursores personalizados en formato PNG ubicados en `assets/cursores_juego/cursores/`

## 🛠️ Desarrollo

### Configuración del Proyecto
El juego utiliza las siguientes constantes configurables (en `ventana.py`):

```python
ANCHO, ALTO = 800, 400            # Dimensiones de la ventana
TAMANO_CELDA = 20                 # Tamaño de cada celda del grid
COLUMNAS = ANCHO // TAMANO_CELDA  # Número de columnas (calculado: 40)
FILAS = ALTO // TAMANO_CELDA      # Número de filas (calculado: 20)
COLOR_SERPIENTE = (0, 51, 102)    # Color de la serpiente (RGB)
COLOR_MANZANA = (231, 76, 60)     # Color fallback de la manzana
```

### Herramientas Incluidas

**strip_png_iccp.py**
- Script de utilidad para limpiar perfiles ICC de imágenes PNG
- Previene advertencias de libpng
- Uso: `python tools/strip_png_iccp.py`

### Arquitectura del Código

El juego sigue un diseño modular:
1. **Separación de responsabilidades**: Cada módulo tiene una función específica
2. **Reutilización de recursos**: Assets se cargan una vez y se comparten
3. **Gestión de estado**: El flujo del juego se maneja mediante estados retornados
4. **Manejo de errores**: Fallbacks para assets faltantes o errores de audio

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ideas para Mejoras
- Sistema de niveles con velocidad incremental
- Power-ups y obstáculos
- Tabla de mejores puntajes (high scores)
- Modo multijugador
- Temas visuales alternativos
- Soporte para gamepad/joystick

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

**Copyright (c) 2025 Angelo**

## 👤 Autor

**Angelo**
- GitHub: [@AngeloE14](https://github.com/AngeloE14)

## 🙏 Agradecimientos

- Pygame community por la excelente librería
- Inspiración del clásico juego Snake
- Recursos de cursores bajo licencia (ver `assets/cursores_juego/License.txt`)

---

**¡Disfruta del juego! 🐍🍎**