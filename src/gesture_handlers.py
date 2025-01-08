import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Verificar si el módulo screen_brightness_control está disponible
try:
    import screen_brightness_control as sbcontrol
except ImportError:
    sbcontrol = None

from .enums.gesture_enums import Gest, HLabel

class Controller:
    """
    Clase que ejecuta comandos según los gestos detectados.

    Atributos
    ----------
    tx_old : int
        Coordenada X anterior del cursor.
    ty_old : int
        Coordenada Y anterior del cursor.
    flag : bool
        Indica si se ha detectado el gesto en "V".
    grabflag : bool
        Indica si se ha detectado el gesto "puño cerrado" (FIST).
    pinchmajorflag : bool
        Indica si se ha detectado el gesto "pinza" con la mano principal.
    pinchminorflag : bool
        Indica si se ha detectado el gesto "pinza" con la mano secundaria.
    pinchstartxcoord : int
        Coordenada X inicial al comenzar el gesto de pinza.
    pinchstartycoord : int
        Coordenada Y inicial al comenzar el gesto de pinza.
    pinchdirectionflag : bool
        Indica si el movimiento del gesto de pinza es en el eje X (True) o en el eje Y (False).
    prevpinchlv : int
        Desplazamiento previo cuantificado del gesto de pinza desde la posición inicial.
    pinchlv : int
        Desplazamiento actual cuantificado del gesto de pinza desde la posición inicial.
    framecount : int
        Número de frames desde que se actualizó `pinchlv`.
    prev_hand : tuple
        Coordenadas (x, y) de la mano en el frame anterior.
    pinch_threshold : float
        Tamaño del paso para cuantificar `pinchlv`.
    """

    tx_old = 0
    ty_old = 0
    flag = False
    grabflag = False
    pinchmajorflag = False
    pinchminorflag = False
    pinchstartxcoord = None
    pinchstartycoord = None
    pinchdirectionflag = None
    prevpinchlv = 0
    pinchlv = 0
    framecount = 0
    prev_hand = None
    pinch_threshold = 0.3

    @staticmethod
    def changesystembrightness():
        """Ajusta el brillo del sistema según el valor de `Controller.pinchlv`."""
        if not sbcontrol:
            print("Control de brillo no disponible.")
            return

        currentBrightnessLv = sbcontrol.get_brightness(display=0) / 100.0
        currentBrightnessLv += Controller.pinchlv / 50.0
        currentBrightnessLv = min(max(currentBrightnessLv, 0.0), 1.0)  # Limitar entre 0.0 y 1.0
        sbcontrol.fade_brightness(int(100 * currentBrightnessLv), start=sbcontrol.get_brightness(display=0))

    @staticmethod
    def changesystemvolume():
        """Ajusta el volumen del sistema según el valor de `Controller.pinchlv`."""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            currentVolumeLv = volume.GetMasterVolumeLevelScalar()
            currentVolumeLv += Controller.pinchlv / 50.0
            currentVolumeLv = min(max(currentVolumeLv, 0.0), 1.0)  # Limitar entre 0.0 y 1.0
            volume.SetMasterVolumeLevelScalar(currentVolumeLv, None)
        except Exception as e:
            print(f"Error al ajustar el volumen: {e}")

    @staticmethod
    def scrollVertical():
        """Realiza un desplazamiento vertical en pantalla."""
        pyautogui.scroll(120 if Controller.pinchlv > 0.0 else -120)

    @staticmethod
    def scrollHorizontal():
        """Realiza un desplazamiento horizontal en pantalla."""
        pyautogui.keyDown('shift')
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(-120 if Controller.pinchlv > 0.0 else 120)
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')

    @staticmethod
    def get_position(hand_result):
        """
        Devuelve las coordenadas actuales de la posición de la mano.

        Localiza la mano para obtener la posición del cursor y estabiliza el cursor
        suavizando movimientos bruscos.

        Returns
        -------
        tuple(float, float)
        """
        point = 9
        position = [hand_result.landmark[point].x, hand_result.landmark[point].y]
        sx, sy = pyautogui.size()
        x_old, y_old = pyautogui.position()
        x = int(position[0] * sx)
        y = int(position[1] * sy)
        if Controller.prev_hand is None:
            Controller.prev_hand = (x, y)

        delta_x = x - Controller.prev_hand[0]
        delta_y = y - Controller.prev_hand[1]

        distsq = delta_x**2 + delta_y**2
        ratio = 1
        Controller.prev_hand = (x, y)

        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** 0.5)
        else:
            ratio = 2.1
        x, y = x_old + delta_x * ratio, y_old + delta_y * ratio
        return (x, y)

    @staticmethod
    def pinch_control_init(hand_result):
        """Inicializa los atributos para el gesto de pinza."""
        Controller.pinchstartxcoord = hand_result.landmark[8].x
        Controller.pinchstartycoord = hand_result.landmark[8].y
        Controller.pinchlv = 0
        Controller.prevpinchlv = 0
        Controller.framecount = 0

    @staticmethod
    def pinch_control(hand_result, controlHorizontal, controlVertical):
        """
        Llama a `controlHorizontal` o `controlVertical` según el movimiento del gesto de pinza.

        Parameters
        ----------
        hand_result : Object
            Landmarks obtenidos de MediaPipe.
        controlHorizontal : función de callback para gestos horizontales.
        controlVertical : función de callback para gestos verticales.
        """
        if Controller.framecount == 5:
            Controller.framecount = 0
            Controller.pinchlv = Controller.prevpinchlv

            if Controller.pinchdirectionflag:
                controlHorizontal()  # Eje X
            else:
                controlVertical()  # Eje Y

        lvx = Controller.get_position(hand_result)[0] - Controller.pinchstartxcoord
        lvy = Controller.get_position(hand_result)[1] - Controller.pinchstartycoord
        
        if abs(lvy) > abs(lvx) and abs(lvy) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = False
            if abs(Controller.prevpinchlv - lvy) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvy
                Controller.framecount = 0

        elif abs(lvx) > Controller.pinch_threshold:
            Controller.pinchdirectionflag = True
            if abs(Controller.prevpinchlv - lvx) < Controller.pinch_threshold:
                Controller.framecount += 1
            else:
                Controller.prevpinchlv = lvx
                Controller.framecount = 0

    @staticmethod
    def handle_controls(gesture, hand_result):
        """Implementa la funcionalidad para todos los gestos detectados."""      
        x, y = None, None
        if gesture != Gest.PALM:
            x, y = Controller.get_position(hand_result)

        # Reinicio de banderas
        if gesture != Gest.FIST and Controller.grabflag:
            Controller.grabflag = False
            pyautogui.mouseUp(button="left")

        if gesture != Gest.PINCH_MAJOR and Controller.pinchmajorflag:
            Controller.pinchmajorflag = False

        if gesture != Gest.PINCH_MINOR and Controller.pinchminorflag:
            Controller.pinchminorflag = False

        # Implementación de gestos
        if gesture == Gest.V_GEST:
            Controller.flag = True
            pyautogui.moveTo(x, y, duration=0.1)

        elif gesture == Gest.FIST:
            if not Controller.grabflag: 
                Controller.grabflag = True
                pyautogui.mouseDown(button="left")
            pyautogui.moveTo(x, y, duration=0.1)

        elif gesture == Gest.MID and Controller.flag:
            pyautogui.click()
            Controller.flag = False

        elif gesture == Gest.INDEX and Controller.flag:
            pyautogui.click(button='right')
            Controller.flag = False

        elif gesture == Gest.TWO_FINGER_CLOSED and Controller.flag:
            pyautogui.doubleClick()
            Controller.flag = False

        elif gesture == Gest.PINCH_MINOR:
            if not Controller.pinchminorflag:
                Controller.pinch_control_init(hand_result)
                Controller.pinchminorflag = True
            Controller.pinch_control(hand_result, Controller.scrollHorizontal, Controller.scrollVertical)
        
        elif gesture == Gest.PINCH_MAJOR:
            if not Controller.pinchmajorflag:
                Controller.pinch_control_init(hand_result)
                Controller.pinchmajorflag = True
            Controller.pinch_control(hand_result, Controller.changesystembrightness, Controller.changesystemvolume)
