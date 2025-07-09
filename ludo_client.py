import tkinter as tk
# Importa la biblioteca principal de tkinter para crear la interfaz gráfica
# Se le asigna el alias 'tk' para facilitar su uso
import tkinter.messagebox
# Importa el módulo de ventanas de mensaje de tkinter
# Permite mostrar mensajes, alertas y diálogos al usuario
from time import sleep
# Importa la función sleep del módulo time
# Permite hacer pausas en la ejecución del programa
from random import choice
# Importa la función choice del módulo random
# Permite seleccionar un elemento aleatorio de una secuencia
from PIL import ImageTk, Image
# Importa las clases ImageTk e Image de la biblioteca Pillow (PIL)
# Permite el manejo y procesamiento de imágenes en la interfaz gráfica
from settings import *
# Importa todas las constantes y configuraciones definidas en el archivo settings.py
# El asterisco (*) indica que se importan todos los elementos públicos del módulo
from board import *
# Importa todas las clases y funciones definidas en el archivo board.py
# Probablemente contiene la definición del tablero de juego
import socket
# Importa el módulo socket para la comunicación en red
# Permite crear conexiones cliente-servidor
import threading
# Importa el módulo threading para manejar hilos
# Permite la ejecución concurrente de múltiples tareas
import json
# Importa el módulo json para el manejo de datos en formato JSON
# Permite codificar y decodificar datos estructurados
import ast
# Importa el módulo ast (Abstract Syntax Trees)
# Permite trabajar con árboles de sintaxis de Python
import time
# Importa el módulo time completo
# Proporciona funciones adicionales para el manejo del tiempo

# Definir una lista global para referencias de imagen
_image_refs = []

class LoginWindow:
    # Define una clase para la ventana de inicio de sesión y registro
    def __init__(self, master, on_success):
        # Constructor de la clase que recibe:
        # master: ventana principal de la aplicación
        # on_success: función callback que se ejecutará al lograr un inicio de sesión exitoso
        self.root = master
        # Almacena la referencia a la ventana principal
        self.on_success = on_success
        # Almacena la función callback para el inicio de sesión exitoso
        self.top = tk.Toplevel(self.root)
        # Crea una ventana secundaria (modal) sobre la ventana principal
        self.top.title('Login / Registro')
        # Establece el título de la ventana
        self.top.geometry('350x250')
        # Define el tamaño inicial de la ventana (ancho x alto)
        self.frame = tk.Frame(self.top)
        # Crea un marco para contener los elementos de la interfaz
        self.frame.pack(pady=10)
        # Coloca el marco en la ventana con un padding vertical de 10 píxeles

        # Sección de Login
        tk.Label(self.frame, text='Usuario:').grid(row=0, column=0, sticky='e')
        # Crea y posiciona la etiqueta "Usuario" alineada a la derecha
        self.login_entry = tk.Entry(self.frame)
        # Crea un campo de entrada para el usuario
        self.login_entry.grid(row=0, column=1)
        # Posiciona el campo de entrada del usuario
        tk.Label(self.frame, text='Clave:').grid(row=1, column=0, sticky='e')
        # Crea y posiciona la etiqueta "Clave" alineada a la derecha
        self.clave_entry = tk.Entry(self.frame, show='*')
        # Crea un campo de entrada para la clave, mostrando asteriscos
        self.clave_entry.grid(row=1, column=1)
        # Posiciona el campo de entrada de la clave
        tk.Button(self.frame, text='Iniciar sesión', command=self.login).grid(row=2, column=0, columnspan=2, pady=5)
        # Crea y posiciona el botón de inicio de sesión que llamará al método login
        
        # Sección de Registro
        tk.Label(self.frame, text='--- Registro ---').grid(row=3, column=0, columnspan=2)
        # Crea y posiciona un separador visual para la sección de registro
        tk.Label(self.frame, text='Nombre:').grid(row=4, column=0, sticky='e')
        # Crea y posiciona la etiqueta "Nombre" alineada a la derecha
        self.nombre_entry = tk.Entry(self.frame)
        # Crea un campo de entrada para el nombre
        self.nombre_entry.grid(row=4, column=1)
        # Posiciona el campo de entrada del nombre
        tk.Label(self.frame, text='Apellido:').grid(row=5, column=0, sticky='e')
        # Crea y posiciona la etiqueta "Apellido" alineada a la derecha
        self.apellido_entry = tk.Entry(self.frame)
        # Crea un campo de entrada para el apellido
        self.apellido_entry.grid(row=5, column=1)
        # Posiciona el campo de entrada del apellido
        tk.Label(self.frame, text='Usuario:').grid(row=6, column=0, sticky='e')
        # Crea y posiciona la etiqueta "Usuario" para registro
        self.reg_login_entry = tk.Entry(self.frame)
        # Crea un campo de entrada para el usuario en registro
        self.reg_login_entry.grid(row=6, column=1)
        # Posiciona el campo de entrada del usuario para registro
        tk.Label(self.frame, text='Clave:').grid(row=7, column=0, sticky='e')
        # Crea y posiciona la etiqueta "Clave" para registro
        self.reg_clave_entry = tk.Entry(self.frame, show='*')
        # Crea un campo de entrada para la clave en registro, mostrando asteriscos
        self.reg_clave_entry.grid(row=7, column=1)
        # Posiciona el campo de entrada de la clave para registro
        tk.Button(self.frame, text='Registrar', command=self.register).grid(row=8, column=0, columnspan=2, pady=5)
        # Crea y posiciona el botón de registro que llamará al método register
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        # Configura el comportamiento al cerrar la ventana, llamando al método on_close

    def login(self):
    # Método que maneja el proceso de inicio de sesión
        if client_socket is None:
            # Verifica si existe una conexión activa con el servidor
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            # Muestra un mensaje de error si no hay conexión
            return
            # Termina la ejecución del método
        login = self.login_entry.get().strip()
        # Obtiene el texto del campo de usuario y elimina espacios en blanco
        clave = self.clave_entry.get().strip()
        # Obtiene el texto del campo de contraseña y elimina espacios en blanco
        if not login or not clave:
            # Verifica si alguno de los campos está vacío
            tkinter.messagebox.showerror('Error', 'Ingrese usuario y clave')
            # Muestra un mensaje de error si falta algún campo
            return
            # Termina la ejecución del método
        msg = f'LOGIN:{login}:{clave}'
        # Construye el mensaje de login con formato "LOGIN:usuario:contraseña"
        client_socket.send(msg.encode('utf-8'))
        # Envía el mensaje codificado en UTF-8 al servidor
        resp = client_socket.recv(256).decode('utf-8')
        # Recibe la respuesta del servidor (máximo 256 bytes) y la decodifica
        if resp.startswith('OK:'):
            # Si la respuesta comienza con 'OK:' (login exitoso)
            self.top.destroy()
            # Cierra la ventana de login
            self.root.deiconify()
            # Muestra nuevamente la ventana principal
            self.on_success(login)
            # Ejecuta la función callback de éxito, pasando el usuario como parámetro
        else:
            # Si la respuesta no comienza con 'OK:' (login fallido)
            tkinter.messagebox.showerror('Error', 
                resp[6:] if resp.startswith('ERROR:') else resp)
            # Muestra un mensaje de error
            # Si la respuesta comienza con 'ERROR:', muestra el mensaje sin ese prefijo
            # Si no, muestra la respuesta completa

    def register(self):
    # Método que maneja el proceso de registro de nuevos usuarios
        if client_socket is None:
            # Verifica si existe una conexión activa con el servidor
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            # Muestra un mensaje de error si no hay conexión
            return
            # Termina la ejecución del método
        nombre = self.nombre_entry.get().strip()
        # Obtiene el texto del campo nombre y elimina espacios en blanco
        apellido = self.apellido_entry.get().strip()
        # Obtiene el texto del campo apellido y elimina espacios en blanco
        login = self.reg_login_entry.get().strip()
        # Obtiene el texto del campo usuario y elimina espacios en blanco
        clave = self.reg_clave_entry.get().strip()
        # Obtiene el texto del campo contraseña y elimina espacios en blanco
        if not (nombre and apellido and login and clave):
            # Verifica que todos los campos contengan datos
            # La expresión evalúa a False si algún campo está vacío
            tkinter.messagebox.showerror('Error', 'Complete todos los campos de registro')
            # Muestra un mensaje de error si falta algún campo
            return
            # Termina la ejecución del método
        msg = f'REGISTER:{nombre}:{apellido}:{login}:{clave}'
        # Construye el mensaje de registro con formato "REGISTER:nombre:apellido:usuario:contraseña"
        client_socket.send(msg.encode('utf-8'))
        # Envía el mensaje codificado en UTF-8 al servidor
        resp = client_socket.recv(256).decode('utf-8')
        # Recibe la respuesta del servidor (máximo 256 bytes) y la decodifica
        if resp.startswith('OK:'):
            # Si la respuesta comienza con 'OK:' (registro exitoso)
            tkinter.messagebox.showinfo('Registro', 
                'Usuario registrado correctamente. Ahora puede iniciar sesión.')
            # Muestra un mensaje de éxito indicando que puede proceder a iniciar sesión
        else:
            # Si la respuesta no comienza con 'OK:' (registro fallido)
            tkinter.messagebox.showerror('Error', 
                resp[6:] if resp.startswith('ERROR:') else resp)
            # Muestra un mensaje de error
            # Si la respuesta comienza con 'ERROR:', muestra el mensaje sin ese prefijo
            # Si no, muestra la respuesta completa

    def on_close(self):
        self.root.destroy() # Cierra completamente la ventana principal de la aplicación al cerrar el login

class Coin:
    # Define una clase para representar las fichas del juego
    def __init__(self, master, x, y, color, path_list, flag, idx):
        # Constructor de la clase que recibe:
        # master: referencia al canvas donde se dibujará la ficha
        # x, y: coordenadas iniciales de la ficha
        # color: color de la ficha
        # path_list: lista de posiciones que puede recorrer la ficha
        # flag: identificador del jugador
        # idx: índice de la ficha para el jugador
        self.canvas = master
        # Almacena la referencia al canvas donde se dibujará la ficha
        self.curr_x = x
        # Almacena la posición actual en X de la ficha
        self.curr_y = y
        # Almacena la posición actual en Y de la ficha
        self.home_x = x
        # Almacena la posición inicial en X de la ficha (su "casa")
        self.home_y = y
        # Almacena la posición inicial en Y de la ficha (su "casa")
        self.color = color
        # Almacena el color de la ficha
        self.curr_index = -1
        # Inicializa el índice actual en el camino como -1 (en casa)
        self.coin = ImageTk.PhotoImage(Image.open('./assets/{}.png'.format(color)))
        # Carga la imagen de la ficha desde el archivo correspondiente a su color
        # La convierte en un formato que tkinter puede mostrar
        self.img = self.canvas.create_image(x, y, anchor=tk.NW, image=self.coin)
        # Crea la imagen en el canvas en la posición especificada
        # anchor=tk.NW significa que el punto de anclaje es la esquina superior izquierda
        self.canvas.tag_bind(self.img, '<1>', self.moveCoin)
        # Vincula el evento de clic izquierdo sobre la ficha con el método moveCoin
        self.disable = True
        # Inicializa la ficha como deshabilitada (no se puede mover)
        self.path_list = path_list
        # Almacena la lista de posiciones que puede recorrer la ficha
        self.flag = flag
        # Almacena el identificador del jugador al que pertenece la ficha
        self.idx = idx
        # Almacena el índice de la ficha para el jugador (probablemente 0-3)
        self.win = 0
        # Inicializa el contador de victorias en 0
        self.pad_x = 0
        # Inicializa el padding en X en 0 (usado para ajustes de posición)

    def moveCoin(self, event):
    # Esta función se encarga de manejar el movimiento de una ficha (moneda) en el juego.
    # 'self' se refiere a la instancia del objeto al que pertenece este método (probablemente un objeto Coin).
    # 'event' es el objeto de evento que activó esta función (ej. un clic del ratón).
        global client_socket, user_color, current_user, current_turn, players
        # Se declaran las variables globales que se accederán y posiblemente se modificarán dentro de esta función.
        # - client_socket: La conexión de socket con el servidor del juego.
        # - user_color: El color de las fichas del usuario actual.
        # - current_user: El nombre de usuario del usuario actual.
        # - current_turn: El índice o identificador del jugador al que le toca mover.
        # - players: Una lista o diccionario que contiene información sobre todos los jugadores en el juego.
        if user_color != self.color:
            # Verifica si el color de la ficha que se intenta mover (self.color) es diferente del color del usuario actual (user_color).
            tkinter.messagebox.showinfo('No permitido', 'Solo puedes mover tus propias fichas.')
            # Si no coinciden, muestra un mensaje informativo al usuario indicando que solo puede mover sus propias fichas.
            return
            # Sale de la función, impidiendo cualquier ejecución posterior.
        if not (players and current_turn is not None and players[current_turn] == current_user):
            # Comprueba varias condiciones:
            # - 'players': Asegura que la lista/diccionario 'players' no esté vacío o sea None.
            # - 'current_turn is not None': Asegura que hay un turno activo.
            # - 'players[current_turn] == current_user': Verifica si es el turno del usuario actual.
            tkinter.messagebox.showinfo('No es tu turno', 'Debes esperar tu turno para mover.')
            # Si alguna de las condiciones anteriores es falsa (lo que significa que no es el turno del usuario o el estado del juego es inválido), muestra un mensaje.
            return
            # Sale de la función.
        if not Dice.roll or len(Dice.roll) == 0:
            # Verifica si la variable Dice.roll está vacía o es None.
            # Se espera que Dice.roll contenga el resultado de una tirada de dado.
            tkinter.messagebox.showinfo('Sin dado', 'Debes lanzar el dado antes de mover.')
            # Si el dado no ha sido lanzado o el resultado está vacío, informa al usuario que debe lanzar el dado primero.
            return
            # Sale de la función.
        if client_socket is None:
            # Verifica si la conexión client_socket no está establecida (es decir, es None).
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            # Si no hay conexión con el servidor, muestra un mensaje de error.
            return
            # Sale de la función.
        pasos = Dice.roll[0]
        # Obtiene el número de pasos para mover la ficha. Toma el primer (y probablemente único) elemento de la lista Dice.roll.
        ficha_idx = self.idx
        # Obtiene el índice de la ficha específica que se está moviendo. 'self.idx' es probablemente un atributo del objeto Coin.
        def task():
            # Define una función interna 'task' que se ejecutará en un hilo separado.
            # Esto se hace para evitar que la interfaz gráfica se congele mientras se esperan las respuestas del servidor.
            if client_socket is None:
                # Vuelve a verificar la conexión client_socket dentro del hilo, ya que el estado podría haber cambiado.
                tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
                # Si aún no hay conexión, muestra un error.
                return
                # Sale de la función task.
            msg = f'MOVE:{self.color}:{ficha_idx}:{pasos}'
            # Construye la cadena de mensaje para enviar al servidor.
            # Tiene el formato "MOVE:color_ficha:indice_ficha:pasos_a_mover".
            client_socket.send(msg.encode('utf-8'))
            # Codifica la cadena de mensaje a bytes usando codificación UTF-8 y la envía al servidor.
            resp = client_socket.recv(2048).decode('utf-8')
            # Recibe hasta 2048 bytes de respuesta del servidor y los decodifica de nuevo a una cadena de texto.
            if resp.startswith('OK:'):
                # Verifica si la respuesta del servidor comienza con 'OK:', lo que indica un movimiento exitoso.
                root.after(0, Dice.clear_dice_label)
                # Programa la ejecución de una función (Dice.clear_dice_label) en el hilo principal de Tkinter.
                # 'root.after(0, ...)' asegura que las actualizaciones de la GUI se realicen de forma segura en el hilo principal inmediatamente.
                get_game_state(force_update=True)
                # Llama a 'get_game_state' para actualizar el estado del juego desde el servidor, forzando una actualización.
            else:
                # Si la respuesta no comienza con 'OK:', indica un error.
                root.after(0, lambda: tkinter.messagebox.showerror('Error', resp[6:] if resp.startswith('ERROR:') else resp))
                # Programa que se muestre un mensaje de error en el hilo principal de Tkinter.
                # Extrae la parte del mensaje de error si la respuesta comienza con 'ERROR:', de lo contrario, muestra la respuesta completa.
        threading.Thread(target=task, daemon=True).start()
        # Crea un nuevo hilo, establece su función objetivo en 'task' y lo configura como un hilo demonio (termina cuando el programa principal termina).
        # Inicia el hilo, que ejecutará la función 'task' de forma concurrente.

    def congratulations(self):
    # Define un método llamado 'congratulations' que toma el parámetro 'self' (referencia a la instancia de la clase)
        Dice.update_state()
        # Llama al método estático 'update_state()' de la clase Dice para actualizar el estado actual
        Dice.set(self.flag - 1)
        # Llama al método estático 'set()' de la clase Dice, pasándole como argumento
        # el valor de self.flag menos 1. Esto probablemente actualiza algún estado interno
        # relacionado con los dados
        return True
        # Retorna True, indicando que la operación se completó exitosamente

    def change_state(self, flag):
    # Define un método llamado 'change_state' que acepta dos parámetros:
    # - self: referencia a la instancia de la clase
    # - flag: un parámetro que se compara con el flag almacenado en la instancia
        if flag == self.flag:
            # Compara si el parámetro 'flag' recibido es igual al valor de 'self.flag'
            # (el flag almacenado en la instancia)
            self.disable = False
            # Si los flags son iguales, establece el atributo 'disable' como False
        else:
            # Si los flags son diferentes
            self.disable = True
            # Establece el atributo 'disable' como True

    def is_at_home(self):
    # Define un método llamado 'is_at_home' que verifica si una ficha está en su posición inicial o "casa"
        return self.curr_x == self.home_x and self.curr_y == self.home_y
        # Retorna True si la posición actual (curr_x, curr_y) coincide con la posición de la casa (home_x, home_y)
        # Usa una comparación lógica AND que verifica ambas coordenadas simultáneamente

    def check_home(self):
        # Define un método llamado 'check_home' que cuenta cuántas fichas de un color están en su casa
        count = 0
        # Inicializa un contador en 0 para llevar la cuenta de las fichas en casa
        for goti in colors[self.flag]:
            # Itera sobre todas las fichas ('goti') del color actual
            # colors[self.flag] parece ser una lista de fichas de un color específico
            if goti.is_at_home():
                # Verifica si la ficha actual está en su posición de casa
                # utilizando el método is_at_home() definido anteriormente
                count += 1
                # Si la ficha está en casa, incrementa el contador
        return count
        # Retorna el número total de fichas que se encuentran en su posición de casa

    def is_player_won(self):
    # Define un método que verifica si un jugador ha ganado
    # (cuando todas sus fichas han llegado a la meta)
        reached = 0
        # Inicializa un contador para las fichas que han llegado a la meta
        for goti in colors[self.flag]:
            # Itera sobre todas las fichas ('goti') del color actual del jugador
            # colors[self.flag] contiene las fichas de un color específico
            if goti.win:
                # Verifica si la ficha actual ha llegado a la meta
                # win es un atributo booleano que indica si la ficha ha ganado
                reached += 1
                # Incrementa el contador por cada ficha que ha llegado
        return reached is 4
        # Retorna True si las 4 fichas del jugador han llegado a la meta

    def is_gameover(self):
        # Define un método que verifica si el juego ha terminado
        # (cuando 3 jugadores han completado todas sus fichas)
        color_reached = 0
        # Inicializa un contador para el número de colores/jugadores que han terminado
        for i in range(4):
            # Itera sobre los 4 colores/jugadores posibles
            game = 0
            # Inicializa un contador para las fichas ganadoras de cada color
            for color in colors[i]:
                # Itera sobre todas las fichas de un color específico
                if color.win:
                    # Verifica si la ficha ha llegado a la meta
                    game += 1
                    # Incrementa el contador de fichas ganadoras
            if game is 4:
                # Si todas las fichas (4) de un color han llegado
                color_reached += 1
                # Incrementa el contador de colores que han terminado
        if color_reached is 3:
            # Si 3 jugadores han completado todas sus fichas
            tkinter.messagebox.showinfo('Game Over', '\n\n1. {}\n\n2. {}\n\n3. {}'.format(*position))
            # Muestra un mensaje de "Game Over" con las posiciones finales
            # position debe ser una lista o tupla con las posiciones de los jugadores
        else:
            # Si aún no han terminado 3 jugadores
            return False
            # Retorna False indicando que el juego continúa
        return True
        # Retorna True indicando que el juego ha terminado

    def can_attack(self, idx):
    # Define un método que determina si una ficha puede atacar a otra en una posición específica
    # Recibe como parámetro idx que parece ser un índice de una posición en path_list
        max_pad = 0
        # Inicializa una variable para mantener el máximo desplazamiento (padding) de las fichas
        count_a = 0
        # Inicializa un contador para el número total de fichas en una posición
        x = self.path_list[idx][0]
        y = self.path_list[idx][1]
        # Obtiene las coordenadas x, y de la posición a verificar desde path_list
        for i in range(4):
            for j in range(4):
                # Itera sobre todas las fichas de todos los colores (4x4 = 16 fichas en total)
                if colors[i][j].curr_x == x and colors[i][j].curr_y == y:
                    # Verifica si hay alguna ficha en las coordenadas (x,y)
                    if colors[i][j].pad_x > max_pad:
                        # Si el padding de la ficha actual es mayor que el máximo registrado
                        max_pad = colors[i][j].pad_x
                        # Actualiza el máximo padding
                    count_a += 1
                    # Incrementa el contador de fichas en esa posición
        if not self.path_list[idx][2]:
            # Si la posición no es una casilla segura (path_list[idx][2] parece ser un indicador de casilla segura)
            for i in range(4):
                # Itera sobre cada color
                count = 0
                # Contador para fichas de un color específico en la posición
                jdx = 0
                # Índice para rastrear la ficha específica
                for j in range(4):
                    # Itera sobre cada ficha del color actual
                    if (colors[i][j].curr_x == x and colors[i][j].curr_y == y 
                        and colors[i][j].color != self.color):
                        # Verifica si hay una ficha de otro color en la misma posición
                        count += 1
                        jdx = j
                        # Incrementa el contador y guarda el índice de la ficha
                if count is not 0 and count is not 2:
                    # Si hay exactamente 1 ficha de otro color (no 0 ni 2)
                    self.pad_x = max_pad + 4
                    # Actualiza el padding de la ficha actual
                    return (True, i, jdx)
                    # Retorna que puede atacar, junto con el color (i) y el índice (jdx) de la ficha a atacar
        if count_a is not 0:
            # Si hay alguna ficha en la posición
            self.pad_x = max_pad + 4
            # Actualiza el padding para evitar superposición
        else:
            # Si no hay fichas en la posición
            self.pad_x = 0
            # Resetea el padding a 0
        return (False, 0, 0)
        # Retorna que no puede atacar, con valores por defecto para color e índice

    def goto_home(self):
    # Define un método llamado 'goto_home' que pertenece a una clase (indicado por 'self').
    # Este método se usa para mover una ficha o elemento visual a su posición inicial o "casa".
        self.canvas.coords(self.img, self.home_x, self.home_y)
        # Actualiza las coordenadas del objeto de imagen (self.img) en el lienzo (self.canvas).
        # self.img es probablemente el identificador de la imagen que representa la ficha en el lienzo Tkinter.
        # self.home_x y self.home_y son las coordenadas X e Y predefinidas de la posición "casa" a la que debe ir el objeto.
        self.curr_x = self.home_x
        # Actualiza la coordenada X actual del objeto (self.curr_x) a la coordenada X de la posición "casa".
        self.curr_y = self.home_y
        # Actualiza la coordenada Y actual del objeto (self.curr_y) a la coordenada Y de la posición "casa".
        self.curr_index = -1

    def next_turn(self):
    # Define un método llamado 'next_turn' (siguiente turno) que pertenece a una clase.
        if len(Dice.roll) == 0:
            # Comprueba si la lista 'Dice.roll' está vacía.
            # 'Dice.roll' se usa para almacenar los resultados de las tiradas de dado.
            # Si está vacía, significa que no se ha realizado una tirada de dado para el turno actual o la anterior tirada ya se procesó.
            Dice.set(self.flag)
            # Si 'Dice.roll' está vacía, llama a un método 'set' de la clase 'Dice'.
            # 'self.flag' es un valor o un indicador que se pasa a la clase 'Dice' para alguna configuración
            # relacionada con la tirada del dado para el próximo turno. Podría ser un indicador de qué jugador tiene el turno.

    def set_playername(self, player):
        # Define un método llamado 'set_playername' (establecer nombre de jugador) que pertenece a la misma clase.
        # Este método se usa para asignar un nombre de jugador al objeto actual.
        self.player = player
        # Asigna el valor del argumento 'player' (que es el nombre del jugador) al atributo 'player' de la instancia actual (self).
        # Esto establece el nombre del jugador asociado a este objeto.

class Dice:
    # Define una clase llamada 'Dice' (Dado). Esta clase probablemente se encarga de gestionar la lógica y el estado del dado en el juego.
    chance = 0
    # Define una variable de clase (o atributo de clase) llamada 'chance' y la inicializa en 0
    roll = []
    # Define una variable de clase 'roll' y la inicializa como una lista vacía.
    # Esta lista se utilizará para almacenar los resultados de las tiradas del dado.
    append_state = False
    # Define una variable de clase 'append_state' y la inicializa en 'False'.
    dice_label_widget = None
    # Define una variable de clase 'dice_label_widget' y la inicializa en 'None'.

    @classmethod
    def rolling(cls):
    # Decorador '@classmethod' indica que 'rolling' es un método de clase.
    # Puede ser llamado en la clase (ej. Dice.rolling()) y recibe la clase (cls) como primer argumento.
        if not (players and current_turn is not None and players[current_turn] == current_user):
            # Verifica si NO se cumplen todas estas condiciones:
            # 1. 'players' existe y no está vacío.
            # 2. 'current_turn' no es None (hay un turno activo).
            # 3. El jugador actual ('current_user') es el que le toca mover ('players[current_turn]').
            tkinter.messagebox.showinfo('No es tu turno', 'Debes esperar tu turno para lanzar el dado.')
            # Si no es el turno del jugador actual, muestra un mensaje de información.
            return
            # Sale de la función, impidiendo que se lance el dado.
        if client_socket is None:
            # Verifica si la variable global 'client_socket' es None, lo que significa que no hay conexión con el servidor.
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            # Si no hay conexión, muestra un mensaje de error.
            return
            # Sale de la función.

    def task():
        # Define una función anidada llamada 'task'. Esta función se ejecutará en un hilo separado
        # para no bloquear la interfaz de usuario mientras se espera la comunicación con el servidor.
        msg = 'ROLL_DICE'
        # Crea el mensaje a enviar al servidor, indicando que se quiere lanzar el dado.
        client_socket.send(msg.encode('utf-8'))
        # Codifica el mensaje a bytes usando UTF-8 y lo envía a través del socket al servidor.
        # 2. Pedir la actualización del estado del juego
        get_game_state(force_update=True)
        # Llama a la función global 'get_game_state'. 'force_update=True' sugiere que se debe solicitar
        # el estado del juego al servidor de nuevo para obtener el resultado del dado y la información actualizada.
    threading.Thread(target=task, daemon=True).start()
    # Crea un nuevo hilo ('threading.Thread').
    # 'target=task': Especifica que la función 'task' será ejecutada en este nuevo hilo.
    # 'daemon=True': Configura el hilo como un hilo "demonio", lo que significa que se cerrará automáticamente
    # cuando el programa principal termine, sin necesidad de esperar a que el hilo termine su ejecución.
    # '.start()': Inicia la ejecución del hilo.

@classmethod
def update_dice_display(cls, dice_value):
    # Decorador '@classmethod' indica que 'update_dice_display' es un método de clase.
    # Esta función se encarga de actualizar la representación visual del dado en la interfaz gráfica.
    dice = {
        1: 'de1.png',
        2: 'de2.png',
        3: 'de3.png',
        4: 'de4.png',
        5: 'de5.png',
        6: 'de6.png',
    }.get(dice_value, None)
    # Crea un diccionario que mapea los valores del dado (1 al 6) a los nombres de archivo de las imágenes correspondientes.
    # '.get(dice_value, None)' intenta obtener el nombre del archivo de imagen usando 'dice_value' como clave.
    # Si 'dice_value' no se encuentra (ej. es un valor no válido), retorna None.

    if dice:
        # Verifica si se encontró un nombre de archivo de imagen válido para el 'dice_value'.
        img = ImageTk.PhotoImage(Image.open('./assets/{}'.format(dice)))
        # Carga la imagen del dado desde el directorio './assets/' usando 'Image.open()' de Pillow.
        # Luego, la convierte a un formato compatible con Tkinter ('ImageTk.PhotoImage').
        image_label = tk.Label(ludo.get_frame(), width=60, height=60, image=img, bg=Color.CYAN)
        # Crea un nuevo widget Label de Tkinter para mostrar la imagen del dado.
        # 'ludo.get_frame()' obtiene el marco o contenedor donde se colocará el Label.
        # Se establecen el ancho, alto, la imagen y el color de fondo.
        image_label.place(x=250, y=300)
        # Posiciona el 'image_label' en las coordenadas (250, 300) dentro de su contenedor usando el gestor de geometría 'place'.
        _image_refs.append(img)
        # Añade la referencia a la imagen ('img') a una lista global '_image_refs'.
        # Esto es crucial en Tkinter para evitar que la imagen sea eliminada por el recolector de basura,
        # lo que resultaría en que la imagen no se muestre o desaparezca.

        # Label del dado más pequeño
        # Comentario que indica que la siguiente sección se refiere a un label de texto más pequeño.
        if cls.dice_label_widget:
            # Verifica si ya existe un widget de etiqueta de dado anterior (almacenado en 'cls.dice_label_widget').
            cls.dice_label_widget.destroy()
            # Si existe, lo destruye para limpiar la interfaz antes de crear uno nuevo.
        cls.dice_label_widget = tk.Label(ludo.get_frame(), text='{}'.format(' | '.join([str(x) for x in cls.roll])),
                                         font=('Arial', 12), width=10, height=1, borderwidth=3, relief=tk.RAISED)
        # Crea un nuevo widget Label de Tkinter para mostrar el valor numérico del dado (o dados).
        # El texto se genera uniendo los valores en 'cls.roll' con un separador ' | '.
        # Se configuran la fuente, el ancho, el alto, el borde y el estilo de relieve.
        cls.dice_label_widget.place(x=260, y=250)
        # Posiciona este nuevo 'dice_label_widget' en las coordenadas (260, 250).

    @classmethod
    def start(cls):
    # Este método inicia la acción de tirar el dado.
        cls.rolling()
    # Esto inicia el proceso de lanzar el dado, incluyendo las verificaciones de turno y la comunicación con el servidor.

    @classmethod
    def update_panel(cls):
        # Este método encarga de actualizar la interfaz gráfica y reiniciar el estado del dado.
        root.update()
        # Fuerza una actualización inmediata de la interfaz gráfica de Tkinter.
        sleep(0.5)
        # Pausa la ejecución del programa por 0.5 segundos (medio segundo).
        # para permitir que el usuario vea la última actualización de la GUI antes de que ocurran otros cambios,
        # o para sincronizar con animaciones/eventos.
        Dice.set(cls.chance)
        # Este método 'set' podría estar configurando el estado inicial del dado para la siguiente tirada,
        # relacionado con el número de intentos o el estado de "oportunidad".
        cls.roll = []
        # borra los resultados de las tiradas de dado anteriores, preparando la clase para una nueva tirada.

    @classmethod
    def set(cls, flag):
        # Este método gestionar el cambio de turno y la actualización de la interfaz gráfica.

        flag += 1
        # Incrementa el valor de 'flag' en 1. 'flag' probablemente representa el índice del jugador actual en alguna lista.

        cls.chance = flag
        # Asigna el nuevo valor de 'flag' a la variable de clase 'chance'

        if flag == 4:
            # Comprueba si 'flag' ha alcanzado el valor de 4.
            # si 'flag' llega a 4, se reinicia al primer jugador.
            cls.chance = flag = 0
            # Si 'flag' es 4, lo reinicia a 0, haciendo que el turno vuelva al primer jugador.
            # También actualiza 'cls.chance' a 0.

        if colors[cls.chance][0].is_player_won():
            # Accede a una estructura de datos global llamada 'colors'.
            # 'colors[cls.chance]' probablemente selecciona la lista de fichas (o datos) para el jugador actual.
            # '[0]' es la primera ficha de ese jugador o un objeto que representa al jugador.
            # '.is_player_won()' llama a un método para verificar si el jugador actual ha ganado el juego.
            Dice.set(cls.chance)
            # Si el jugador actual ha ganado, llama recursivamente a 'Dice.set' con el mismo 'cls.chance'.
            # Esto es para avanzar al siguiente jugador si el actual ya ganó o para manejar un estado de fin de juego.

        else:
            # Si el jugador actual NO ha ganado:
            for i in range(4):
                # Inicia un bucle que itera 4 veces (probablemente para cada uno de los 4 jugadores/colores).
                for j in range(4):
                    # Inicia un bucle anidado que itera 4 veces (probablemente para cada una de las 4 fichas de un jugador).
                    colors[i][j].change_state(flag)
                    # Llama al método 'change_state()' de cada ficha.
                    # 'colors[i][j]' accede a una ficha específica.
                    # 'flag' se pasa a 'change_state()', lo que podría indicar el nuevo estado de la ficha
                    # (ej., si es interactuable o no, basado en si es el turno de su color).

            next_label = tk.Label(ludo.get_frame(), text='{} turn'.format(turn[flag]), font=('Arial', 20), width=30, height=3,
                                borderwidth=3, relief=tk.SUNKEN)
            # Crea un nuevo widget Label de Tkinter para mostrar de quién es el próximo turno.
            # 'ludo.get_frame()' obtiene el marco principal.
            # El texto se forma con 'turn[flag]', donde 'turn' es una lista/diccionario que mapea el índice 'flag' al nombre del jugador/color.
            # Se configuran la fuente, el tamaño, el borde y el estilo de relieve (hundido).
            next_label.place(x=100, y=100)
            # Posiciona esta etiqueta en las coordenadas (100, 100) en el marco.

            roll_label = tk.Label(ludo.get_frame(), text='ROLL PLEASE', font=('Arial', 20), width=30, height=3, borderwidth=3, relief=tk.RAISED)
            # Crea un nuevo widget Label de Tkinter con el texto "ROLL PLEASE" (POR FAVOR, LANZA EL DADO).
            # Se configuran la fuente, el tamaño, el borde y el estilo de relieve (elevado).
            roll_label.place(x=100, y=200)
            # Posiciona esta etiqueta en las coordenadas (100, 200) en el marco.

            img = ImageTk.PhotoImage(Image.open('./assets/trans.png'))
            # Carga una imagen llamada 'trans.png' desde el directorio 'assets'.
            # 'trans.png' probablemente es una imagen transparente o un marcador de posición para borrar visualmente el dado anterior.
            # La convierte a un formato compatible con Tkinter.
            image_label = tk.Label(ludo.get_frame(), width=100, height=100, image=img, bg=Color.CYAN)
            # Crea un nuevo widget Label para mostrar esta imagen transparente.
            # Esto podría usarse para "ocultar" el resultado del dado anterior o limpiar visualmente el área del dado.
            image_label.place(x=250, y=300)
            # Posiciona esta etiqueta en las coordenadas (250, 300) en el marco.

    @classmethod
    def remove(cls):
        Dice.roll.pop(0)

    @classmethod
    def remove_by_index(cls, ex):
        del cls.roll[cls.roll.index(ex)]

    @classmethod
    def update_state(cls):
        cls.append_state = True

    @classmethod
    def check_move_possibility(cls):
        check_1 = 0
        check_2 = 0
        for goti in colors[cls.chance]:
            if goti.is_at_home():
                check_1 += 1
            else:
                max_moves = len(goti.path_list) - goti.curr_index - 1
                if max_moves < cls.roll[0]:
                    check_2 += 1

        if 6 not in cls.roll:
            if check_1 is 4 or check_1 + check_2 is 4:
                Dice.update_panel()
        else:
            if check_2 is 4:
                Dice.update_panel()

    @classmethod
    def clear_dice_label(cls):
        if cls.dice_label_widget:
            cls.dice_label_widget.destroy()
            cls.dice_label_widget = None
        cls.roll = []

# --- Hilo de actualización periódica del estado ---
def actualizar_periodicamente_estado():
    def loop():
        while True:
            get_game_state(force_update=True)
            time.sleep(0.5)
    threading.Thread(target=loop, daemon=True).start()

def align(x, y, color, path_list, flag):
    container = []
    idx = 0
    for i in range(2):
        test = Coin(ludo.get_canvas(), x, y + i*2*Board.SQUARE_SIZE, color=color, path_list=path_list, flag=flag, idx=idx)
        container.append(test)
        idx += 1
    for i in range(2):
        test = Coin(ludo.get_canvas(), x + 2*Board.SQUARE_SIZE, y + i*2*Board.SQUARE_SIZE, color=color, path_list=path_list, flag=flag, idx=idx)
        container.append(test)
        idx += 1
    return container

def startgame():
    # Unirse a la partida en el servidor
    def task():
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        msg = f'JOIN_GAME:{current_user}'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(256).decode('utf-8')
        root.after(0, lambda: tkinter.messagebox.showinfo('Info', resp))
    
    threading.Thread(target=task, daemon=True).start()
    
    # Configurar nombres de jugadores
    for i in range(4):
        if players[i].get():
            turn[i] = players[i].get()
    for i in range(4):
        for j in range(4):
            colors[i][j].set_playername(turn[i])

    start_label = tk.Label(ludo.get_frame(), text='! START ! Let\'s Begin with {}'.format(turn[0]), font=('Arial', 20),
                         width=30, height=3, borderwidth=3, relief=tk.SUNKEN)
    start_label.place(x=100, y=100)
    root.destroy()

def create_enterpage():
    enter_label = tk.Label(root, text='Enter Your Nickname!', font=('Arial', 20), width=30, height=3,
                            borderwidth=3, relief=tk.RAISED)
    enter_label.place(x=20, y=20)

    enter_button = tk.Button(root, text='Enter', command=startgame, width=15, height=2)
    enter_button.place(x=230, y=500)

    for i in range(2):
        temp = tk.Entry(root, width=15)
        temp.place(x=87, y=220 + i*180)
        players.append(temp)

    for i in range(2):
        temp = tk.Entry(root, width=15)
        temp.place(x=387, y=400 - i*180)
        players.append(temp)

    global greenimg, redimg, blueimg, yellowimg

    greenimg = ImageTk.PhotoImage(Image.open('./assets/green2.png'))
    green_label = tk.Label(root, image=greenimg)
    green_label.place(x=107, y=130)

    redimg = ImageTk.PhotoImage(Image.open('./assets/red2.png'))
    red_label = tk.Label(root, image=redimg)
    red_label.place(x=107, y=310)

    blueimg = ImageTk.PhotoImage(Image.open('./assets/blue2.png'))
    blue_label = tk.Label(root, image=blueimg)
    blue_label.place(x=407, y=310)

    yellowimg = ImageTk.PhotoImage(Image.open('./assets/yellow2.png'))
    yellow_label = tk.Label(root, image=yellowimg)
    yellow_label.place(x=407, y=130)

def on_closing():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit the game? If you want to continue the game, press Enter in the Nickname window"):
        root.destroy()

def on_closingroot():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit the game?"):
        root.destroy()

# Variables globales
players = []
current_user = None
client_socket = None
user_color = None
current_turn = None

# Inicializar conexión al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remote_ip = '192.168.1.160'
remote_port = 10319
client_socket.connect((remote_ip, remote_port))

# Crear ventana principal
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('{}x{}'.format(width, height))
root.title('Ludo Online')
root.withdraw()  # Ocultar hasta login exitoso

ludo = LudoBoard(root)
ludo.create()

turn = ['Green', 'Red', 'Blue', 'Yellow']
position = []
colors = []

# Inicializar fichas
colors.append(align(2.1*Board.SQUARE_SIZE, 2.1*Board.SQUARE_SIZE, color='green', path_list=path.green_path, flag=0))
colors.append(align(2.1*Board.SQUARE_SIZE, 11.1*Board.SQUARE_SIZE, color='red', path_list=path.red_path, flag=1))
colors.append(align(11.1*Board.SQUARE_SIZE, 11.1*Board.SQUARE_SIZE, color='blue', path_list=path.blue_path, flag=2))
colors.append(align(11.1*Board.SQUARE_SIZE, 2.1*Board.SQUARE_SIZE, color='yellow', path_list=path.yellow_path, flag=3))

for i in range(4):
    for j in range(4):
        colors[i][j].change_state(0)

# Botón ROLL modificado para usar red
button = tk.Button(ludo.get_frame(), text='ROLL', command=Dice.start, width=20, height=2)
button.place(x=210, y=470)

def start_gui(username):
    global current_user, user_color
    current_user = username
    
    # Unirse automáticamente a la partida y obtener color asignado
    def join_task():
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        msg = f'JOIN_GAME:{current_user}'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(256).decode('utf-8')
        color = None
        if resp.startswith('OK:') and 'Color asignado:' in resp:
            color = resp.split('Color asignado:')[1].strip()
        if color:
            global user_color
            user_color = color
        root.after(0, lambda: show_status_message(resp))
        root.after(0, create_control_panel)
        root.after(0, get_game_state)
    
    threading.Thread(target=join_task, daemon=True).start()

    # Al final de start_gui (después de crear el panel de control y unirse a la partida), iniciar la actualización periódica:
    root.after(0, actualizar_periodicamente_estado)

def create_control_panel():
    # Panel de control en la parte superior
    control_frame = tk.Frame(ludo.get_frame())
    control_frame.place(x=50, y=50)
    
    # Información del usuario
    user_label = tk.Label(control_frame, text=f'Usuario: {current_user}', font=('Arial', 12, 'bold'))
    user_label.pack()
    color_label = tk.Label(control_frame, text=f'Tu color: {user_color}', font=('Arial', 12, 'bold'))
    color_label.pack()
    
    # Botones de control
    join_button = tk.Button(control_frame, text='Unirse a partida', command=join_game, width=15)
    join_button.pack(pady=2)
    
    start_button = tk.Button(control_frame, text='Iniciar partida', command=start_game, width=15)
    start_button.pack(pady=2)
    
    status_button = tk.Button(control_frame, text='Consultar estado', command=get_game_state, width=15)
    status_button.pack(pady=2)
    
    # Área de información
    info_frame = tk.Frame(ludo.get_frame())
    info_frame.place(x=50, y=200)
    
    global status_label, players_label, roll_button
    status_label = tk.Label(info_frame, text='Estado: Esperando conexión...', font=('Arial', 10))
    status_label.pack()
    
    players_label = tk.Label(info_frame, text='Jugadores: Ninguno', font=('Arial', 10))
    players_label.pack()
    
    # Botón ROLL modificado para usar red y control de turno
    roll_button = tk.Button(ludo.get_frame(), text='ROLL', command=Dice.start, width=20, height=2)
    roll_button.place(x=210, y=470)
    roll_button.config(state='disabled')

def update_buttons_state():
    # Solo habilitar y colorear ROLL si es el turno del usuario
    if current_turn is not None and user_color is not None and current_user is not None and players:
        if players[current_turn] == current_user:
            # Es el turno del jugador
            roll_button.config(state='normal', bg='#90EE90')  # Habilitado y color verde suave
        else:
            # No es el turno del jugador
            roll_button.config(state='disabled', bg='#F0F0F0') # Deshabilitado y color gris (default)
    else:
        # El juego no ha comenzado o los datos no están listos
        roll_button.config(state='disabled', bg='#F0F0F0') # Deshabilitado y color gris (default)


def join_game():
    def task():
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        msg = f'JOIN_GAME:{current_user}'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(256).decode('utf-8')
        root.after(0, lambda: show_status_message(resp))
    
    threading.Thread(target=task, daemon=True).start()

def start_game():
    def task():
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        msg = 'START_GAME'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(256).decode('utf-8')
        root.after(0, lambda: show_status_message(resp))
    
    threading.Thread(target=task, daemon=True).start()

def get_game_state(force_update=False):
    def task():
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        msg = 'GET_STATE'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(2048).decode('utf-8')
        if resp.startswith('OK:'):
            try:
                state_str = resp[3:]
                state = ast.literal_eval(state_str)
                root.after(0, lambda: update_status_display(state))
                root.after(0, lambda: actualizar_tablero_desde_estado(state))
            except Exception as e:
                root.after(0, lambda: show_status_message(f'Error al procesar estado: {e}'))
        else:
            root.after(0, lambda: show_status_message(resp))
    threading.Thread(target=task, daemon=True).start()

def show_status_message(message):
    status_label.config(text=f'Estado: {message}')

def update_status_display(state):
    global players, current_turn
    players = state.get('players', [])
    current_turn = state.get('turn', None)
    players_text = f'Jugadores: {", ".join(players)}'
    players_label.config(text=players_text)
    
    game_state = state.get('state', 'unknown')
    status_text = f'Estado: {game_state}'
    
    if game_state == 'running':
        status_text += f' - Turno: {players[current_turn] if current_turn is not None and current_turn < len(players) else "N/A"}'
        
        dice_val = state.get('dice')
        if dice_val:
            status_text += f' - Dado: {dice_val}'
            Dice.roll = [dice_val]  # <-- LÍNEA AÑADIDA: Actualiza la variable del dado.
            Dice.update_dice_display(dice_val) # <-- LÍNEA AÑADIDA: Actualiza la imagen del dado.

    status_label.config(text=status_text)
    update_buttons_state()

# Iniciar ventana de login
login_win = LoginWindow(root, start_gui)

# --- Nueva función para actualizar el tablero desde el estado del servidor ---
def actualizar_tablero_desde_estado(state):
    # state['positions'] es un dict: {color: [posiciones de fichas]}
    # 1. Construir un mapa de (x, y) -> lista de (color_idx, idx) para saber cuántas fichas hay en cada casilla
    pos_map = {}
    for color, fichas in state.get('positions', {}).items():
        color_idx = {'green': 0, 'red': 1, 'blue': 2, 'yellow': 3}[color]
        for idx, pos in enumerate(fichas):
            goti = colors[color_idx][idx]
            if pos == 0:
                key = (goti.home_x, goti.home_y)
            elif pos < len(goti.path_list):
                key = (goti.path_list[pos][0], goti.path_list[pos][1])
            else:
                continue
            if key not in pos_map:
                pos_map[key] = []
            pos_map[key].append((color_idx, idx))
    # 2. Posicionar cada ficha con offset si hay más de una en la misma casilla
    for key, fichas in pos_map.items():
        n = len(fichas)
        for i, (color_idx, idx) in enumerate(fichas):
            goti = colors[color_idx][idx]
            x, y = key
            offset = 0
            if n == 2:
                offset = [-6, 6][i]
            elif n == 3:
                offset = [-8, 0, 8][i]
            elif n >= 4:
                offset = [-10, -3, 3, 10][i] if i < 4 else 0
            else:
                offset = 0
            goti.curr_x = x
            goti.curr_y = y
            goti.canvas.coords(goti.img, x + 4 + offset, y + 4 + offset)
            goti.curr_index = -1 if (x, y) == (goti.home_x, goti.home_y) else pos

root.mainloop() 