# Proyecto: Gesture Controller

Este proyecto fue desarrollado por **Miguel Ángel Choque García** de la **Universidad San Francisco Xavier de Chuquisaca (USFX)** como parte de sus estudios en **desarrollo de aplicaciones inteligentes**. El objetivo principal es crear un sistema capaz de controlar aplicaciones utilizando gestos manuales capturados a través de una cámara.

## Descripción

El Gesture Controller permite la detección de gestos de manos para interactuar con el sistema. Utiliza herramientas como OpenCV, MediaPipe y otras bibliotecas para implementar funcionalidades como control de volumen, brillo y desplazamiento mediante gestos específicos.

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

- **opencv-python==4.5.3.56**
- **mediapipe==0.8.6.2**
- **pyautogui==0.9.53**
- **comtypes==1.1.11**
- **pycaw==20181226**
- **screen-brightness-control==0.9.0**
- **google-protobuf>=3.19.0**

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

