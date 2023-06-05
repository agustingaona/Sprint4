import socket
import detectorDistancia
import detectorCara
import json

ip_server = '192.168.100.128'
puerto_server = 0

num_estacion = 0
sala = "Montevideo"

socketRasp = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

socketRasp.connect((ip_server, puerto_server))
data = {
    'tipo': 'new_station',
    'socket': socketRasp,
    'NEstacion': num_estacion,
    'sala': sala
}
data_json = json.dumps(data)
socketRasp.sendall(data_json.encode())

while (True):
    socketRasp.s