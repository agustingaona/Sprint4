import socket
import threading
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pyttsx3
from pyHS100 import SmartPlug

# Modificable -------------------------------------
ip_server = '192.168.100.111'
purto_server = 8404

sala_Einstein = {'name': 'Einstein',
                 'estaciones': [],
                 'llena': False,
                 'ip_luz': 0}
sala_Newton = {'name': 'Newton',
               'estaciones': [],
               'llena': False,
               'ip_luz': 0}

salas = [sala_Einstein, sala_Newton]
# -----------------------------------------------

# Funciones, Clases y variables -------------------------------------
func = True
token_bot = "xoxb-5382984556802-5380324370133-jvZiNPY5fOZxJ54XjEo0ZOS7"
canal = "C05B2A35F3Q"
contador_msj = 0
app = App(token=token_bot)


class Estacion:
    def __init__(self, sala, numero, cara, objeto):
        self.sala = sala
        self.numero = numero
        self.cara = cara
        self.objeto = objeto

    def ocupado(self):
        return self.cara and self.objeto


def cantidadOcupados(sala):
    ocupado = 0
    for estacion in sala['estaciones']:
        if (estacion.ocupado()):
            ocupado += 1
    return ocupado

def leer_texto(texto):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'spanish-latin-am')
    engine.setProperty('rate', 150)
    engine.say(texto)
    engine.runAndWait()

def encender_luz(ip):
    try:
        plug = SmartPlug(ip)
        plug.turn_on()
        print("Luz encendida")
    except Exception as e:
        print("Error al encender lux:", str(e))

def apagar_luz(ip):
    try:
        plug = SmartPlug(ip)
        plug.turn_off()
        print("Luz apagada")
    except Exception as e:
        print("Error al apagar luz:", str(e))
# -----------------------------------------------------------------

# Eventos de Slack -------------------------------------------------
@app.event('message')
def muchosMsg(body , say):
    global contador_msj
    contador_msj += 1
    if (contador_msj > 5):
        say("Dejen mi canal en paz :rage:")
        contador_msj = 0

@app.command('/salas')
def mostrarSalas(ack, respond, command):
    ack()
    msj = ""
    for sala in salas:
        sala_name = sala['name']
        sala_ocupados = cantidadOcupados(sala)
        sala_max = len(sala['estaciones'])
        if (sala_ocupados == sala_max):
            aux = "Sala {}, {}/{} estaciones ocupadas. :red_circle:\n".format(sala_name, sala_ocupados, sala_max)
            msj += aux
        else:
            aux = "Sala {}, {}/{} estaciones ocupadas. :large_green_circle:\n".format(sala_name, sala_ocupados, sala_max)
            msj += aux
    respond(msj)

@app.command('/disponibles')
def mostrarDisponibles(ack, respond, command):
    ack()
    msj = ""
    for sala in salas:
        sala_name = sala['name']
        sala_ocupados = cantidadOcupados(sala)
        sala_max = len(sala['estaciones'])
        if (sala_ocupados < sala_max):
            aux = "Sala {}, {}/{} estaciones ocupadas. :large_green_circle:\n".format(sala_name, sala_ocupados, sala_max)
            msj += aux
    respond(msj)


def slackBot():
    if __name__ == '__main__':
        SocketModeHandler(app, "xapp-1-A05B96HUM7U-5409523457329-d9383ca8c6a1019d213db443734562e34d56b8fe6635491a574ca148c892bb23").start()
# ---------------------------------------------------------------------


# Cliente(Raspberry) ----------------------------------------------
def client(socket, address):
    print("Se conectó: {}".format(address))

    while (func):
        data_code = socket.recv(1024)
        if not data_code:
            break

        data_json = data_code.decode()
        data = json.loads(data_json)
        if (data['tipo'] == 'new_station'):
            for sala in salas:
                if (data['sala'] == sala['name']):
                    sala_nombre = data['sala']
                    num_estacion = data['NEstacion']
                    station = Estacion(sala_nombre, num_estacion, False, False)
                    sala['estaciones'].append(station)
                    print("Se agregó estación N°{} a sala {}".format(num_estacion, sala_nombre))
        elif (data['tipo'] == 'update'):
            global contador_msj
            for sala in salas:
                if (data['sala'] == sala['name']):
                    for estacion in sala['estaciones']:
                        if (estacion.numero == data['num_estacion']):
                            estacion.cara = data['cara']
                            estacion.objeto = data['objeto']
                    if (sala['llena']):
                        sala_name = sala['name']
                        sala_max = len(sala['estaciones'])
                        sala_ocupados = cantidadOcupados(sala)
                        if (sala_max != sala_ocupados):
                            app.client.chat_postMessage(channel=canal, text= "Se liberó sala {} con {}/{} estaciones ocupadas :runner:".format(sala_name, sala_ocupados, sala_max))
                            txt = "La sala {} esta disponible, quedan {} lugares libres".format(sala_name, (sala_max-sala_ocupados))
                            leer_texto(txt)
                            apagar_luz(sala['ip_luz'])
                            sala['llena'] = False
                            print("Sala {} liberada {}/{}".format(sala_name, sala_ocupados, sala_max))
                            contador_msj = 0
                    else:
                        sala_name = sala['name']
                        sala_max = len(sala['estaciones'])
                        sala_ocupados = cantidadOcupados(sala)
                        if (sala_max == sala_ocupados):
                            app.client.chat_postMessage(channel=canal, text= "Se llenó sala {}, no molesten :angry:".format(sala_name, sala_ocupados, sala_max))
                            txt = "La sala {} se ha llenado".format(sala_name)
                            leer_texto(txt)
                            encender_luz(sala['ip_luz'])
                            sala['llena'] = True
                            print("Sala {} llena {}/{}".format(sala_name, sala_ocupados, sala_max))
                            contador_msj = 0
# -------------------------------------------------------------

# Servidor e inicio de procesos ------------------------------------------------------------------
def start_server():
    bot_thread = threading.Thread(target=slackBot)
    bot_thread.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ip_server, purto_server))

    s.listen(60)
    
    while (func):
        clientSocket, clientAddress = s.accept()
        client_thread = threading.Thread(target= client, args= (clientSocket, clientAddress))
        client_thread.start()

    s.close()
# ------------------------------------------------------------------------------------------

try:
    start_server()
except KeyboardInterrupt:
    print("Server finalizado manualmente por usuario.")
    func = False