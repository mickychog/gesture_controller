# Proyecto: Control por Gestos Basado en Visión Artificial

Este proyecto fue desarrollado por **Miguel Ángel Choque García** de la **Universidad San Francisco Xavier de Chuquisaca (USFX)** como parte de sus estudios en **desarrollo de aplicaciones inteligentes**. El objetivo principal es crear un sistema capaz de controlar aplicaciones utilizando gestos manuales capturados a través de una cámara.

## Descripción

El Gesture Controller permite la detección de gestos de manos para interactuar con el sistema. Utiliza herramientas como **OpenCV** y **MediaPipe** para implementar funcionalidades como control de volumen, brillo y desplazamiento mediante gestos específicos.

- **OpenCV (Visión por Computadora):**  
  OpenCV se utiliza para capturar imágenes desde la cámara, procesarlas (por ejemplo, cambiar el formato de color) y mostrar los resultados visuales en tiempo real. Es la base del manejo de imágenes en el proyecto.

- **MediaPipe (Visión Artificial):**  
  MediaPipe proporciona algoritmos avanzados de inteligencia artificial para detectar landmarks (puntos clave) en las manos y clasificarlas como izquierda o derecha. Estos landmarks son procesados posteriormente para interpretar los gestos del usuario.

### Ejemplo de Uso:
1. **Captura de imágenes con OpenCV:**  
   OpenCV abre la cámara, captura los frames de video y los prepara para el procesamiento posterior.

2. **Procesamiento de landmarks con MediaPipe:**  
   MediaPipe analiza las imágenes capturadas y detecta landmarks, permitiendo reconocer gestos como pinzas, puños y movimientos de los dedos.

## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

```
gesture_controller/
│
├── requirements.txt        # Lista de dependencias necesarias
├── README.md               # Documentación del proyecto
├── main.py                 # Archivo principal para iniciar el programa
│
├── src/                    # Código fuente principal
│   ├── __init__.py
│   ├── gesture_controller.py
│   ├── hand_recognition.py
│   ├── gesture_handlers.py
│   └── enums/
│       ├── __init__.py
│       └── gesture_enums.py
│
└── config/
    └── settings.py         # Configuración del sistema
```

## Instalación

Para configurar y ejecutar el proyecto, siga los pasos a continuación:

### Paso 1: Crear un entorno virtual con Conda
```bash
conda create --name gest python=3.8.5
```

### Paso 2: Activar el entorno virtual
```bash
conda activate gest
```

### Paso 3: Instalar las dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Instalar pywin32
```bash
conda install pywin32
```

## Dependencias

El proyecto utiliza las siguientes bibliotecas y versiones especificadas en el archivo `requirements.txt`:

- **opencv-python==4.5.3.56**: Captura y manejo de imágenes en tiempo real.
- **mediapipe==0.8.6.2**: Detección de landmarks y procesamiento de gestos con IA.
- **pyautogui==0.9.53**: Control del cursor y simulación de interacciones del ratón.
- **comtypes==1.1.11**: Comunicación con bibliotecas del sistema (usado para controlar el volumen).
- **pycaw==20181226**: Manejo del volumen del sistema.
- **screen-brightness-control==0.9.0**: Ajuste del brillo del sistema.

## Uso

Ejecute el archivo principal para iniciar el sistema:

```bash
python main.py
```

El sistema abrirá la cámara y comenzará a procesar los gestos en tiempo real. Los gestos reconocidos se utilizarán para realizar acciones específicas como ajustar el volumen, cambiar el brillo o desplazarse por la pantalla.

## Créditos

Este proyecto fue desarrollado por **Miguel Ángel Choque García**, estudiante de la USFX, como parte de su formación en Desarrollo de Aplicaciones Inteligentes.

---

¡Gracias por revisar este proyecto! Para preguntas o sugerencias, no dude en contactarme.

