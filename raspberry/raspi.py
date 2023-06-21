import socket
import detectorDistancia
import detectorCara
import time
import json
import RPi.GPIO as GPIO

# Modificables -------------------------------
ip_server = '192.168.100.111'
puerto_server = 8404

sala = "Einstein"
estaciones = [{'num_estacion': 1, 'cara': False, 'objeto':False, 'trigger': 18, 'echo': 24, 'camara': 0, 'disponible': False},
              {'num_estacion': 2, 'cara': False, 'objeto':False, 'trigger': None, 'echo': None, 'camara': None, 'disponible': False},
              {'num_estacion': 3, 'cara': False, 'objeto':False, 'trigger': None, 'echo': None, 'camara': None, 'disponible': False},
              {'num_estacion': 4, 'cara': False, 'objeto':False, 'trigger': None, 'echo': None, 'camara': None, 'disponible': False}]
# -------------------------------------------

# Socket, conexión y setup de pines ------------------------------
socketRasp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRasp.connect((ip_server, puerto_server))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for estacion in estaciones:
    if (not estacion['trigger'] is None and not estacion['echo'] is None):
        estacion['disponible'] = True
        GPIO.setup(estacion['trigger'], GPIO.OUT)
        GPIO.setup(estacion['echo'], GPIO.IN)

# ---------------------------------------------------------------

# Envío de estaciones disponibles -----------------------------
for estacion in estaciones:
    if (estacion['disponible']):
        data = {
            'tipo': 'new_station',
            'NEstacion': estacion['num_estacion'],
            'sala': sala
        }
        data_json = json.dumps(data)
        socketRasp.sendall(data_json.encode())
# -------------------------------------------------------------

# detectorDistancia --------------------------

def distancia(estacion):
    trigger = estacion['trigger']
    echo = estacion['echo']
    
    print(trigger)
    print(echo)

    GPIO.output(trigger, True)

    time.sleep(0.001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    while (GPIO.input(echo) == 0):
        StartTime = time.time()

    while (GPIO.input(echo) == 1):
        StopTime = time.time()

    timeDif = StopTime - StartTime

    d = (timeDif * 34300) / 2

    return int(d)

# -------------------------------------------

while (True):
    for estacion in estaciones:
        if (estacion['disponible']):
            print("aca entra")
            objeto = False
            cara = False
            if (detectorCara.contar_personas(estacion) > 0):
                cara = True
            if (detectorDistancia.medir_distancia(estacion) < 15):
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
    time.sleep(10)