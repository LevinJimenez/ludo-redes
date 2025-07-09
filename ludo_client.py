import tkinter as tk
import tkinter.messagebox
from time import sleep
from random import choice
from PIL import ImageTk, Image
from settings import *
from board import *
import socket
import threading
import json
import ast
import time

# Definir una lista global para referencias de imagen
_image_refs = []

class LoginWindow:
    def __init__(self, master, on_success):
        self.root = master
        self.on_success = on_success
        self.top = tk.Toplevel(self.root)
        self.top.title('Login / Registro')
        self.top.geometry('350x250')
        self.frame = tk.Frame(self.top)
        self.frame.pack(pady=10)
        
        # Login
        tk.Label(self.frame, text='Usuario:').grid(row=0, column=0, sticky='e')
        self.login_entry = tk.Entry(self.frame)
        self.login_entry.grid(row=0, column=1)
        tk.Label(self.frame, text='Clave:').grid(row=1, column=0, sticky='e')
        self.clave_entry = tk.Entry(self.frame, show='*')
        self.clave_entry.grid(row=1, column=1)
        tk.Button(self.frame, text='Iniciar sesión', command=self.login).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Registro
        tk.Label(self.frame, text='--- Registro ---').grid(row=3, column=0, columnspan=2)
        tk.Label(self.frame, text='Nombre:').grid(row=4, column=0, sticky='e')
        self.nombre_entry = tk.Entry(self.frame)
        self.nombre_entry.grid(row=4, column=1)
        tk.Label(self.frame, text='Apellido:').grid(row=5, column=0, sticky='e')
        self.apellido_entry = tk.Entry(self.frame)
        self.apellido_entry.grid(row=5, column=1)
        tk.Label(self.frame, text='Usuario:').grid(row=6, column=0, sticky='e')
        self.reg_login_entry = tk.Entry(self.frame)
        self.reg_login_entry.grid(row=6, column=1)
        tk.Label(self.frame, text='Clave:').grid(row=7, column=0, sticky='e')
        self.reg_clave_entry = tk.Entry(self.frame, show='*')
        self.reg_clave_entry.grid(row=7, column=1)
        tk.Button(self.frame, text='Registrar', command=self.register).grid(row=8, column=0, columnspan=2, pady=5)
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def login(self):
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        login = self.login_entry.get().strip()
        clave = self.clave_entry.get().strip()
        if not login or not clave:
            tkinter.messagebox.showerror('Error', 'Ingrese usuario y clave')
            return
        msg = f'LOGIN:{login}:{clave}'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(256).decode('utf-8')
        if resp.startswith('OK:'):
            self.top.destroy()
            self.root.deiconify()
            self.on_success(login)
        else:
            tkinter.messagebox.showerror('Error', resp[6:] if resp.startswith('ERROR:') else resp)

    def register(self):
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        login = self.reg_login_entry.get().strip()
        clave = self.reg_clave_entry.get().strip()
        if not (nombre and apellido and login and clave):
            tkinter.messagebox.showerror('Error', 'Complete todos los campos de registro')
            return
        msg = f'REGISTER:{nombre}:{apellido}:{login}:{clave}'
        client_socket.send(msg.encode('utf-8'))
        resp = client_socket.recv(256).decode('utf-8')
        if resp.startswith('OK:'):
            tkinter.messagebox.showinfo('Registro', 'Usuario registrado correctamente. Ahora puede iniciar sesión.')
        else:
            tkinter.messagebox.showerror('Error', resp[6:] if resp.startswith('ERROR:') else resp)

    def on_close(self):
        self.root.destroy()

class Coin:
    def __init__(self, master, x, y, color, path_list, flag, idx):
        self.canvas = master
        self.curr_x = x
        self.curr_y = y
        self.home_x = x
        self.home_y = y
        self.color = color
        self.curr_index = -1
        self.coin = ImageTk.PhotoImage(Image.open('./assets/{}.png'.format(color)))
        self.img = self.canvas.create_image(x, y, anchor=tk.NW, image=self.coin)
        self.canvas.tag_bind(self.img, '<1>', self.moveCoin)
        self.disable = True
        self.path_list = path_list
        self.flag = flag
        self.idx = idx
        self.win = 0
        self.pad_x = 0

    def moveCoin(self, event):
        global client_socket, user_color, current_user, current_turn, players
        if user_color != self.color:
            tkinter.messagebox.showinfo('No permitido', 'Solo puedes mover tus propias fichas.')
            return
        if not (players and current_turn is not None and players[current_turn] == current_user):
            tkinter.messagebox.showinfo('No es tu turno', 'Debes esperar tu turno para mover.')
            return
        if not Dice.roll or len(Dice.roll) == 0:
            tkinter.messagebox.showinfo('Sin dado', 'Debes lanzar el dado antes de mover.')
            return
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return
        pasos = Dice.roll[0]
        ficha_idx = self.idx
        def task():
            if client_socket is None:
                tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
                return
            msg = f'MOVE:{self.color}:{ficha_idx}:{pasos}'
            client_socket.send(msg.encode('utf-8'))
            resp = client_socket.recv(2048).decode('utf-8')
            if resp.startswith('OK:'):
                root.after(0, Dice.clear_dice_label)
                get_game_state(force_update=True)
            else:
                root.after(0, lambda: tkinter.messagebox.showerror('Error', resp[6:] if resp.startswith('ERROR:') else resp))
        threading.Thread(target=task, daemon=True).start()

    def congratulations(self):
        Dice.update_state()
        Dice.set(self.flag - 1)
        return True

    def change_state(self, flag):
        if flag == self.flag:
            self.disable = False
        else:
            self.disable = True

    def is_at_home(self):
        return self.curr_x == self.home_x and self.curr_y == self.home_y

    def check_home(self):
        count = 0
        for goti in colors[self.flag]:
            if goti.is_at_home():
                count += 1
        return count

    def is_player_won(self):
        reached = 0
        for goti in colors[self.flag]:
            if goti.win:
                reached += 1
        return reached is 4

    def is_gameover(self):
        color_reached = 0
        for i in range(4):
            game = 0
            for color in colors[i]:
                if color.win:
                    game += 1
            if game is 4:
                color_reached += 1

        if color_reached is 3:
            tkinter.messagebox.showinfo('Game Over', '\n\n1. {}\n\n2. {}\n\n3. {}'.format(*position))
        else:
            return False
        return True

    def can_attack(self, idx):
        max_pad = 0
        count_a = 0
        x = self.path_list[idx][0]
        y = self.path_list[idx][1]
        for i in range(4):
            for j in range(4):
                if colors[i][j].curr_x == x and colors[i][j].curr_y == y:
                        if colors[i][j].pad_x > max_pad:
                            max_pad = colors[i][j].pad_x
                        count_a += 1

        if not self.path_list[idx][2]:
            for i in range(4):
                count = 0
                jdx = 0
                for j in range(4):
                    if (colors[i][j].curr_x == x and colors[i][j].curr_y == y 
                        and colors[i][j].color != self.color):
                        count += 1
                        jdx = j
                        
                if count is not 0 and count is not 2:
                    self.pad_x = max_pad + 4
                    return (True, i, jdx)

        if count_a is not 0:
            self.pad_x = max_pad + 4
        else:
            self.pad_x = 0
        return (False, 0, 0)

    def goto_home(self):
        self.canvas.coords(self.img, self.home_x, self.home_y)
        self.curr_x = self.home_x
        self.curr_y = self.home_y
        self.curr_index = -1

    def next_turn(self):
        if len(Dice.roll) == 0:
            Dice.set(self.flag)

    def set_playername(self, player):
        self.player = player

class Dice:
    chance = 0
    roll = []
    append_state = False
    dice_label_widget = None

    @classmethod
    def rolling(cls):
        if not (players and current_turn is not None and players[current_turn] == current_user):
            tkinter.messagebox.showinfo('No es tu turno', 'Debes esperar tu turno para lanzar el dado.')
            return
        if client_socket is None:
            tkinter.messagebox.showerror('Error', 'No hay conexión con el servidor.')
            return

        def task():
            # 1. Enviar la orden de tirar el dado
            msg = 'ROLL_DICE'
            client_socket.send(msg.encode('utf-8'))
            
            # 2. Pedir la actualización del estado del juego
            # El servidor responderá con el estado completo, que incluye el nuevo valor del dado.
            # La función get_game_state ya se encarga de recibir y procesar la respuesta.
            get_game_state(force_update=True)

        threading.Thread(target=task, daemon=True).start()

    @classmethod
    def update_dice_display(cls, dice_value):
        dice = {
            1: 'de1.png',
            2: 'de2.png',
            3: 'de3.png',
            4: 'de4.png',
            5: 'de5.png',
            6: 'de6.png',
        }.get(dice_value, None)

        if dice:
            img = ImageTk.PhotoImage(Image.open('./assets/{}'.format(dice)))
            image_label = tk.Label(ludo.get_frame(), width=60, height=60, image=img, bg=Color.CYAN)
            image_label.place(x=250, y=300)
            _image_refs.append(img)

            # Label del dado más pequeño
            if cls.dice_label_widget:
                cls.dice_label_widget.destroy()
            cls.dice_label_widget = tk.Label(ludo.get_frame(), text='{}'.format(' | '.join([str(x) for x in cls.roll])),
                                  font=('Arial', 12), width=10, height=1, borderwidth=3, relief=tk.RAISED)
            cls.dice_label_widget.place(x=260, y=250)

    @classmethod
    def start(cls):
        cls.rolling()

    @classmethod
    def update_panel(cls):
        root.update()
        sleep(0.5)
        Dice.set(cls.chance)
        cls.roll = []

    @classmethod
    def set(cls, flag):
        flag += 1
        cls.chance = flag
        if flag == 4:
            cls.chance = flag = 0
        if colors[cls.chance][0].is_player_won():
            Dice.set(cls.chance)
        else:
            for i in range(4):
                for j in range(4):
                    colors[i][j].change_state(flag)

            next_label = tk.Label(ludo.get_frame(), text='{} turn'.format(turn[flag]), font=('Arial', 20), width=30, height=3,
                            borderwidth=3, relief=tk.SUNKEN)
            next_label.place(x=100, y=100)

            roll_label = tk.Label(ludo.get_frame(), text='ROLL PLEASE', font=('Arial', 20), width=30, height=3, borderwidth=3, relief=tk.RAISED)
            roll_label.place(x=100, y=200)

            img = ImageTk.PhotoImage(Image.open('./assets/trans.png'))
            image_label = tk.Label(ludo.get_frame(), width=100, height=100, image=img, bg=Color.CYAN)
            image_label.place(x=250, y=300)

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