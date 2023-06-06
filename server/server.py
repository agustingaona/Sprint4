import socket
import threading
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import slack.web
from flask import Flask, request

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
        

estaciones_Einstein = []
estaciones_Newton = []
estaciones_Area52 = []

def cantidadSala(sala):
    ocupado = 0
    for estacion in sala:
        if (estacion.ocupado()):
            ocupado += 1
    return ocupado

def client(socket, address):
    print("Se conectó: {}".format(address))

    while (True):
        data_code = socket.recv(1024)
        if not data:
            break

        data_json = data_code.decode()
        data = json.loads(data_json)
        if (data['tipo'] == 'new_station'):
            station = Estacion(data['sala'], data['NEstacion'], False, False)
            if (data['sala'] == 'Einstein'):
                estaciones_Einstein.append(station)
                print("Se agrego estación a Montevideo.")
            elif (data['sala'] == 'Newton'):
                estaciones_Newton.append(station)
                print("Se agrego estación a Rick & Morty.")
            # Si hay sala nueva agregarla.
        elif (data['tipo'] == 'update'):
            if (data['sala'] == 'Einstein'):
                for estacion in estaciones_Einstein:
                    if (estacion.numero == data['num_estacion']):
                        estacion.cara = data['cara']
                        estacion.objeto = data['objeto']
            elif (data['sala'] == 'Newton'):
                for estacion in estaciones_Newton:
                    if (estacion.numero == data['num_estacion']):
                        estacion.cara = data['cara']
                        estacion.objeto = data['objeto']
            # Si hay sala nueva agregarla.
            

def slackBot():
    token = "xoxb-5382984556802-5380324370133-AC65SWoHURbIVi95EKLjH851"
    cliente = WebClient(token=token)
    canal = "C05B2A35F3Q"

    app = Flask(__name__)
    @app.route('/slack/events', methods=['POST'])
    def event_handler():
        data = request.json
        if 'event' in data and 'type' in data['event'] and data['event']['type'] == 'message':
            event = data['event']
            channel_id = event['channel']
            user_id = event['user']
            text = event['text']
            if (text == "hola querido"):
                try:
                    response = cliente.chat_postMessage(channel=canal, text="queridooo :heart:")
                    print("Mensaje enviado:", response["ts"])
                except SlackApiError as e:
                    print("Error al  enviar:", e.response['error'])
        return 'OK'
    
    if __name__ == '__main__':
        app.run()


    #msj = "holaaaa grupooo :smile:"
    #try:
    #    response = cliente.chat_postMessage(channel=canal, text=msj)
    #    print("Mensaje enviado:", response["ts"])
    #except SlackApiError as e:
    #    print("Error al  enviar:", e.response['error'])



def start_server():
    bot_thread = threading.Thread(target=slackBot)
    bot_thread.start()

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