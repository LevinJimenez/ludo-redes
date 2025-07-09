class Color:
    GREEN = '#0CED2C'
    # Define el color verde.
    RED = '#F71313'
    # Define el color rojo.
    YELLOW = '#FFFF00'
    # Defin"#9b6f6f"r amarillo.
    BLUE = '#3575EC'
    # Define el color azul.
    DEFAULT = '#E9E9E9'
    # Define un color gris claro por defecto.
    CYAN = '#4EB1BA'
    # Define el color cian.
    GRAY = '#A9A9A9'
    # Define un color gris oscuro.


class Board:
    # Define la clase Board para almacenar dimensiones y puntos clave del tablero.
    SQUARE_SIZE = 40
    # Tamaño de un cuadrado individual en el tablero.
    PANEL_WIDTH = 600
    # Ancho del panel principal de la interfaz.
    PANEL_HEIGHT = 640
    # Alto del panel principal de la interfaz.
    BOARD_WIDTH = 640
    # Ancho total del área del tablero.
    BOARD_HEIGHT = 640
    # Alto total del área del tablero.
    POINTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
    # Puntos de coordenadas (posiblemente para esquinas o áreas base).
    POSITIVE_V = [(6, 2), (8, 1), (6, 13), (8, 12)]
    # Puntos específicos verticales (posiblemente seguros o de inicio/fin).
    POSITIVE_H = [(1, 6), (2, 8), (13, 8), (12, 6)]
    # Puntos específicos horizontales (posiblemente seguros o de inicio/fin).


class Text:
    # Define la clase Text para almacenar cadenas de texto estáticas.
    MADE_BY = 'Made By: César, Levin, Ainhoa, Jesus y Lilian'
    # Créditos de los creadores.
    HEADER =  'LUDO Multiplayer'
    # Título del juego.

class Path:
    # Define la clase Path para gestionar las coordenadas de los caminos de las fichas.

    def __init__(self):
        # Constructor de la clase Path.

        self.green_path = []
        # Lista para almacenar las coordenadas del camino verde.
        self.red_path = []
        # Lista para almacenar las coordenadas del camino rojo.
        self.blue_path = []
        # Lista para almacenar las coordenadas del camino azul.
        self.yellow_path = []
        # Lista para almacenar las coordenadas del camino amarillo.
        self.gx = None
        # Coordenada X genérica para cálculos de camino.
        self.gy = None
        # Coordenada Y genérica para cálculos de camino.
        self.ry = None
        # Coordenada Y específica para el camino rojo.
        self.by = None
        # Coordenada Y específica para el camino azul.
        self.count = None
        # Número de pasos en una sección del camino.

    def update_coordinates(self, gx, gy, ry, by, count):
        # Actualiza las coordenadas y el contador para el cálculo del camino.

        self.gx = gx
        # Actualiza gx.
        self.gy = gy
        # Actualiza gy.
        self.ry = ry
        # Actualiza ry.
        self.by = by
        # Actualiza by.
        self.count = count
        # Actualiza count.

    def start_populating(self):
        # Inicia la población de todos los caminos con sus coordenadas
        #1
        self.update_coordinates(60, 260, 540, 340, 5)
        # Actualiza coordenadas para el segmento 1.
        self.direct(pow_index=0, direction='right')
        # Calcula y añade el segmento 1, moviendo a la derecha.
        #2
        self.update_coordinates(260, 220, 340, 380, 5)
        # Actualiza coordenadas para el segmento 2.
        self.direct(pow_index=3, direction='up')
        # Calcula y añade el segmento 2, moviendo hacia arriba.
        #3
        self.update_coordinates(260, 20, 340, 580, 3)
        # Actualiza coordenadas para el segmento 3.
        self.direct(direction='right')
        # Calcula y añade el segmento 3, moviendo a la derecha.
        #4
        self.update_coordinates(340, 60, 260, 540, 5)
        # Actualiza coordenadas para el segmento 4.
        self.direct(pow_index=0, direction='down')
        # Calcula y añade el segmento 4, moviendo hacia abajo.
        #5
        self.update_coordinates(380, 260, 220, 340, 5)
        # Actualiza coordenadas para el segmento 5.
        self.direct(pow_index=3, direction='right')
        # Calcula y añade el segmento 5, moviendo a la derecha.
        #6
        self.update_coordinates(580, 260, 20, 340, 3)
        # Actualiza coordenadas para el segmento 6.
        self.direct(direction='down')
        # Calcula y añade el segmento 6, moviendo hacia abajo.
        #7
        self.update_coordinates(540, 340, 60, 260, 5)
        # Actualiza coordenadas para el segmento 7.
        self.direct(pow_index=0, direction='left')
        # Calcula y añade el segmento 7, moviendo a la izquierda.
        #8
        self.update_coordinates(340, 380, 260, 220, 5)
        # Actualiza coordenadas para el segmento 8.
        self.direct(pow_index=3, direction='down')
        # Calcula y añade el segmento 8, moviendo hacia abajo.
        #9
        self.update_coordinates(340, 580, 260, 20, 3)
        # Actualiza coordenadas para el segmento 9.
        self.direct(direction='left')
        # Calcula y añade el segmento 9, moviendo a la izquierda.
        #10
        self.update_coordinates(260, 540, 340, 60, 5)
        # Actualiza coordenadas para el segmento 10.
        self.direct(pow_index=0, direction='up')
        # Calcula y añade el segmento 10, moviendo hacia arriba.
        #11
        self.update_coordinates(220, 340, 380, 260, 6)
        # Actualiza coordenadas para el segmento 11.
        self.direct(pow_index=3, direction='left')
        # Calcula y añade el segmento 11, moviendo a la izquierda.
        #12
        self.update_coordinates(20, 300, 580, 300, 7)
        # Actualiza coordenadas para el segmento 12.
        self.direct(direction='right')
        # Calcula y añade el segmento 12, moviendo a la derecha.

    def direct_horizontal(self, k, pow_index = -1):
        # Calcula y añade puntos para movimientos horizontales.

        for i in range(self.count):
            # Itera 'count' veces para generar cada punto.
            if i == pow_index:
                # Comprueba si el índice actual es un punto especial (ej. seguro).
                p = 1
                # Si es un punto especial, 'p' es 1.
            else:
                # Si no es un punto especial.
                p = 0
                # 'p' es 0.
            self.green_path.append((self.gx + k*i*Board.SQUARE_SIZE, self.gy, p))
            # Añade el punto al camino verde.
            self.red_path.append((self.gy, self.ry - k*i*Board.SQUARE_SIZE, p))
            # Añade el punto al camino rojo.
            self.blue_path.append((self.ry - k*i*Board.SQUARE_SIZE, self.by, p))
            # Añade el punto al camino azul.
            self.yellow_path.append((self.by, self.gx + k*i*Board.SQUARE_SIZE, p))
            # Añade el punto al camino amarillo.

    def direct_vertical(self, k, pow_index = -1):
        # Calcula y añade puntos para movimientos verticales.

        for i in range(self.count):
            # Itera 'count' veces para generar cada punto.
            if i == pow_index:
                # Comprueba si el índice actual es un punto especial.
                p = 1
                # Si es un punto especial, 'p' es 1.
            else:
                # Si no es un punto especial.
                p = 0
                # 'p' es 0.
            self.green_path.append((self.gx, self.gy - k*i*Board.SQUARE_SIZE, p))
            # Añade el punto al camino verde.
            self.red_path.append((self.gy - k*i*Board.SQUARE_SIZE,self.ry, p))
            # Añade el punto al camino rojo.
            self.blue_path.append((self.ry, self.by + k*i*Board.SQUARE_SIZE, p))
            # Añade el punto al camino azul.
            self.yellow_path.append((self.by + k*i*Board.SQUARE_SIZE, self.gx, p))
            # Añade el punto al camino amarillo.

    def direct(self, direction, pow_index = -1):
        # Dirige la adición de puntos según la dirección especificada.

        if direction=='right':
            # Si la dirección es 'right'.
            self.direct_horizontal(1, pow_index=pow_index)
            # Llama a direct_horizontal con k=1 (hacia la derecha).
        elif direction=='left':
            # Si la dirección es 'left'.
            self.direct_horizontal(-1, pow_index=pow_index)
            # Llama a direct_horizontal con k=-1 (hacia la izquierda).
        elif direction=='down':
            # Si la dirección es 'down'.
            self.direct_vertical(-1, pow_index=pow_index)
            # Llama a direct_vertical con k=-1 (hacia abajo).
        else:
            # Si es cualquier otra dirección (asume 'up').
            self.direct_vertical(1, pow_index=pow_index)
            # Llama a direct_vertical con k=1 (hacia arriba).
path = Path()
# Crea una instancia de la clase Path.
path.start_populating()
# Llama al método para empezar a poblar los caminos.
