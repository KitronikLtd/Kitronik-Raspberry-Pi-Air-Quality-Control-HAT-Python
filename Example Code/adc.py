from time import sleep
from KitronikAirQualityControlHAT import *

# Initialise the ADCs
adc0 = KitronikADC(0)
adc1 = KitronikADC(1)
adc2 = KitronikADC(2)

while True:
    # Read and output the current ADC values
    print("ADC0:", adc0.read())
    print("ADC1:", adc1.read())
    print("ADC2:", adc2.read())
    sleep(1)