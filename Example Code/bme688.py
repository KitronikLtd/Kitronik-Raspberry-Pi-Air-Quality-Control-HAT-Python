from time import sleep
from KitronikAirQualityControlHAT import *

print("BME688")
# Initialise the BME688 sensor
bme688 = KitronikBME688()
# Initialise the OLED display
oled = KitronikOLED()
# Calculate the baseline values for the BME688 sensor
bme688.calcBaselines(oled) # Takes OLED as input to show progress

# Measure the sensor every second
while True:
    # Update the sensor values
    bme688.measureData()
    oled.clear()
    # Read and output the sensor values to the OLED display
    oled.displayText("Temperature:" + str(bme688.readTemperature()), 1)
    oled.displayText("Pressure:" + str(bme688.readPressure()), 2)
    oled.displayText("Humidity:"+  str(bme688.readHumidity()), 3)
    oled.displayText("eCO2:" + str(bme688.readeCO2()), 4)
    oled.displayText("Air Quality %:" + str(bme688.getAirQualityPercent()), 5)
    oled.displayText("Air Quality Score:" + str(bme688.getAirQualityScore()), 6)
    oled.show()

    # Read and output the sensor values
    print("Temperature:", bme688.readTemperature())
    print("Pressure:", bme688.readPressure())
    print("Humidity:", bme688.readHumidity())
    print("eCO2:", bme688.readeCO2())
    print("Air Quality %:", bme688.getAirQualityPercent())
    print("Air Quality Score:", bme688.getAirQualityScore())
    sleep(1)