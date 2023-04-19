from time import sleep
from KitronikAirQualityControlHAT import *

print("GPIO")
# Initialise the GPIO
gpio22 = KitronikGPIO(22) # Without PWM
gpio23 = KitronikGPIO(23, isPWM = False) # Without PWM
gpio24 = KitronikGPIO(24, isPWM = True) # With PWM

while True:
    # Gradually turn on the 3 GPIOs
    gpio22.turnOn()
    sleep(1)
    gpio23.turnOn()
    sleep(1)
    gpio24.start()
    # Gradually increase the GPIO PWM duty cycle to 100
    for dc in range(0, 101, 5):
        gpio24.changeDutyCycle(dc)
        sleep(0.1)
    # Gradually turn off the 3 GPIOs
    gpio22.turnOff()
    sleep(1)
    gpio23.turnOff()
    sleep(1)
    gpio24.stop()
    sleep(1)