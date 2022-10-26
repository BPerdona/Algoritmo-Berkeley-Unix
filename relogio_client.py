import threading
import socket
from tempo import Tempo
from time import sleep
from tempo import timeToSeconds, timeToArray


class Client:
    def __init__(self, port):
        self.tempo = Tempo()
        self.HOST = '127.0.0.1'
        self.PORT = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen()
        self.serverPort = 5000

        # Relogio
        print(f"Relogio rodadando em {self.HOST}:{self.PORT}")
        threading.Thread(target=self.clock).start()
        threading.Thread(target=self.receiveServer).start()

    def clock(self):
        while True:
            sleep(1)
            self.tempo.add_seconds()
            print(f"Tempo relogio -> {self.tempo.hora:02}:{self.tempo.minuto:02}:{self.tempo.segundo:02}")

    def send(self):
        print("Enviando tempo")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("127.0.0.1", self.serverPort))
            client.sendall(str.encode(f"{self.PORT},{timeToSeconds([self.tempo.hora, self.tempo.minuto, self.tempo.segundo])}"))
        except:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receiveServer(self):
        while True:
            connection, address = self.tcp.accept()
            message = connection.recv(1024).decode()
            if message == "SEND":
                threading.Thread(target=self.send).start()
            else:
                tempo_att = timeToSeconds([self.tempo.hora, self.tempo.minuto, self.tempo.segundo]) - int(message)
                print(f"Diferença -> {int(message)}")
                print(f"Atualizou para -> {tempo_att}")
                self.tempo.hora, self.tempo.minuto, self.tempo.segundo = timeToArray(tempo_att)
