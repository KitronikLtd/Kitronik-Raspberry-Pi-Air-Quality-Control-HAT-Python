from time import sleep
from KitronikAirQualityControlHAT import *

# Initialise the Real Time Clock
rtc = KitronikRTC()
# Read and output the current time on the Real Time Clock
print("RTC READ:", rtc.read())
# Update the current time on the Real Time Clock
rtc.set(2023, 1, 23, 1, 22, 20, 21)
print("RTC SET")
sleep(5)
# Read and output the updated time on the Real Time Clock
print("RTC READ:", rtc.read())