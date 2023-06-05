import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

trigger = 18
echo = 24

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def distancia():
    GPIO.output(trigger, True)

    time.sleep(0.00001)
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
