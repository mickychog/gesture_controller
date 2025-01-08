from enum import IntEnum

# Codificaciones de gestos
class Gest(IntEnum):
    """
    Enumeración para mapear todos los gestos de la mano a un número binario.
    """

    FIST = 0  # Puño cerrado
    PINKY = 1  # Solo meñique levantado
    RING = 2  # Solo anular levantado
    MID = 4  # Solo medio levantado
    LAST3 = 7  # Últimos tres dedos levantados
    INDEX = 8  # Solo índice levantado
    FIRST2 = 12  # Primeros dos dedos levantados
    LAST4 = 15  # Últimos cuatro dedos levantados
    THUMB = 16  # Solo pulgar levantado
    PALM = 31  # Mano abierta completamente

    # Mapas adicionales para gestos
    V_GEST = 33  # Gesto en forma de "V" (paz)
    TWO_FINGER_CLOSED = 34  # Dos dedos juntos cerrados
    PINCH_MAJOR = 35  # Gesto de pinza con mano principal
    PINCH_MINOR = 36  # Gesto de pinza con mano secundaria
    THREE_FINGER_SCROLL = 37  # Tres dedos extendidos para scroll

    
    # Gesto no reconocido
    UNKNOWN = -1  # Valor predeterminado para gestos no reconocidos


# Etiquetas de multi-mano
class HLabel(IntEnum):
    """
    Etiquetas para la clasificación de las manos (izquierda, derecha).
    """
    MINOR = 0  # Mano secundaria (izquierda o menos dominante)
    MAJOR = 1  # Mano principal (derecha o más dominante)
