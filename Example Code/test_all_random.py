from time import sleep
from KitronikAirQualityControlHAT import *


print("OLED Display")
# Initialise the OLED display
oled = KitronikOLED()
# Draw an empty rectangle on the OLED display
oled.drawRect(0, 0, 24, 24)
# Update the OLED display with the changes
oled.show()
sleep(0.2)
# Draw a filled rectangle on the OLED display
oled.drawRect(25, 0, 24, 24, fill = True)
# Update the OLED display with the changes
oled.show()
sleep(0.2)
# Remove everythig from the OLED display
oled.clear()
sleep(0.2)
# Write the following text on line 1 of the OLED display
oled.displayText("Hello dev :)", 1)
# Write the following text on line 2 of the OLED display
oled.displayText("Here again!", 2, 32) # With a 32 pixel margin at the start
# Draw a diagonal line across the OLED display
oled.drawLine(32, 32, 64, 64)
# Update the OLED display with the changes
oled.show()
# Load the kitronik-logo.jpg image onto the OLED display
oled.image = Image.open("kitronik-logo.jpg")
# Convert the image to greyscale on the OLED display
oled.image = oled.image.convert('1')
# Resize the image to fit on the OLED display
oled.image = oled.image.resize((128, 64))
# Invert the colours of the image (black to white, white to black)
oled.invert(1)
# Update the OLED display with the changes
oled.show()


# Initialise the ADCs
adc0 = KitronikADC(0)
adc1 = KitronikADC(1)
adc2 = KitronikADC(2)
# Read and output the current ADC values
print(adc0.read())


# Initialise the Real Time Clock
rtc = KitronikRTC()
# Read and output the current time on the Real Time Clock
print("RTC READ:", rtc.read())


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


print("ZIPLEDs Brightness")
# Gradually increase the ZIPLEDs brightness from 0 to 100
for i in range(101):
    zipLEDs.setBrightness(i)
    zipLEDs.show()


print("Buzzer")
# Initialise the Buzzer
buzzer = KitronikBuzzer()
# Start the Buzzer generating sound
buzzer.start()
# Gradually change the sound of the Buzzer
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


print("ADC1:", adc1.read())
# Update the current time on the Real Time Clock
rtc.set(2023, 1, 23, 1, 22, 20, 21)
print("RTC SET")


print("GPIO")
# Initialise the GPIO
gpio22 = KitronikGPIO(22) # Without PWM
gpio23 = KitronikGPIO(23, isPWM = False) # Without PWM
gpio24 = KitronikGPIO(24, isPWM = True) # With PWM
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


print("ADC2:", adc2.read())


print("High Power Out")
# Initialise High Power Out 1 without PWM
hpo1 = KitronikHighPowerOut(1)
# Turn on High Power Out 1
hpo1.turnOn()
sleep(2)
# Turn off High Power Out 1
hpo1.turnOff()
# Initialise High Power Out 2 with PWM
hpo2 = KitronikHighPowerOut(2, isPWM = True)
# Start the PWM output on High Power Out 2
hpo2.start()
# Gradually increase the High Power Out 2 PWM duty cycle to 100
for dc in range(0, 101, 5):
    hpo2.changeDutyCycle(dc)
    sleep(0.2)
# Stop the PWM output on High Power Out 2
hpo2.stop()


print("ZIPLEDs")
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
    

print("Servo")
# Initialise the Servo
servo = KitronikServo()
# Start the PWM output to the Servo
servo.start()
# Gradually move the Servo from 0% to 100%
sleep(0.1)
servo.changePercent(25)
sleep(0.1)
servo.changePercent(50)
sleep(0.1)
servo.changePercent(75)
sleep(0.1)
servo.changePercent(100)
sleep(0.1)
servo.changePercent(75)
sleep(0.1)
servo.changePercent(50)
sleep(0.1)
servo.changePercent(25)
sleep(0.1)
servo.changePercent(0)
# Gradually move the Servo from 0 degrees to 180 degrees
sleep(0.1)
servo.changeAngle(0)
sleep(0.1)
servo.changeAngle(45)
sleep(0.1)
servo.changeAngle(90)
sleep(0.1)
servo.changeAngle(135)
sleep(0.1)
servo.changeAngle(180)
sleep(0.1)
servo.changeAngle(135)
sleep(0.1)
servo.changeAngle(90)
sleep(0.1)
servo.changeAngle(45)
sleep(0.1)
servo.changeAngle(0)
sleep(0.1)
# Stop the PWM output to the Servo
servo.stop()


# Read and output the updated time on the Real Time Clock
print("RTC READ:", rtc.read())


print("BME688")
# Initialise the BME688 sensor
bme688 = KitronikBME688()
# Calculate the baseline values for the BME688 sensor
bme688.calcBaselines(oled) # Takes OLED as input to show progress
# Measure the sensor every second for a minute
for i in range(5):
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

