import socket
import detectorDistancia
import detectorCara
import time
import json

ip_server = '192.168.100.128'
puerto_server = 0

num_estacion = 0
sala = "Einstein"
estaciones = [{'num_estacion': 1, 'cara': False, 'objeto':False, 'trigger': 0, 'echo': 0, 'camara': 0, 'disponible': False},
              {'num_estacion': 2, 'cara': False, 'objeto':False, 'trigger': None, 'echo': None, 'camara': None, 'disponible': False},
              {'num_estacion': 3, 'cara': False, 'objeto':False, 'trigger': None, 'echo': None, 'camara': None, 'disponible': False},
              {'num_estacion': 4, 'cara': False, 'objeto':False, 'trigger': None, 'echo': None, 'camara': None, 'disponible': False}]

for estacion in estaciones:
    if (not estacion['trigger'] is None and not estacion['echo'] is None):
        estacion['disponible'] = True

socketRasp = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
socketRasp.connect((ip_server, puerto_server))

for estacion in estaciones:
    if (estacion['disponible']):
        data = {
            'tipo': 'new_station',
            'socket': socketRasp,
            'NEstacion': estacion['num_estacion'],
            'sala': sala
        }
        data_json = json.dumps(data)
        socketRasp.sendall(data_json.encode())

while (True):
    for estacion in estaciones:
        objeto = False
        cara = False
        if (detectorCara.contar_personas(estacion) > 0):
            cara = True
        if (detectorDistancia.distancia(estacion) < 15):
            objeto = True
        data = {
            'tipo': 'update',
            'sala': sala,
            'num_estacion': estacion['num_estacion'],
            'objeto': objeto,
            'cara': cara
        }
        data_json = json.dumps(data)
        socketRasp.sendall(data_json.encode())
    time.sleep(60)