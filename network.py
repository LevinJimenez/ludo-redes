import socket
# Importa el módulo 'socket' para la comunicación de red.

class Network:
    # Define la clase 'Network' para manejar la conexión y comunicación con el servidor.
    def __init__(self):
        # Constructor de la clase 'Network'.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Crea un objeto socket del cliente (IPv4, TCP).
        self.server = socket.gethostname()
        # Obtiene el nombre de host local como la dirección del servidor.
        self.port = 5555
        # Define el número de puerto para la conexión.
        self.addr = (self.server, self.port)
        # Crea una tupla con la dirección del servidor y el puerto.
        self.pos = self.connect()
        # Llama al método 'connect' para establecer la conexión e inicializa 'pos' con la respuesta del servidor.
    def getPos(self):
        # Método para obtener la posición recibida del servidor.
        return self.pos
        # Retorna el valor de 'pos'.
    def connect(self):
        # Método para establecer la conexión con el servidor.
        try:
            # Inicia un bloque try-except para manejar posibles errores de conexión.
            self.client.connect(self.addr)
            # Intenta conectar el socket del cliente a la dirección especificada.
            return self.client.recv(2048).decode()
            # Recibe hasta 2048 bytes de datos del servidor y los decodifica como una cadena.
        except:
            # Captura cualquier excepción que ocurra durante la conexión.
            pass
            # No hace nada si ocurre un error (la conexión falló silenciosamente).
    def send(self, data):
        # Método para enviar datos al servidor y recibir una respuesta.
        try:
            # Inicia un bloque try-except para manejar errores de socket.
            self.client.send(str.encode(data))
            # Codifica los datos de entrada a bytes y los envía al servidor.
            return self.client.recv(2048).decode()
            # Recibe y decodifica la respuesta del servidor.
        except socket.error as e:
            # Captura excepciones específicas de socket y las asigna a 'e'.
            print(e)
            # Imprime el error del socket.

# n = Network()
# print(n.send("hello"))
# print(n.send("working"))