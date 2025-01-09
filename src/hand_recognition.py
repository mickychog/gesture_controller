import math
from .enums.gesture_enums import Gest, HLabel

class HandRecog:
    """
    Convierte los puntos de referencia de MediaPipe en gestos reconocibles utilizando **Visión Artificial**.
    """

    def __init__(self, hand_label):
        """
        Inicializa los atributos necesarios para el objeto HandRecog.

        Parameters
        ----------
        hand_label : int
            Representa la etiqueta de la mano (principal o secundaria) según el Enum `HLabel`.
        """
        self.finger = 0  # Estado de los dedos codificado en binario
        self.ori_gesture = Gest.PALM  # Gesto original detectado
        self.prev_gesture = Gest.PALM  # Gesto detectado en el frame anterior
        self.frame_count = 0  # Contador de frames desde la última actualización de `ori_gesture`
        self.hand_result = None  # Resultado de MediaPipe para la mano
        self.hand_label = hand_label  # Etiqueta de la mano (principal o secundaria)
        

    def update_hand_result(self, hand_result):
        """Actualiza los resultados de MediaPipe para la mano."""
        self.hand_result = hand_result

    def get_signed_dist(self, point):
        """
        Calcula la distancia euclidiana firmada entre dos puntos.

        Parameters
        ----------
        point : list
            Contiene dos elementos que representan los índices de los puntos de referencia.

        Returns
        -------
        float
        """
        if not self.hand_result or not self.hand_result.landmark:
            return 0.0

        sign = -1
        if self.hand_result.landmark[point[0]].y < self.hand_result.landmark[point[1]].y:
            sign = 1
        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x) ** 2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y) ** 2
        dist = math.sqrt(dist)
        return dist * sign

    def get_dist(self, point):
        """
        Calcula la distancia euclidiana entre dos puntos.

        Parameters
        ----------
        point : list
            Contiene dos elementos que representan los índices de los puntos de referencia.

        Returns
        -------
        float
        """
        if not self.hand_result or not self.hand_result.landmark:
            return 0.0

        dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x) ** 2
        dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y) ** 2
        dist = math.sqrt(dist)
        return dist

    def get_dz(self, point):
        """
        Calcula la diferencia absoluta en el eje Z entre dos puntos.

        Parameters
        ----------
        point : list
            Contiene dos elementos que representan los índices de los puntos de referencia.

        Returns
        -------
        float
        """
        if not self.hand_result or not self.hand_result.landmark:
            return 0.0

        return abs(self.hand_result.landmark[point[0]].z - self.hand_result.landmark[point[1]].z)

    def set_finger_state(self):
        """
        **Visión Artificial**: Actualiza el estado de los dedos evaluando la relación de distancia
        entre el punto de la punta, la articulación media y la base del dedo.

        Returns
        -------
        None
        """
        if not self.hand_result or not self.hand_result.landmark:
            return

        points = [[8, 5, 0], [12, 9, 0], [16, 13, 0], [20, 17, 0]] # Índice, Medio, Anular, Meñique
        self.finger = 0
        for idx, point in enumerate(points):
            dist = max(self.get_signed_dist(point[:2]), 0.01)  # Evitar división por cero
            dist2 = max(self.get_signed_dist(point[1:]), 0.01)
            ratio = round(dist / dist2, 1)
            self.finger = (self.finger << 1) | (1 if ratio > 0.5 else 0)
        

    def get_gesture(self):
        """
        **Visión Artificial**:Determina el gesto actual basado en el estado de los dedos y la distancia entre puntos clave.

        Returns
        -------
        int
            Gesto identificado según el Enum `Gest`.
        """
        if not self.hand_result or not self.hand_result.landmark:
            return Gest.PALM

        current_gesture = Gest.PALM
            # Detectar PINCH_MAJOR
        if self.finger in [Gest.LAST3, Gest.LAST4] and self.get_dist([8, 4]) < 0.05:
            current_gesture = Gest.PINCH_MAJOR

        # Detectar tres dedos del medio levantados para scroll
        elif self.finger == 0b01110:  # Índice, Medio y Anular levantados (binario: 01110)
            current_gesture = Gest.THREE_FINGER_SCROLL
            
        # if self.finger in [Gest.LAST3, Gest.LAST4] and self.get_dist([8, 4]) < 0.05:
        #     if self.hand_label == HLabel.MINOR:
        #         current_gesture = Gest.PINCH_MINOR
        #     else:
        #         current_gesture = Gest.PINCH_MAJOR

        # Detectar gestos como V_GEST, TWO_FINGER_CLOSED, etc.
        elif Gest.FIRST2 == self.finger:
            point = [[8, 12], [5, 9]]
            dist1 = self.get_dist(point[0])
            dist2 = self.get_dist(point[1])
            ratio = dist1 / dist2
            if ratio > 1.7:
                current_gesture = Gest.V_GEST
            else:
                if self.get_dz([8, 12]) < 0.1:
                    current_gesture = Gest.TWO_FINGER_CLOSED
                else:
                    current_gesture = Gest.MID
        else:
            current_gesture = self.finger

        if current_gesture == self.prev_gesture:
            self.frame_count += 1
        else:
            self.frame_count = 0

        self.prev_gesture = current_gesture

        if self.frame_count > 4:
            self.ori_gesture = current_gesture
        return self.ori_gesture
