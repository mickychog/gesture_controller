import time
import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
from .hand_recognition import HandRecog
from .gesture_handlers import Controller
from .enums.gesture_enums import HLabel, Gest
from config.settings import (
    CAMERA_INDEX,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    MAX_NUM_HANDS,
    WINDOW_NAME
)

# Inicialización de MediaPipe para detección de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class GestureController:
    """
    Maneja la cámara, obtiene los puntos de referencia (landmarks) de MediaPipe,
    y sirve como punto de entrada para todo el programa.

    Atributos
    ----------
    gc_mode : int
        indica si el controlador de gestos está ejecutándose o no,
        1 si está ejecutándose, 0 si no.
    cap : Object
        objeto obtenido de cv2, para capturar frames de video.
    CAM_HEIGHT : int
        altura en píxeles del frame obtenido de la cámara.
    CAM_WIDTH : int
        ancho en píxeles del frame obtenido de la cámara.
    hr_major : Object de 'HandRecog'
        objeto que representa la mano principal.
    hr_minor : Object de 'HandRecog'
        objeto que representa la mano secundaria.
    dom_hand : bool
        True si la mano derecha es la dominante, False en caso contrario.
        Por defecto es True.
    """
    gc_mode = 0
    cap = None
    CAM_HEIGHT = None
    CAM_WIDTH = None
    hr_major = None  # Mano derecha por defecto
    hr_minor = None  # Mano izquierda por defecto
    dom_hand = True

    def __init__(self):
        """Inicializa los atributos y configura la captura de video."""
        GestureController.gc_mode = 1
        GestureController.cap = cv2.VideoCapture(CAMERA_INDEX)
        if not GestureController.cap.isOpened():
            raise RuntimeError("No se pudo acceder a la cámara.")
        GestureController.CAM_HEIGHT = GestureController.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        GestureController.CAM_WIDTH = GestureController.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    @staticmethod
    def classify_hands(results):
        """
        Establece 'hr_major' y 'hr_minor' basándose en la clasificación (izquierda, derecha)
        de la mano obtenida de MediaPipe. Utiliza 'dom_hand' para decidir qué mano es
        la principal y cuál la secundaria.
        """
        left, right = None, None
        try:
            handedness_dict = MessageToDict(results.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[0]
            else:
                left = results.multi_hand_landmarks[0]
        except:
            pass

        try:
            handedness_dict = MessageToDict(results.multi_handedness[1])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[1]
            else:
                left = results.multi_hand_landmarks[1]
        except:
            pass
        
        if GestureController.dom_hand:
            GestureController.hr_major = right
            GestureController.hr_minor = left
        else:
            GestureController.hr_major = left
            GestureController.hr_minor = right

    def start(self):
        """
        Punto de entrada del programa completo. Captura frames de video,
        obtiene landmarks de MediaPipe y los pasa a 'handmajor' y 'handminor'
        para su control.
        
        El método realiza un bucle continuo que:
        1. Captura frames de la cámara
        2. Procesa cada frame para detectar manos
        3. Clasifica las manos detectadas
        4. Actualiza el estado de los dedos
        5. Detecta gestos
        6. Ejecuta controles basados en los gestos
        7. Muestra el resultado visual
        """
        handmajor = HandRecog(HLabel.MAJOR)
        handminor = HandRecog(HLabel.MINOR)

        last_frame_time = time.time()
        
        with mp_hands.Hands(
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        ) as hands:
            while GestureController.cap.isOpened() and GestureController.gc_mode:
                current_time = time.time()
                if current_time - last_frame_time < 1 / 15:  # Limitar a 15 FPS
                    continue
                last_frame_time = current_time
                
                # **Visión por Computadora**: Captura de la cámara y detección de manos
                success, image = GestureController.cap.read()

                if not success:
                    print("Ignorando frame vacío de la cámara.")
                    continue
                
                # Convertir la imagen a RGB para MediaPipe
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                
                # Convertir de vuelta a BGR para OpenCV
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                 # **Visión Artificial**: Uso de landmarks para reconocer gestos
                if results.multi_hand_landmarks:                   
                    GestureController.classify_hands(results)
                    handmajor.update_hand_result(GestureController.hr_major)
                    handminor.update_hand_result(GestureController.hr_minor)

                    handmajor.set_finger_state()
                    handminor.set_finger_state()
                    gest_name = handminor.get_gesture()

                # Asegurarse de que gest_name sea un miembro del enum Gest
                    try:
                        gest_name = Gest(gest_name)
                    except ValueError:
                        print(f"Gesto no reconocido: {gest_name}")
                        continue
                
                # Mostrar el gesto reconocido en consola
                    if gest_name == Gest.PINCH_MINOR:
                        print(f"Gesto reconocido: {gest_name.name} (Pinza menor - Desplazamiento)")
                        Controller.handle_controls(gest_name, handminor.hand_result)
                    else:
                        gest_name = Gest(handmajor.get_gesture())  # Convertir también aquí
                        print(f"Gesto reconocido: {gest_name.name} (Pinza mayor - Volumen/Brillo)")
                        Controller.handle_controls(gest_name, handmajor.hand_result)
                    
                    # Dibuja los landmarks de las manos
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, 
                            hand_landmarks, 
                            mp_hands.HAND_CONNECTIONS
                        )
                else:
                    Controller.prev_hand = None
                    
                cv2.imshow(WINDOW_NAME, image)
                if cv2.waitKey(5) & 0xFF == 13:  # Presionar Enter para salir
                    break
                    
        GestureController.cap.release()
        cv2.destroyAllWindows()