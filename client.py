# Tkinter Python Module for GUI
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox, Toplevel
import socket  # Sockets for network connection
import threading  # for multiple proccess


class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master, client_socket=None):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        if client_socket:
            self.client_socket = client_socket
        else:
            self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        # initialazing socket with TCP and IPv4
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '127.0.0.1'  # IP address
        remote_port = 10319  # TCP port
        # connect to the remote server
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):  # GUI initializer
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()
        self.display_game_buttons()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(
            self.client_socket,))  # Create a thread for the send and receive in same time
        thread.start()
    # function to recieve msg

    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')

            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                if self.chat_transcript_area:
                    self.chat_transcript_area.insert('end', message + '\n')
                    self.chat_transcript_area.yview(END)
            else:
                if self.chat_transcript_area:
                    self.chat_transcript_area.insert('end', message + '\n')
                    self.chat_transcript_area.yview(END)

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter your name:', font=(
            "Helvetica", 16)).pack(side='left', padx=10)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
        self.join_button = Button(
            frame, text="Join", width=10, command=self.on_join).pack(side='left')
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box:', font=(
            "Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(
            frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(
            frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=(
            "Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(
            frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def display_game_buttons(self):
        frame = Frame()
        # Unirse a partida
        Button(frame, text="Unirse a partida", command=self.join_game).pack(side='left', padx=2)
        # Iniciar partida
        Button(frame, text="Iniciar partida", command=self.start_game).pack(side='left', padx=2)
        # Lanzar dado
        Button(frame, text="Lanzar dado", command=self.roll_dice).pack(side='left', padx=2)
        # Mover ficha
        Label(frame, text="Color:").pack(side='left')
        self.move_color = Entry(frame, width=6)
        self.move_color.pack(side='left')
        Label(frame, text="Ficha:").pack(side='left')
        self.move_idx = Entry(frame, width=3)
        self.move_idx.pack(side='left')
        Label(frame, text="Pasos:").pack(side='left')
        self.move_steps = Entry(frame, width=3)
        self.move_steps.pack(side='left')
        Button(frame, text="Mover", command=self.move_piece).pack(side='left', padx=2)
        # Consultar estado
        Button(frame, text="Estado", command=self.get_state).pack(side='left', padx=2)
        frame.pack(side='top', pady=5)

    def on_join(self):
        if not self.name_widget or len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your name", "Enter your name to send a message")
            return
        self.name_widget.config(state='disabled')
        if self.client_socket:
            self.client_socket.send(
                ("joined:" + self.name_widget.get()).encode('utf-8'))

    def on_enter_key_pressed(self, event):
        if not self.name_widget or len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your name", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        if self.enter_text_widget:
            self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        if not self.name_widget:
            return 'break'
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip() if self.enter_text_widget else ''
        message = (senders_name + data).encode('utf-8')
        if self.chat_transcript_area:
            self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
            self.chat_transcript_area.yview(END)
        if self.client_socket:
            self.client_socket.send(message)
        if self.enter_text_widget:
            self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def join_game(self):
        def task():
            if not self.name_widget or not self.name_widget.get():
                self.append_chat('Debes ingresar tu nombre antes de unirte a la partida.')
                return
            msg = f'JOIN_GAME:{self.name_widget.get()}'
            if self.client_socket:
                self.client_socket.send(msg.encode('utf-8'))
                resp = self.client_socket.recv(256).decode('utf-8')
                self.root.after(0, lambda: self.append_chat(f'Servidor: {resp}'))
        threading.Thread(target=task, daemon=True).start()

    def start_game(self):
        def task():
            msg = 'START_GAME'
            if self.client_socket:
                self.client_socket.send(msg.encode('utf-8'))
                resp = self.client_socket.recv(256).decode('utf-8')
                self.root.after(0, lambda: self.append_chat(f'Servidor: {resp}'))
        threading.Thread(target=task, daemon=True).start()

    def roll_dice(self):
        def task():
            msg = 'ROLL_DICE'
            if self.client_socket:
                self.client_socket.send(msg.encode('utf-8'))
                resp = self.client_socket.recv(256).decode('utf-8')
                self.root.after(0, lambda: self.append_chat(f'Servidor: {resp}'))
        threading.Thread(target=task, daemon=True).start()

    def move_piece(self):
        def task():
            color = self.move_color.get().strip().lower()
            idx = self.move_idx.get().strip()
            steps = self.move_steps.get().strip()
            if not (color and idx and steps):
                self.root.after(0, lambda: self.append_chat('Completa color, ficha y pasos para mover.'))
                return
            msg = f'MOVE:{color}:{idx}:{steps}'
            if self.client_socket:
                self.client_socket.send(msg.encode('utf-8'))
                resp = self.client_socket.recv(256).decode('utf-8')
                self.root.after(0, lambda: self.append_chat(f'Servidor: {resp}'))
        threading.Thread(target=task, daemon=True).start()

    def get_state(self):
        def task():
            msg = 'GET_STATE'
            if self.client_socket:
                self.client_socket.send(msg.encode('utf-8'))
                resp = self.client_socket.recv(2048).decode('utf-8')
                self.root.after(0, lambda: self.append_chat(f'Servidor: {resp}'))
        threading.Thread(target=task, daemon=True).start()

    def append_chat(self, message):
        if self.chat_transcript_area:
            self.chat_transcript_area.insert('end', message + '\n')
            self.chat_transcript_area.yview(END)

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            if self.client_socket:
                self.client_socket.close()
            exit(0)


class LoginWindow:
    def __init__(self, master, on_success, client_socket):
        self.root = master
        self.on_success = on_success
        self.client_socket = client_socket
        self.top = Toplevel(self.root)
        self.top.title('Login / Registro')
        self.top.geometry('350x250')
        self.frame = Frame(self.top)
        self.frame.pack(pady=10)
        # Login
        Label(self.frame, text='Usuario:').grid(row=0, column=0, sticky='e')
        self.login_entry = Entry(self.frame)
        self.login_entry.grid(row=0, column=1)
        Label(self.frame, text='Clave:').grid(row=1, column=0, sticky='e')
        self.clave_entry = Entry(self.frame, show='*')
        self.clave_entry.grid(row=1, column=1)
        Button(self.frame, text='Iniciar sesión', command=self.login).grid(row=2, column=0, columnspan=2, pady=5)
        # Registro
        Label(self.frame, text='--- Registro ---').grid(row=3, column=0, columnspan=2)
        Label(self.frame, text='Nombre:').grid(row=4, column=0, sticky='e')
        self.nombre_entry = Entry(self.frame)
        self.nombre_entry.grid(row=4, column=1)
        Label(self.frame, text='Apellido:').grid(row=5, column=0, sticky='e')
        self.apellido_entry = Entry(self.frame)
        self.apellido_entry.grid(row=5, column=1)
        Label(self.frame, text='Usuario:').grid(row=6, column=0, sticky='e')
        self.reg_login_entry = Entry(self.frame)
        self.reg_login_entry.grid(row=6, column=1)
        Label(self.frame, text='Clave:').grid(row=7, column=0, sticky='e')
        self.reg_clave_entry = Entry(self.frame, show='*')
        self.reg_clave_entry.grid(row=7, column=1)
        Button(self.frame, text='Registrar', command=self.register).grid(row=8, column=0, columnspan=2, pady=5)
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def login(self):
        login = self.login_entry.get().strip()
        clave = self.clave_entry.get().strip()
        if not login or not clave:
            messagebox.showerror('Error', 'Ingrese usuario y clave')
            return
        msg = f'LOGIN:{login}:{clave}'
        self.client_socket.send(msg.encode('utf-8'))
        resp = self.client_socket.recv(256).decode('utf-8')
        if resp.startswith('OK:'):
            self.top.destroy()
            self.root.deiconify()
            self.on_success(login)
        else:
            messagebox.showerror('Error', resp[6:] if resp.startswith('ERROR:') else resp)

    def register(self):
        nombre = self.nombre_entry.get().strip()
        apellido = self.apellido_entry.get().strip()
        login = self.reg_login_entry.get().strip()
        clave = self.reg_clave_entry.get().strip()
        if not (nombre and apellido and login and clave):
            messagebox.showerror('Error', 'Complete todos los campos de registro')
            return
        msg = f'REGISTER:{nombre}:{apellido}:{login}:{clave}'
        self.client_socket.send(msg.encode('utf-8'))
        resp = self.client_socket.recv(256).decode('utf-8')
        if resp.startswith('OK:'):
            messagebox.showinfo('Registro', 'Usuario registrado correctamente. Ahora puede iniciar sesión.')
        else:
            messagebox.showerror('Error', resp[6:] if resp.startswith('ERROR:') else resp)

    def on_close(self):
        self.root.destroy()


if __name__ == '__main__':
    root = Tk()  # Chat application window
    root.withdraw()  # Ocultar ventana principal hasta login exitoso
    # Inicializar socket antes de login
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = '127.0.0.1'  # IP address
    remote_port = 10319  # TCP port
    client_socket.connect((remote_ip, remote_port))
    def start_gui(username):
        gui = GUI(root, client_socket=client_socket)
        if gui.name_widget:
            gui.name_widget.insert(0, username)
            gui.name_widget.config(state='disabled')
        root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    login_win = LoginWindow(root, start_gui, client_socket)
    root.mainloop()
