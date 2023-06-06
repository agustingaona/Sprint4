import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)


def distancia(estacion):
    GPIO.setup(estacion['trigger'], GPIO.OUT)
    GPIO.setup(estacion['echo'], GPIO.IN)

    GPIO.output(estacion['trigger'], True)

    time.sleep(0.00001)
    GPIO.output(estacion['trigger'], False)

    StartTime = time.time()
    StopTime = time.time()

    while (GPIO.input(estacion['echo']) == 0):
        StartTime = time.time()

    while (GPIO.input(estacion['echo']) == 1):
        StopTime = time.time()

    timeDif = StopTime - StartTime

    d = (timeDif * 34300) / 2

    return int(d)

print(distancia())