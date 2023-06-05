import socket
import threading
import json

ip_server = '192.168.100.128'
purto_server = 8404

class Estacion:
    def __init__(self, sala, numero, cara, objeto):
        self.sala = sala
        self.numero = numero
        self.cara = cara
        self.objeto = objeto

    def ocupado(self):
        return self.cara and self.objeto
        

estaciones_Montevideo = []
estaciones_RyM = []
estaciones_Area52 = []


def client(socket, address):
    print("Se conectó: {}".format(address))

    while (True):
        data_code = socket.recv(1024)
        if not data:
            break

        data_json = data_code.decode()
        data = json.loads(data_json)
        if (data['tipo']=='new_station'):
            station = Estacion(data['sala'], data['NEstacion'], False, False)
            if (data['sala'] == 'Montevideo'):
                estaciones_Montevideo.append(station)
                print("Se agrego estación a Montevideo.")
            elif (data['sala'] == 'RyM'):
                estaciones_RyM.append(station)
                print("Se agrego estación a Rick & Morty.")
            elif (data['sala'] == 'Area52'):
                estaciones_Area52.append(station)
                print("Se agrego estación a Área 52.")





def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ip_server, purto_server))

    s.listen(60)
  
    while (True):
        clientSocket, clientAddress = s.accept()
        client_thread = threading.Thread(target= client, args= (clientSocket, clientAddress))
        client_thread.start()

try:
    start_server()
except KeyboardInterrupt:
    print("Server finalizado manualmente por usuario.")