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