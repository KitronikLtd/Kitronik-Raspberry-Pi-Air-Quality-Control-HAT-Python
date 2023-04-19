from time import sleep
from KitronikAirQualityControlHAT import *

print("ZIPLEDs")
# Initialise the ZIPLEDs, with auto show turned off
zipLEDs = KitronikZIPLEDs(autoShow = False)
r = 255
g = 0
b = 0
# Set each pixel to red
for i in range(3):
    zipLEDs.setPixel(i, (r, g, b))
# Update the ZIPLEDs with the updated values
zipLEDs.show()
step = 1
# Loop and gradually update ZIPLEDs to create a rainbow effect
for i in range(765):
    if r > 0 and b == 0:
        r -= step
        g += step
    elif g > 0:
        g -= step
        b += step
    else:
        r += step
        b -= step
    # Set all the pixels to the new r,g,b values
    zipLEDs.fill((r, g, b))
    # Update the ZIPLEDs with the updated values
    zipLEDs.show()


print("ZIPLEDs Brightness")
# Gradually increase the ZIPLEDs brightness from 0 to 100
for i in range(101):
    zipLEDs.setBrightness(i)
    zipLEDs.show()
    sleep(0.1)