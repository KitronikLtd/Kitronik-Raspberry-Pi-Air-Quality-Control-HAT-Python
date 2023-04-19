# Kitronik Air Quality Control HAT
In this repo is the library for the [Kitronik Air Quality Control HAT](https://kitronik.co.uk/5038) and the example code to test your HAT.

## Enable Serial Connection on the Raspberry Pi
We are going to enable serial0 from the Raspberry Pi to connect to the HAT. We need to edit the Raspberry Pi configuration by executing the following command:
```
sudo raspi-config
```

Inside of the configuration helper select the following options:
```
3 Interface Options
I6 Serial Port
Login shell over serial? No
Serial port hardware enabled? Yes
```

## Install the library
Run the following command on your Raspberry Pi in the terminal:
```
pip install KitronikAirQualityControlHAT
```

## Run the test code
Copy the code from one of the files in the `Example Code` folder onto your Raspberry Pi. For example, copy the `test_all.py` file.

Also download the `Example Code\kitronik-logo.jpg` to test your OLED Display.

Then run the following command in the terminal to run the test code, replacing `test_all.py` with the name of the file you copied:
```
python test_all.py
```
<br/>

# How to use the HAT
Below is a small section for each component on the HAT explaining how to use it.
- [BME688](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#bme688)
- [OLED Display](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#oled-display)
- [ZIPLEDs](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#zipleds)
- [Real Time Clock](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#real-time-clock)
- [ADC](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#adc)
- [Buzzer](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#buzzer)
- [GPIO](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#gpio)
- [High Power Out](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#high-power-out)
- [Servo](https://github.com/JackAtKitronik/Kitronik-Air-Quality-Control-HAT#servo)
<br/>

## BME688
The BME688 sensor allows us to measure temperature, humidity, pressure and gasses from our HAT. To do this we need to initialise the sensor and calculate the baseline values for the BME688 to use.
``` python
# Initialise the BME688 sensor
bme688 = KitronikBME688()
# Initialise the OLED display
oled = KitronikOLED()
# Calculate the baseline values for the BME688 sensor
bme688.calcBaselines(oled) # Takes OLED as input to show progress
```

When the baselines have been calculated we can then measure the quality of the air around the HAT. We first need to tell the BME688 to measure the air quality and then we can read individual values from the sensor.
``` python
# Update the sensor values
bme688.measureData()
# Read and output the sensor values
print("Temperature:", bme688.readTemperature())
print("Pressure:", bme688.readPressure())
print("Humidity:", bme688.readHumidity())
print("eCO2:", bme688.readeCO2())
print("Air Quality %:", bme688.getAirQualityPercent())
print("Air Quality Score:", bme688.getAirQualityScore())
```
<br/>

## OLED Display
The OLED Display allows us to display text, shapes and images on the screen of the HAT. We use this when calculating the baselines values for the BME688 sensor. To use the OLED display we first need to initialise it.
``` python
# Initialise the OLED display
oled = KitronikOLED()
```

To display text in the OLED screen we can use the `displayText` function. This function requires two inputs for the text to display and the line to display it on. Optionally, it also allows for an X offset to push the text away from the left.
``` python
# Write the following text on line 1 of the OLED display
oled.displayText("Hello dev :)", 1)
# Write the following text on line 2 of the OLED display
oled.displayText("Here again!", 2, 32) # With a 32 pixel margin at the start
```

When we tell the OLED screen to display this text, it doesn't actually update the screen. To update the screen after telling the OLED display to do anything, we need to use the `show` function. We can also tell the OLED display to remove everything we have drawn to the screen.
``` python
# Update the OLED display with the changes
oled.show()
# Remove everythig from the OLED display
oled.clear()
```

We can also draw shapes on the OLED display using the `drawRect` and `drawLine` functions. The `drawRect` function draws a rectangle on the screen and requires four inputs for the start X, start Y, width, and height of the rectangle. Optionally, it also allows use to fill the pixels inside of the rectangle as well as drawing the border. We also have the `drawLine` function which takes four inputs for the start X, start Y, end X, and end Y positions of the line we want to draw.
``` python
# Draw an empty rectangle on the OLED display
oled.drawRect(0, 0, 24, 24)
# Draw a filled rectangle on the OLED display
oled.drawRect(25, 0, 24, 24, fill = True)
# Draw a diagonal line across the OLED display
oled.drawLine(32, 32, 64, 64)
```
<br/>

## ZIPLEDs
The ZIPLEDs could be used to show status values on the HAT. Each LED is addressable on its own and use RGB values to set them. To start using the ZIPLEDs we need to initialise them. When initialising the LEDs we have one optional input value to determine whether we want the LEDs to automatically update when we change a value. By default the ZIPLEDs are set to auto show changes when they happen.
``` python
# Initialise the ZIPLEDs, with auto show turned off
zipLEDs = KitronikZIPLEDs(autoShow = False)
```

To update changes we have made to the LEDs values we can use the `show` function. This is only necessary if we have turned auto show off.
``` python
# Update the ZIPLEDs with the updated values
zipLEDs.show()
```

To set all of the ZIPLEDs to the same colour at once we can use the `fill` function. This function takes one input for the RGB colour we would like to set the LEDs to.
``` python
# Set all LEDs to pink
zipLEDs.fill((255, 0, 255))
```

To set each LED individually we can use the `setPixel` function which takes two inputs. The first input is the number of the LED we want to change and the second is the RGB colour we would like to set the LED to.
``` python
# Set the LED to red
zipLEDs.setPixel(0, (255, 0, 0))
# Set the LED to green
zipLEDs.setPixel(1, (0, 255, 0))
# Set the LED to blue
zipLEDs.setPixel(2, (0, 0, 255))
```

We can also change the brightness of the ZIPLEDs, allowing us to increase or decrease the LEDs whether they are being used inside or outside. We can do this using the `setBrightness` function which takes one input for the brightness value we would like to set the LEDs to.
``` python
# Set the ZIPLEDs to half brightness
zipLEDs.setBrightness(50)
```
<br/>

## Real Time Clock
On the HAT is a real time clock which we can use to set and read the time. Before using the real time clock we need to initialise it.
``` python
# Initialise the Real Time Clock
rtc = KitronikRTC()
```

To get the current time held by the real time clock we can use the `read` function. This function will return the current time as a string.
``` python
# Read and output the current time on the Real Time Clock
print("RTC READ:", rtc.read())
```

To update the current time held by the real time clock we use the `set` function. This function takes seven inputs. The first three are the year, month and day we want to set the clock at. The next is the day of the week for that day as a number with 0 being Sunday and 6 being Saturday. Then the last three inputs are the hour, minute and second we want to set the clock to.
``` python
# Update the current time on the Real Time Clock
rtc.set(2023, 1, 23, 1, 22, 20, 21)
```
<br/>

## ADC
On the HAT there are three ADC connections. To use each ADC connection we need to create an ADC object for each of them. The ADCs range from 0 to 2 and we use these numbers to specify which ADC we are initialising.
``` python
# Initialise the ADCs
adc0 = KitronikADC(0)
adc1 = KitronikADC(1)
adc2 = KitronikADC(2)
```

With our ADC objects initialised we can then read the current value at the ADC connection using the `read` function.
``` python
# Read and output the current ADC values
print("ADC0:", adc0.read())
print("ADC1:", adc1.read())
print("ADC2:", adc2.read())
```
<br/>

## Buzzer
The HAT has a buzzer which we can use to play tones. To use the buzzer we first need to initialise it.
``` python
# Initialise the Buzzer
buzzer = KitronikBuzzer()
```

To tell the buzzer when to play a tone we need to use the `start` function. Then to stop it playing the tone we can use the `stop` function.
``` python
# Start the Buzzer generating sound
buzzer.start()
# Stop the Buzzer generating sound
buzzer.stop()
```

We can change the tone the buzzer makes using the `changeTone` function. This function takes one input for the frequency of the tone we would like it to play. The frequency can be set between 1 and 3000 Hz.
``` python
# Change the sound of the Buzzer
buzzer.changeTone(440)
```
<br/>

## GPIO
On the HAT there are three GPIO connections. To use each GPIO connection we need to create an GPIO object for each of them. The GPIOs range from 22 to 24 and we use these numbers to specify which GPIO we are initialising. Optionally, we can also set the GPIO up using PWM.
``` python
# Initialise the GPIO
gpio22 = KitronikGPIO(22) # Without PWM
gpio23 = KitronikGPIO(23, isPWM = False) # Without PWM
gpio24 = KitronikGPIO(24, isPWM = True) # With PWM
```

For the GPIOs we have setup without PWM, we can turn them on using the `turnOn` function. We can also turn them off using the `turnOff` function.
``` python
# Turn on the 2 GPIOs
gpio22.turnOn()
gpio23.turnOn()
# Turn off the 2 GPIOs
gpio22.turnOff()
gpio23.turnOff()
```

For the GPIOs we have setup with PWM, we can tell the HAT to generate a PWM signal using the `start` function. We can then change the duty cycle of the PWM using the `changeDutyCycle` function with a value between 0 and 100. We can also change the frequency of the PWM using the `changeFrequency` function with a value between 1 and 3000 Hz. Finally, we can stop the PWM signal using the `stop` function.
``` python
# Turn on the PWM for the GPIO
gpio24.start()
# Set the GPIO PWM duty cycle at half
gpio24.changeDutyCycle(50)
# Turn off the PWM for the GPIO
gpio24.stop()
```
<br/>

## High Power Out
The HAT also has two high power out terminals. We can use each of these high power out connection by initialising them separately using `KitronikHighPowerOut`. We can then use the high power out objects using the same functions we lined out for the GPIO above.
``` python
# Initialise High Power Out 1 without PWM
hpo1 = KitronikHighPowerOut(1)
# Turn on High Power Out 1
hpo1.turnOn()
# Turn off High Power Out 1
hpo1.turnOff()

# Initialise High Power Out 2 with PWM
hpo2 = KitronikHighPowerOut(2, isPWM = True)
# Start the PWM output on High Power Out 2
hpo2.start()
# Set the High Power Out 2 PWM duty cycle at half
hpo2.changeDutyCycle(50)
# Stop the PWM output on High Power Out 2
hpo2.stop()
```
<br/>

## Servo
There is one servo connection on the HAT. To use the servo we first need to initialise it.
``` python
# Initialise the Servo
servo = KitronikServo()
```

To tell the servo connection when to generate the PWM signal we need to use the `start` function. Then to stop the PWM output we can use the `stop` function.
``` python
# Start the PWM output to the Servo
servo.start()
# Stop the PWM output to the Servo
servo.stop()
```

Moving the servo can be done using two functions. The `changePercent` function takes one input for the percent of the servo's range you would like to move it to. Then the `changeAngle` function takes the angle you would like to move the servo to as its input.
``` python
# Move the servo to half way (90 degrees)
servo.changePercent(50)
# Move the servo to half way (90 degrees)
servo.changeAngle(90)
```
