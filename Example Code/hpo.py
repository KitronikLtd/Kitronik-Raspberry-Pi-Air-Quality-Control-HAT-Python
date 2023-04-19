from time import sleep
from KitronikAirQualityControlHAT import *

print("High Power Out")
# Initialise High Power Out 1 without PWM
hpo1 = KitronikHighPowerOut(1)
# Initialise High Power Out 2 with PWM
hpo2 = KitronikHighPowerOut(2, isPWM = True)

while True:
    # Turn on High Power Out 1
    hpo1.turnOn()
    sleep(2)
    # Turn off High Power Out 1
    hpo1.turnOff()

    # Start the PWM output on High Power Out 2
    hpo2.start()
    # Gradually increase the High Power Out 2 PWM duty cycle to 100
    for dc in range(0, 101, 5):
        hpo2.changeDutyCycle(dc)
        sleep(0.2)
    # Stop the PWM output on High Power Out 2
    hpo2.stop()