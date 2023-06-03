import socket
import threading
import mysql.connector
import json


func = True
base = mysql.connector.connect(host="127.0.0.1", user="root", password="123456", database="Salas")
cursor = base.cursor()
base.autocommit = True
suscriptores = []


def client(socket, address):
    print("Se conectó: {}".format(address))

    while (True):
        data = socket.recv(1024)
        if not data:
            break

        data_str = data.decode()
        data_ok = json.loads(data_str)
        print(data_ok)
        if (data_ok["tipo"]=="inicio"):
            query = ("SELECT nombre, apellido FROM empleados WHERE id_empleado = "+str(data_ok["data"])+";")
            cursor.execute(query)
            info = cursor.fetchall()

            msj = ("{} {} ha llegado a NetLabs!".format(info[0][0], info[0][1])).encode()
            for sock in suscriptores:
                sock.sendall(msj)
        elif (data_ok['tipo'] == 'susc'):
            suscriptores.append(socket)
        elif (data_ok['tipo'] == 'desusc'):
            suscriptores.pop(socket)
        else:
            query = data_ok["data"]
            cursor.execute(query)
            datos = cursor.fetchall()
            if (len(datos) > 0):
                json_datos = json.dumps(datos)
                json_bytes = json_datos.encode()
                socket.sendall(json_bytes)
            else:
                print("Query sin devolución.")



def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '192.168.100.119'
    port = 8404

    s.bind((host, port))

    s.listen(60)
  
    while (True):
        clientSocket, clientAddress = s.accept()
        client_thread = threading.Thread(target= client, args= (clientSocket, clientAddress))
        client_thread.start()

start_server()