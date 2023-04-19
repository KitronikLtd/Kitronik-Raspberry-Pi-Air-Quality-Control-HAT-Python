from time import sleep
from KitronikAirQualityControlHAT import *

print("Buzzer")
# Initialise the Buzzer
buzzer = KitronikBuzzer()

while True:
    # Start the Buzzer generating sound
    buzzer.start()
    # Gradually change the sound of the Buzzer
    buzzer.changeTone(440)
    sleep(0.1)
    buzzer.changeTone(494)
    sleep(0.1)
    buzzer.changeTone(523)
    sleep(0.1)
    buzzer.changeTone(587)
    sleep(0.1)
    buzzer.changeTone(659)
    sleep(0.1)
    buzzer.changeTone(698)
    sleep(0.1)
    buzzer.changeTone(784)
    sleep(0.1)
    # Stop the Buzzer generating sound
    buzzer.stop()
    sleep(5)
