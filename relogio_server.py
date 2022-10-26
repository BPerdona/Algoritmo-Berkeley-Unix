import math
import socket
import threading
import time
from tempo import Tempo, timeToSeconds, timeToArray


class Server:
    def __init__(self, port):
        # Configuração TCP
        self.HOST = '127.0.0.1'
        self.PORT = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen()
        self.receives = 0

        # Relogio
        self.relogios = {
            5001: 0,
            5002: 0,
            5003: 0,
            5004: 0
        }
        self.tempo = Tempo()
        print(f"Servidor rodadando em {self.HOST}:{self.PORT}")
        threading.Thread(target=self.clock).start()
        threading.Thread(target=self.receive).start()

    def clock(self):
        aux = 0
        while True:
            time.sleep(1)
            self.tempo.add_seconds()
            aux += 1
            print(f"Tempo servidor -> {self.tempo.hora:02}:{self.tempo.minuto:02}:{self.tempo.segundo:02}")
            if aux == 10:
                print("Executando algoritmo de Berkeley Unix")
                threading.Thread(target=self.sendFlag).start()
                aux = 0

    def receive(self):
        while True:
            connection, address = self.tcp.accept()
            msg = connection.recv(1024).decode()
            porta = msg.split(',')[0]
            self.relogios[int(porta)] = int(msg.split(',')[1])
            self.receives += 1
            if self.receives == len(self.relogios):
                self.receives = 0
                print("Recebeu o tempo de todos os relogios!")
                threading.Thread(target=self.sendRealTime).start()

    def sendFlag(self):
        for relogio, tempo in self.relogios.items():
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                client.connect(("127.0.0.1", relogio))
                client.sendall(str.encode(f"SEND"))
            except:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client.close()

    def sendRealTime(self):
        media = 0
        media = timeToSeconds([self.tempo.hora, self.tempo.minuto, self.tempo.segundo])
        for relogio, tempo in self.relogios.items():
            media += tempo

        media = round(media / (len(self.relogios) + 1))  # +1 relacionado ao servidor
        print(f"Média gerada -> {media}")

        self.tempo.hora, self.tempo.minuto, self.tempo.segundo = timeToArray(media)
        for relogio, tempo in self.relogios.items():
            retorno = tempo - media
            print(f"Relogio {relogio} redebeu diferença de -> {retorno} s")

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect(("127.0.0.1", relogio))
                client.sendall(str.encode(f"{retorno}"))
            except:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            client.close()
