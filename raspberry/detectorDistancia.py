import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor

def falsaMedicion(estacion):
    trigger = estacion['trigger']
    echo = estacion['echo']

    # Logica del sensor

    return 13

def medir_distancia(estacion):
    trigger = estacion['trigger']
    echo = estacion['echo']
    time.sleep(0.1)
    
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(echo) == 0:
        StartTime = time.time()

    while GPIO.input(echo) == 1:
        StopTime = time.time()

    tiempo = StopTime - StartTime
    velocidad_sonido = 34300
    distancia = (tiempo * velocidad_sonido) / 2

    return int(distancia)

def distancia(estacion):
    sensor = DistanceSensor(estacion['echo'], estacion['trigger'])

    distancia = sensor.distance*100
    return int(distancia)