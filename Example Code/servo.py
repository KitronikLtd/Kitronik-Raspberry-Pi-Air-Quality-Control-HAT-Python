from time import sleep
from KitronikAirQualityControlHAT import *

print("Servo")
# Initialise the Servo
servo = KitronikServo()
# Start the PWM output to the Servo
servo.start()

while True:
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
    sleep(5)
