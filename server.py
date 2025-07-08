import socket
from _thread import *
import sys
import threading
import json
import random
import datetime
import tkinter as tk

class UserManager:
    def __init__(self, filename='users.json'):
        self.filename = filename
        try:
            with open(self.filename, 'r') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f)

    def register(self, nombre, apellido, login, clave):
        if login in self.users:
            return False, 'Usuario ya existe'
        self.users[login] = {
            'nombre': nombre,
            'apellido': apellido,
            'clave': clave
        }
        self.save()
        return True, 'Usuario registrado'

    def delete(self, login):
        if login not in self.users:
            return False, 'Usuario no existe'
        del self.users[login]
        self.save()
        return True, 'Usuario borrado'

    def validate(self, login, clave):
        if login not in self.users:
            return False, 'Usuario no existe'
        if self.users[login]['clave'] != clave:
            return False, 'Clave incorrecta'
        return True, 'Login exitoso'

class GameManager:
    def __init__(self):
        self.players = []  # lista de usuarios conectados
        self.turn = 0
        self.dice = None
        self.state = 'waiting'  # waiting, running, stopped
        self.positions = {}  # {color: [posiciones de fichas]}
        self.colors = ['green', 'red', 'blue', 'yellow']
        self.user_colors = {}  # usuario -> color
        self.dice_pending = False  # True si el dado está pendiente de usar
        self.init_positions()

    def init_positions(self):
        self.positions = {color: [0, 0, 0, 0] for color in self.colors}

    def add_player(self, username):
        if username in self.user_colors:
            return True  # Ya unido
        if len(self.players) < 4:
            self.players.append(username)
            # Asignar color disponible
            assigned_colors = set(self.user_colors.values())
            for color in self.colors:
                if color not in assigned_colors:
                    self.user_colors[username] = color
                    break
            return True
        return False

    def get_player_color(self, username):
        return self.user_colors.get(username)

    def start_game(self):
        if len(self.players) >= 2:
            self.state = 'running'
            self.turn = 0
            self.dice = None
            self.dice_pending = False
            self.init_positions()
            return True, 'Partida iniciada'
        return False, 'Se requieren al menos 2 jugadores'

    def stop_game(self):
        self.state = 'stopped'
        return True, 'Partida detenida'

    def roll_dice(self, username):
        if self.state != 'running':
            return False, 'La partida no está en curso'
        current_player = self.players[self.turn]
        if username != current_player:
            return False, 'No es tu turno'
        if self.dice_pending:
            return False, 'Debes usar el dado actual antes de lanzar de nuevo'
        self.dice = random.randint(1, 6)
        self.dice_pending = True
        # Si no hay movimientos posibles, saltar turno automáticamente
        color = self.user_colors[username]
        if not self.can_move_any(color, self.dice):
            if self.dice != 6:
                self.advance_turn()
                self.dice = None
                self.dice_pending = False
                return False, 'No puedes mover ninguna ficha, turno saltado'
        return True, self.dice

    def can_move_any(self, color, dice_value):
        # Si hay fichas en casa y el dado es 6, se puede sacar ficha
        if any(pos == 0 for pos in self.positions[color]) and dice_value == 6:
            return True
        # Si hay fichas en juego que pueden avanzar
        for idx, pos in enumerate(self.positions[color]):
            if pos > 0 and pos + dice_value < 57:  # 57 es la meta
                return True
        return False

    def move_piece(self, username, color, idx, steps):
        if self.state != 'running':
            return False, 'La partida no está en curso'
        current_player = self.players[self.turn]
        player_color = self.user_colors.get(username)
        if username != current_player or color != player_color:
            return False, 'Solo puedes mover tus fichas en tu turno'
        if not self.dice_pending or self.dice is None:
            return False, 'Debes lanzar el dado antes de mover'
        if color not in self.positions or idx < 0 or idx > 3:
            return False, 'Movimiento inválido'
        pos = self.positions[color][idx]
        from settings import path
        color_path = getattr(path, f'{color}_path')
        # Si la ficha está en casa
        if pos == 0:
            if self.dice == 6:
                self.positions[color][idx] = 1  # Sale de casa
                self.dice_pending = False
                self.dice = None
                return True, self.positions[color]
            else:
                return False, 'Solo puedes sacar ficha con un 6'
        # Si la ficha está afuera
        if pos > 0:
            if pos + self.dice < 57:
                new_pos = pos + self.dice
                # Obtener la posición absoluta (x, y) de la ficha movida
                if new_pos < len(color_path):
                    new_x, new_y, _ = color_path[new_pos]
                else:
                    new_x, new_y = None, None
                # Lógica de comer fichas enemigas (excepto en zona segura)
                if not self.is_safe_square(new_pos, color):
                    for other_color in self.colors:
                        if other_color == color:
                            continue
                        other_path = getattr(path, f'{other_color}_path')
                        for j in range(4):
                            other_pos = self.positions[other_color][j]
                            if other_pos > 0 and other_pos < len(other_path):
                                ox, oy, _ = other_path[other_pos]
                                # Comparar posición absoluta
                                if new_x == ox and new_y == oy:
                                    self.positions[other_color][j] = 0  # Enviar a casa
                self.positions[color][idx] = new_pos
                self.dice_pending = False
                if self.dice == 6:
                    self.dice = None
                    return True, self.positions[color]
                self.advance_turn()
                self.dice = None
                return True, self.positions[color]
            else:
                return False, 'Movimiento fuera de rango'
        return False, 'Movimiento inválido'

    def is_safe_square(self, pos, color):
        # Las zonas seguras son las posiciones del path donde el tercer valor de la tupla es True
        # Usar el path correspondiente al color
        from settings import path
        color_path = getattr(path, f'{color}_path')
        if pos < len(color_path):
            return color_path[pos][2]  # True si es seguro
        return False

    def advance_turn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def get_state(self):
        return {
            'players': self.players,
            'turn': self.turn,
            'dice': self.dice,
            'state': self.state,
            'positions': self.positions,
            'user_colors': self.user_colors,
            'dice_pending': self.dice_pending
        }

class ChatServer:

    clients_list = []

    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.user_manager = UserManager()
        self.game_manager = GameManager()
        self.create_listening_server()

    def create_listening_server(self):

        # create a socket using TCP port and ipv4
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = '0.0.0.0'  # Escuchar en todas las interfaces de red
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        # listen for incomming connections / max 4 clients
        self.server_socket.listen(4)
        self.receive_messages_in_a_new_thread()
    
   
    def receive_messages(self, so):   # function to receive new msgs
        username = None
        while True:
            incoming_buffer = so.recv(256)  # initialize the buffer
            if not incoming_buffer:
                break
            msg = incoming_buffer.decode('utf-8')
            if msg.startswith('REGISTER:'):
                _, nombre, apellido, login, clave = msg.strip().split(':', 4)
                ok, info = self.user_manager.register(nombre, apellido, login, clave)
                so.sendall(('OK:' + info if ok else 'ERROR:' + info).encode('utf-8'))
            elif msg.startswith('LOGIN:'):
                _, login, clave = msg.strip().split(':', 2)
                ok, info = self.user_manager.validate(login, clave)
                if ok:
                    username = login
                so.sendall(('OK:' + info if ok else 'ERROR:' + info).encode('utf-8'))
            elif msg.startswith('DELETE:'):
                _, login = msg.strip().split(':', 1)
                ok, info = self.user_manager.delete(login)
                so.sendall(('OK:' + info if ok else 'ERROR:' + info).encode('utf-8'))
            elif msg.startswith('JOIN_GAME:'):
                _, username = msg.strip().split(':', 1)
                ok = self.game_manager.add_player(username)
                color = self.game_manager.get_player_color(username)
                # Obtener IP del socket
                try:
                    ip = so.getpeername()[0]
                except Exception:
                    ip = 'desconocida'
                hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if ok and color:
                    log_msg = f"[{hora}] Jugador unido: {username} (Color: {color}, IP: {ip})"
                    print(log_msg)
                    server_gui.add_entry(log_msg)
                    so.sendall(f'OK:Jugador {username} unido a la partida. Color asignado: {color}'.encode('utf-8'))
                else:
                    so.sendall(f'ERROR:No se pudo unir a la partida (¿ya está lleno o ya unido?)'.encode('utf-8'))
            elif msg.startswith('START_GAME'):
                ok, info = self.game_manager.start_game()
                so.sendall(('OK:' + info if ok else 'ERROR:' + info).encode('utf-8'))
            elif msg.startswith('STOP_GAME'):
                ok, info = self.game_manager.stop_game()
                so.sendall(('OK:' + info if ok else 'ERROR:' + info).encode('utf-8'))
            elif msg.startswith('ROLL_DICE'):
                if username is None:
                    so.sendall('ERROR:No autenticado'.encode('utf-8'))
                else:
                    ok, result = self.game_manager.roll_dice(username)
                    so.sendall(('OK:' + str(result) if ok else 'ERROR:' + str(result)).encode('utf-8'))
            elif msg.startswith('MOVE:'):
                if username is None:
                    so.sendall('ERROR:No autenticado'.encode('utf-8'))
                else:
                    _, color, idx, steps = msg.strip().split(':', 3)
                    ok, result = self.game_manager.move_piece(username, color, int(idx), int(steps))
                    so.sendall(('OK:' + str(result) if ok else 'ERROR:' + str(result)).encode('utf-8'))
            elif msg.startswith('GET_STATE'):
                state = self.game_manager.get_state()
                so.sendall(('OK:' + str(state)).encode('utf-8'))
            else:
                self.last_received_message = msg
                self.broadcast_to_all_clients(so)  # send to all clients
        so.close()
    # broadcast the message to all clients

    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list((so, (ip, port)))
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()
    # add a new client

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)

# Ventana gráfica para mostrar conexiones
class ServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Conexiones al Servidor Ludo')
        self.text = tk.Text(self.root, width=70, height=20, state='disabled', font=('Consolas', 10))
        self.text.pack(padx=10, pady=10)
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        # La línea que iniciaba el hilo ha sido eliminada.

    def add_entry(self, msg):
        self.text.config(state='normal')
        self.text.insert('end', msg + '\n')
        self.text.see('end')
        self.text.config(state='disabled')

    def on_close(self):
        self.root.destroy()

# Instancia global de la GUI del servidor
server_gui = ServerGUI()

if __name__ == "__main__":
    # Iniciar el servidor en un hilo secundario
    def start_server():
        ChatServer()
    import threading
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    # Lanzar la ventana gráfica en el hilo principal
    server_gui.root.mainloop()
