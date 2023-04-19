import math
import RPi.GPIO as GPIO
import serial
from PIL import Image, ImageDraw, ImageFont
from smbus import SMBus
from time import sleep

# Singleton to access the UART connection with the HAT
class KitronikSerial:
    def __new__(cls):
        # Check if singleton instance already exists
        if not hasattr(cls, 'instance'):
            # Create the singleton instance
            cls.instance = super(KitronikSerial, cls).__new__(cls)
        # Return the singleton instance
        return cls.instance

    def __init__(self):
        # Create the UART connection with the HAT
        self.ser = serial.Serial("/dev/serial0", baudrate=115200,
            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, timeout=1)

    def getSerial(self):
        return self.ser

# Class to communicate with the ADC on the HAT
class KitronikADC:
    def __init__(self, adcNumber):
        if adcNumber > 2: adcNumber = 2
        if adcNumber < 0: adcNumber = 0
        self.adcNumber = adcNumber + 1
        # Increment for communication with HAT, can't send a request of zero
        s = KitronikSerial()
        self.ser = s.getSerial()

    # Ask the HAT for the current ADC value
    def read(self):
        req = [self.adcNumber, 0, 0, 0, 0, 0, 0, 0, 0, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        try:
            temp = int(response[2:len(response) - 3])
        except:
            temp = self.read()
        return temp

# Class to communicate with the Real Time Clock on the HAT
class KitronikRTC:
    def __init__(self):
        s = KitronikSerial()
        self.ser = s.getSerial()

    # Ask the HAT for the current Real Time Clock value
    def read(self):
        req = [5, 0, 0, 0, 0, 0, 0, 0, 0, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        while len(response) < 24:
            self.ser.write(request)
            response = str(self.ser.readline())
        return response[2:len(response) - 3]

    # Ask the HAT to update the Real Time Clock value
    def set(self, year, month, day, dayOfWeek, hour, minute, second):
        req = [6, (year >> 8) & 0xff, year & 0xff, month, day, dayOfWeek, hour, minute, second, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        while response != str(b'RTC SET DONE\n'):
            self.ser.write(request)
            response = str(self.ser.readline())

# Class to communicate with the ZIPLEDs on the HAT
class KitronikZIPLEDs:
    def __init__(self, autoShow = True):
        s = KitronikSerial()
        self.ser = s.getSerial()
        self.autoShow = autoShow

    # Ask the HAT to update the ZIPLEDs brightness
    def setBrightness(self, brightness):
        if brightness < 0: brightness = 0
        if brightness > 100: brightness = 100
        req = [7, brightness, 0, 0, 0, 0, 0, 0, 0, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        while response != str(b'LEDS BRIGHTNESS SET DONE\n'):
            self.ser.write(request)
            response = str(self.ser.readline())

    # Ask the HAT to show the updated ZIPLED values
    def show(self):
        req = [8, 0, 0, 0, 0, 0, 0, 0, 0, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        while response != str(b'LEDS SHOW DONE\n'):
            self.ser.write(request)
            response = str(self.ser.readline())

    # Ask the HAT to update a ZIPLED value
    def setPixel(self, pixelNumber, colour):
        r = colour[0]
        g = colour[1]
        b = colour[2]
        if pixelNumber < 0: pixelNumber = 0
        if pixelNumber > 2: pixelNumber = 2
        if r < 0: r = 0
        if r > 255: r = 255
        if g < 0: g = 0
        if g > 255: g = 255
        if b < 0: b = 0
        if b > 255: b = 255
        req = [9, pixelNumber, r, g, b, 0, 0, 0, 0, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        while response != str(b'LED PIXEL SET DONE\n'):
            self.ser.write(request)
            response = str(self.ser.readline())
        if self.autoShow:
             self.show()

    # Ask the HAT to update the ZIPLEDs values
    def fill(self, colour):
        r = colour[0]
        g = colour[1]
        b = colour[2]
        if r < 0: r = 0
        if r > 255: r = 255
        if g < 0: g = 0
        if g > 255: g = 255
        if b < 0: b = 0
        if b > 255: b = 255
        req = [10, r, g, b, 0, 0, 0, 0, 0, 255]
        request = bytearray(req)
        self.ser.write(request)
        response = str(self.ser.readline())
        while response != str(b'LEDS FILL DONE\n'):
            self.ser.write(request)
            response = str(self.ser.readline())
        if self.autoShow:
             self.show()

# Class to control the Buzzer on the HAT
class KitronikBuzzer:
    def __init__(self):
        buzzerPin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(buzzerPin, GPIO.OUT)
        self.buzzer = GPIO.PWM(buzzerPin, 440)

    # Update the tone output by the Buzzer
    def changeTone(self, frequency):
        if frequency > 3000: frequency = 3000
        if frequency < 1: frequency = 1
        self.buzzer.ChangeFrequency(frequency)

    # Start the buzzer generating the tone
    def start(self):
        self.buzzer.start(10)

    # Stop the buzzer generating the tone
    def stop(self):
        self.buzzer.stop()

# Class to control the GPIO on the HAT
class KitronikGPIO:
    def __init__(self, gpioNumber, isPWM = False):
        if gpioNumber not in [13, 19, 22, 23, 24]:
            gpioNumber = 22
        self.gpioNumber = gpioNumber
        self.isPWM = isPWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(gpioNumber, GPIO.OUT)
        # Optionally use the GPIO as PWM
        if isPWM:
            self.gpio = GPIO.PWM(gpioNumber, 500)
            self.dutyCycle = 10

    # Turn the GPIO on, when not in PWM mode
    def turnOn(self):
        if self.isPWM: return
        GPIO.output(self.gpioNumber, GPIO.HIGH)

    # Turn the GPIO off, when not in PWM mode
    def turnOff(self):
        if self.isPWM: return
        GPIO.output(self.gpioNumber, GPIO.LOW)

    # Update the frequency output by the GPIO, when in PWM mode
    def changeFrequency(self, frequency):
        if not self.isPWM: return
        if frequency > 3000: frequency = 3000
        if frequency < 1: frequency = 1
        self.gpio.ChangeFrequency(frequency)

    # Update the duty cycle output by the GPIO, when in PWM mode
    def changeDutyCycle(self, dutyCycle):
        if not self.isPWM: return
        if dutyCycle > 100: dutyCycle = 100
        if dutyCycle < 0: dutyCycle = 0
        self.dutyCycle = dutyCycle
        self.gpio.ChangeDutyCycle(dutyCycle)

    # Start the GPIO generating the PWM
    def start(self):
        if not self.isPWM: return
        self.gpio.start(self.dutyCycle)

    # Stop the GPIO generating the PWM
    def stop(self):
        if not self.isPWM: return
        self.gpio.stop()

# Class to control the High Power Out on the HAT
# Is a subclass of KitronikGPIO, uses the same functions
class KitronikHighPowerOut(KitronikGPIO):
    def __init__(self, hpoNumber, isPWM = False):
        gpioNumber = 13
        if hpoNumber == 2: gpioNumber = 19
        KitronikGPIO.__init__(self, gpioNumber, isPWM = isPWM)

# Class to control the Servo on the HAT
class KitronikServo:
    def __init__(self):
        servoPin = 6
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(servoPin, GPIO.OUT)
        self.servo = GPIO.PWM(servoPin, 50)
        self.dutyCycle = 2.5

    # Update the duty cycle output to the Servo
    def changeDutyCycle(self, dutyCycle):
        if dutyCycle > 12.5: dutyCycle = 12.5
        if dutyCycle < 2.5: dutyCycle = 2.5
        self.dutyCycle = dutyCycle
        self.servo.ChangeDutyCycle(dutyCycle)

    # Start the Servo PWM
    def start(self):
        self.servo.start(self.dutyCycle)

    # Stop the Servo PWM
    def stop(self):
        self.servo.stop()

    # Update the percent the Servo is set to between 0 and 100
    def changePercent(self, percent):
        if percent > 100: percent = 100
        if percent < 0: percent = 0
        self.changeDutyCycle(2.5 + (percent / 10))

    # Update the angle the Servo is set to between 0 and 180
    def changeAngle(self, angle):
        if angle > 180: angle = 180
        if angle < 0: angle = 0
        self.changePercent(angle / 1.8)

# Class to control the OLED display on the HAT
class KitronikOLED():
    # Runs on initialisation of the class
    # Sets up all the register definitions and global variables
    def __init__(self, flipScreen=False):
        self.width = 128
        self.height = 64
        self.external_vcc = False
        self.pages = 8
        self.buffer = [0] * (self.width * self.pages)
        self.i2c_address = 0x3C
        self.i2c = SMBus(1)

        self.plotArray = []
        self.plotYMin = 0
        self.plotYMax = 100
        self.yPixelMin = 63
        self.yPixelMax = 12

        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

        # register definitions
        self.SET_CONTRAST = 0x81
        self.SET_ENTIRE_ON = 0xA4
        self.SET_NORM_INV = 0xA6
        self.SET_DISP = 0xAE
        self.SET_MEM_ADDR = 0x20
        self.SET_COL_ADDR = 0x21
        self.SET_PAGE_ADDR = 0x22
        self.SET_DISP_START_LINE = 0x40
        if flipScreen:
            self.SET_SEG_REMAP = 0xA0
            self.SET_COM_OUT_DIR = 0xC0
        else:
            self.SET_SEG_REMAP = 0xA1
            self.SET_COM_OUT_DIR = 0xC8
        self.SET_MUX_RATIO = 0xA8
        self.SET_DISP_OFFSET = 0xD3
        self.SET_COM_PIN_CFG = 0xDA
        self.SET_DISP_CLK_DIV = 0xD5
        self.SET_PRECHARGE = 0xD9
        self.SET_VCOM_DESEL = 0xDB
        self.SET_CHARGE_PUMP = 0x8D

        self.init_display()

    # Write commands to the OLED controller
    def write_cmd(self, cmd):
        self.i2c.write_byte_data(self.i2c_address, 0x00, cmd)

    # Write data to the OLED controller
    def write_data(self, data):
        self.i2c.write_byte_data(self.i2c_address, 0x40, data)

    # Initialise the display settings and start the display clear
    def init_display(self):
        for cmd in (
            self.SET_DISP | 0x00,  # off
            # address setting
            self.SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            self.SET_DISP_START_LINE | 0x00,
            self.SET_SEG_REMAP,# | 0x01,  # Set to either 0xA0 or A1, flips screen horizontally
            self.SET_MUX_RATIO,
            self.height - 1,
            self.SET_COM_OUT_DIR, #| 0x08, # Set to either 0xC0 or 0xC8, flips screen vertically
            self.SET_DISP_OFFSET,
            0x00,
            self.SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            self.SET_DISP_CLK_DIV,
            0x80,
            self.SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            self.SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            self.SET_CONTRAST,
            0xFF,  # maximum
            self.SET_ENTIRE_ON,  # output follows RAM contents
            self.SET_NORM_INV,  # not inverted
            # charge pump
            self.SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            self.SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.clear()
        self.show()

    # Screen will switch off, but retain the information that was displayed
    def poweroff(self):
        self.write_cmd(self.SET_DISP | 0x00)

    # Turn the screen back on - do not need to re-display what was showing as the information is retained
    def poweron(self):
        self.write_cmd(self.SET_DISP | 0x01)

    # 0 = Dim to 150 = Bright
    def contrast(self, contrast):
        self.write_cmd(self.SET_CONTRAST)
        self.write_cmd(contrast)

    # 0 = White on black, 1 = Black on white
    def invert(self, invert):
        self.write_cmd(self.SET_NORM_INV | (invert & 1))

    # Set text to display on a particular line (1 - 6) and an x-axis offset can be set (0 - 127, 0 is default)
    # If the text is longer than than the screen it will be cut off, it will not be pushed to the next line (16 characters max per line)
    # Need to call 'show()' to make the text actually display
    def displayText(self, text, line, x_offset = 0):
        if line < 1: line = 1
        if line > 6: line = 6
        y = (line * 11) - 10
        (font_width, font_height) = self.font.getsize(text)
        self.draw.text((x_offset, y), text, font = self.font, fill = 1)

    # Make what has been set to display actually appear on the screen
    # Needs to be called after 'displayText()', 'plot()', clear()', 'drawLine()' & 'drawRect()'
    def show(self):
        # Load the pixels stored in the image
        pixels = self.image.load()
        # Iterate through the memory pages
        index = 0
        for page in range(self.pages):
            # Iterate through all x axis columns.
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                bits = 0
                # Don't use range here as it's a bit slow
                for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                    bits = bits << 1
                    bits |= 0 if pixels[(x, page * 8 + 7 - bit)] == 0 else 1
                # Update buffer byte and increment to next byte.
                self.buffer[index] = bits
                index += 1

        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(self.SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(self.SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        for i in range(len(self.buffer)):
            self.write_data(self.buffer[i])


    # Plot a live updating graph of a variable
    # Plot y range is pixels 12 down to 63, leaving room for a title or similar on the first line
    # Need to call 'show()' to make the plot actually display
    def plot(self, variable):
        variable = math.trunc(variable)

        if (variable > self.plotYMax):
            self.plotYMax = variable
        if (variable < self.plotYMin):
            self.plotYMin = variable

        entries = len(self.plotArray)
        if (entries >= 128):
            prevX = 0
            prevY = self.plotArray[127]
            self.plotArray.pop(0)
            self.plotArray.append(variable)
        else:
            self.plotArray.append(variable)
            prevX = len(self.plotArray) - 1
            prevY = self.plotArray[prevX]

        for entry in range(entries):
            x = entry
            y = self.plotArray[entry]
            y = math.trunc(self.yPixelMin - (y * ((self.yPixelMin - self.yPixelMax) / (self.plotYMax - self.plotYMin))))
            if (x == 0):
                super().pixel(x, y, 1)
            else:
                self.drawLine(prevX, prevY, x, y)
            prevX = x 
            prevY = y

    # Wipe all data from the screen
    # Need to call 'show()' to make the clear actually happen
    def clear(self):
        self.buffer = [0] * (self.width * self.pages)
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    # Clear a specific line on the screen
    def clearLine(self, line):
        y = (line - 1) + ((line * 10) - 10)
        self.draw.rectangle((0, y, 128, y + 10), outline = 0, fill = 0)

    # Draw a line on the screen (vertical, horizontal or diagonal), setting start and finish (x, y) coordinates
    # Need to call 'show()' to make the line actually display    
    def drawLine(self, start_x, start_y, end_x, end_y):
        self.draw.line((start_x, start_y, end_x, end_y), fill = 1)

    # Draw rectangles with a top left starting (x, y) coordinate and then a width and height
    # Can be filled (True) or just an outline (False)
    # Need to call 'show()' to make the rectangle actually display
    def drawRect(self, start_x, start_y, width, height, fill=False):
        fill_value = 1
        if (fill == False): fill_value = 0
        self.draw.rectangle((start_x, start_y, start_x + width, start_y + height), outline = 1, fill = fill_value)

# Class to control the BME688 sensor on the HAT
class KitronikBME688:
    # The following functions are for reading the registers on the BME688
    # Function for reading register as signed 8 bit integer
    def getUInt8(self, reg):
        #return int.from_bytes(self.i2c.readfrom_mem(self.CHIP_ADDRESS, reg, 1), "big")
        return self.i2c.read_byte_data(self.CHIP_ADDRESS, reg)
    
    # Function to convert unsigned ints to twos complement signed ints
    def twosComp(self, value, bits):
        if ((value & (1 << (bits - 1))) != 0):
            value = value - (1 << bits)
        return value

    # Function for proportionally mapping a value to a different value range
    def mapValues(self, value, frMin, frMax, toMin, toMax):
        toRange = toMax - toMin
        mappedVal = toMin + ((value - frMin) * ((toMax - toMin) / (frMax - frMin)))
        return mappedVal

    def __init__(self):
        self.CHIP_ADDRESS = 0x77    # I2C address as determined by hardware configuration
        self.i2c = SMBus(1)

        # Useful BME688 Register Addresses
        # Control
        self.CTRL_MEAS = 0x74       # Bit position <7:5>: Temperature oversampling   Bit position <4:2>: Pressure oversampling   Bit position <1:0>: Sensor power mode
        self.RESET = 0xE0           # Write 0xB6 to initiate soft-reset (same effect as power-on reset)
        self.CHIP_ID = 0xD0         # Read this to return the chip ID: 0x61 - good way to check communication is occurring
        self.CTRL_HUM = 0x72        # Bit position <2:0>: Humidity oversampling settings
        self.CONFIG = 0x75          # Bit position <4:2>: IIR filter settings
        self.CTRL_GAS_0 = 0x70      # Bit position <3>: Heater off (set to '1' to turn off current injection)
        self.CTRL_GAS_1 = 0x71      # Bit position <5> DATASHEET ERROR: Enable gas conversions to start when set to '1'   Bit position <3:0>: Heater step selection (0 to 9)

        # Pressure Data
        self.PRESS_MSB_0 = 0x1F     # Forced & Parallel: MSB [19:12]
        self.PRESS_LSB_0 = 0x20     # Forced & Parallel: LSB [11:4]
        self.PRESS_XLSB_0 = 0x21    # Forced & Parallel: XLSB [3:0]

        # Temperature Data
        self.TEMP_MSB_0 = 0x22      # Forced & Parallel: MSB [19:12]
        self.TEMP_LSB_0 = 0x23      # Forced & Parallel: LSB [11:4]
        self.TEMP_XLSB_0 = 0x24     # Forced & Parallel: XLSB [3:0]

        # Humidity Data
        self.HUMID_MSB_0 = 0x25     # Forced & Parallel: MSB [15:8]
        self.HUMID_LSB_0 = 0x26     # Forced & Parallel: LSB [7:0]

        # Gas Resistance Data
        self.GAS_RES_MSB_0 = 0x2C   # Forced & Parallel: MSB [9:2]
        self.GAS_RES_LSB_0 = 0x2D   # Forced & Parallel: Bit <7:6>: LSB [1:0]    Bit <5>: Gas valid    Bit <4>: Heater stability    Bit <3:0>: Gas resistance range

        # Status
        self.MEAS_STATUS_0 = 0x1D   # Forced & Parallel: Bit <7>: New data    Bit <6>: Gas measuring    Bit <5>: Measuring    Bit <3:0>: Gas measurement index

        # Calibration parameters for compensation calculations
        # Temperature
        self.PAR_T1 = self.twosComp((self.getUInt8(0xEA) << 8) | self.getUInt8(0xE9), 16)      # Signed 16-bit
        self.PAR_T2 = self.twosComp((self.getUInt8(0x8B) << 8) | self.getUInt8(0x8A), 16)      # Signed 16-bit
        self.PAR_T3 = self.twosComp(self.getUInt8(0x8C), 8)           # Signed 8-bit

        # Pressure
        self.PAR_P1 = (self.getUInt8(0x8F) << 8) | self.getUInt8(0x8E)   # Always a positive number, do not do twosComp() conversion!
        self.PAR_P2 = self.twosComp((self.getUInt8(0x91) << 8) | self.getUInt8(0x90), 16)      # Signed 16-bit
        self.PAR_P3 = self.twosComp(self.getUInt8(0x92), 8)                                 # Signed 8-bit
        self.PAR_P4 = self.twosComp((self.getUInt8(0x95) << 8) | self.getUInt8(0x94), 16)      # Signed 16-bit
        self.PAR_P5 = self.twosComp((self.getUInt8(0x97) << 8) | self.getUInt8(0x96), 16)      # Signed 16-bit
        self.PAR_P6 = self.twosComp(self.getUInt8(0x99), 8)                                 # Signed 8-bit
        self.PAR_P7 = self.twosComp(self.getUInt8(0x98), 8)                                 # Signed 8-bit
        self.PAR_P8 = self.twosComp((self.getUInt8(0x9D) << 8) | self.getUInt8(0x9C), 16)      # Signed 16-bit
        self.PAR_P9 = self.twosComp((self.getUInt8(0x9F) << 8) | self.getUInt8(0x9E), 16)      # Signed 16-bit
        self.PAR_P10 = self.twosComp(self.getUInt8(0xA0), 8)                                # Signed 8-bit

        # Humidity
        parH1_LSB_parH2_LSB = self.getUInt8(0xE2)
        self.PAR_H1 = (self.getUInt8(0xE3) << 4) | (parH1_LSB_parH2_LSB & 0x0F)
        self.PAR_H2 = (self.getUInt8(0xE1) << 4) | (parH1_LSB_parH2_LSB >> 4)
        self.PAR_H3 = self.twosComp(self.getUInt8(0xE4), 8)                                 # Signed 8-bit
        self.PAR_H4 = self.twosComp(self.getUInt8(0xE5), 8)                                 # Signed 8-bit
        self.PAR_H5 = self.twosComp(self.getUInt8(0xE6), 8)                                 # Signed 8-bit
        self.PAR_H6 = self.twosComp(self.getUInt8(0xE7), 8)                                 # Signed 8-bit
        self.PAR_H7 = self.twosComp(self.getUInt8(0xE8), 8)                                 # Signed 8-bit

        # Gas resistance
        self.PAR_G1 = self.twosComp(self.getUInt8(0xED), 8)                                 # Signed 8-bit
        self.PAR_G2 = self.twosComp((self.getUInt8(0xEB) << 8) | self.getUInt8(0xEC), 16)      # Signed 16-bit
        self.PAR_G3 = self.getUInt8(0xEE)                                # Unsigned 8-bit
        self.RES_HEAT_RANGE = (self.getUInt8(0x02) >> 4) & 0x03
        self.RES_HEAT_VAL = self.twosComp(self.getUInt8(0x00), 8)              # Signed 8-bit

        # Oversampling rate constants
        self.OSRS_1X = 0x01
        self.OSRS_2X = 0x02
        self.OSRS_4X = 0x03
        self.OSRS_8X = 0x04
        self.OSRS_16X = 0x05

        # IIR filter coefficient values
        self.IIR_0 = 0x00
        self.IIR_1 = 0x01
        self.IIR_3 = 0x02
        self.IIR_7 = 0x03
        self.IIR_15 = 0x04
        self.IIR_31 = 0x05
        self.IIR_63 = 0x06
        self.IIR_127 = 0x07

        #Global variables used for storing one copy of value, these are used in multiple locations for calculations
        self.bme688InitFlag = False
        self.gasInit = False

        self.tRead = 0       # calculated readings of sensor parameters from raw adc readings
        self.pRead = 0
        self.hRead = 0
        self.gRes = 0
        self.iaqPercent = 0
        self.iaqScore = 0
        self.airQualityRating = ""
        self.eCO2Value = 0

        self.gBase = 0
        self.hBase = 40        # Between 30% & 50% is a widely recognised optimal indoor humidity, 40% is a good middle ground
        self.hWeight = 0.25     # Humidity contributes 25% to the IAQ score, gas resistance is 75%
        self.hPrev = 0
        self.measTime = 0
        self.measTimePrev = 0

        self.tRaw = 0    # adc reading of raw temperature
        self.pRaw = 0       # adc reading of raw pressure
        self.hRaw = 0       # adc reading of raw humidity
        self.gResRaw = 0  # adc reading of raw gas resistance
        self.gasRange = 0

        self.t_fine = 0                          # Intermediate temperature value used for pressure calculation
        self.newAmbTemp = 0
        self.tAmbient = 0       # Intermediate temperature value used for heater calculation
        self.ambTempFlag = False

        # Create an instance of the OLED display screen for use during setup and for error messages
        #self.screen = KitronikOLED()

        # Begin the hardware inititialisation for the BME688 sensor
        self.bme688Init()

    # Temperature compensation calculation: rawADC to degrees C (integer)
    def calcTemperature(self, tempADC):
        var1 = (tempADC >> 3) - (self.PAR_T1 << 1)
        var2 = (var1 * self.PAR_T2) >> 11
        var3 = ((((var1 >> 1) * (var1 >> 1)) >> 12) * (self.PAR_T3 << 4)) >> 14
        self.t_fine = var2 + var3
        self.newAmbTemp = ((self.t_fine * 5) + 128) >> 8
        self.tRead = self.newAmbTemp / 100     # Convert to floating point with 2 dp
        if (self.ambTempFlag == False):
            self.tAmbient = self.newAmbTemp

    # Pressure compensation calculation: rawADC to Pascals (integer)
    def intCalcPressure(self, pressureADC):
        var1 = (self.t_fine >> 1) - 64000
        var2 = ((((var1 >> 2) * (var1 >> 2)) >> 11) * self.PAR_P6) >> 2
        var2 = var2 + ((var1 * self.PAR_P5) << 1)
        var2 = (var2 >> 2) + (self.PAR_P4 << 16)
        var1 = (((((var1 >> 2) * (var1 >> 2)) >> 13) * (self.PAR_P3 << 5)) >> 3) + ((self.PAR_P2 * var1) >> 1)
        var1 = var1 >> 18
        var1 = ((32768 + var1) * self.PAR_P1) >> 15
        self.pRead = 1048576 - pressureADC
        self.pRead = ((self.pRead - (var2 >> 12)) * 3125)

        if (self.pRead >= (1 << 30)):
            self.pRead = (self.pRead // var1) << 1
        else:
            self.pRead = ((self.pRead << 1) // var1)

        var1 = (self.PAR_P9 * (((self.pRead >> 3) * (self.pRead >> 3)) >> 13)) >> 12
        var2 = ((self.pRead >> 2) * self.PAR_P8) >> 13
        var3 = ((self.pRead >> 8) * (self.pRead >> 8) * (self.pRead >> 8) * self.PAR_P10) >> 17
        self.pRead = self.pRead + ((var1 + var2 + var3 + (self.PAR_P7 << 7)) >> 4)

    # Humidity compensation calculation: rawADC to % (integer)
    # 'tempScaled' is the current reading from the Temperature sensor
    def intCalcHumidity(self, humidADC, tempScaled):
        self.hPrev = self.hRead
        tempScaled = math.trunc(tempScaled)
        
        var1 = humidADC - (self.PAR_H1 << 4) - (((tempScaled * self.PAR_H3) // 100) >> 1)
        var2 = (self.PAR_H2 * (((tempScaled * self.PAR_H4) // 100) + (((tempScaled * ((tempScaled * self.PAR_H5) // 100)) >> 6) // 100) + (1 << 14))) >> 10
        var3 = var1 * var2
        var4 = ((self.PAR_H6 << 7) + ((tempScaled * self.PAR_H7) // 100)) >> 4
        var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
        var6 = (var4 * var5) >> 1
        self.hRead = (var3 + var6) >> 12
        self.hRead = (((var3 + var6) >> 10) * (1000)) >> 12
        self.hRead = self.hRead // 1000

    # Gas sensor heater target temperature to target resistance calculation
    # 'ambientTemp' is reading from Temperature sensor in degC (could be averaged over a day when there is enough data?)
    # 'targetTemp' is the desired temperature of the hot plate in degC (in range 200 to 400)
    # Note: Heating duration also needs to be specified for each heating step in 'gas_wait' registers
    def intConvertGasTargetTemp(self, ambientTemp, targetTemp):
        var1 = ((ambientTemp * self.PAR_G3) // 1000) << 8    # Divide by 1000 as we have ambientTemp in pre-degC format (i.e. 2500 rather than 25.00 degC)
        var2 = (self.PAR_G1 + 784) * (((((self.PAR_G2 + 154009) * targetTemp * 5) // 100) + 3276800) // 10)
        var3 = var1 + (var2 >> 1)
        var4 = (var3 // (self.RES_HEAT_RANGE + 4))
        var5 = (131 * self.RES_HEAT_VAL) + 65536                 # Target heater resistance in Ohms
        resHeatX100 = (((var4 // var5) - 250) * 34)
        resHeat = ((resHeatX100 + 50) // 100)

        return resHeat

    # Gas resistance compensation calculation: rawADC & range to Ohms (integer)
    def intCalcgRes(self, gasADC, gasRange):
        var1 = 262144 >> gasRange
        var2 = gasADC - 512
        var2 = var2 * 3
        var2 = 4096 + var2
        calcGasRes = ((10000 * var1) // var2)
        self.gRes = calcGasRes * 100

    # Initialise the BME688, establishing communication, entering initial T, P & H oversampling rates, setup filter and do a first data reading (won't return gas)
    def bme688Init(self):
        # Establish communication with BME688
        #chipID = self.i2c.readfrom_mem(self.CHIP_ADDRESS, self.CHIP_ID, 1)
        #chipID = int.from_bytes(chipID, "big")
        chipID = self.i2c.read_byte_data(self.CHIP_ADDRESS, self.CHIP_ID)
        while (chipID != 97):
            #chipID = self.i2c.readfrom_mem(self.CHIP_ADDRESS, self.CHIP_ID, 1)
            chipID = self.i2c.read_byte_data(self.CHIP_ADDRESS, self.CHIP_ID)
        # Do a soft reset
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.RESET, "\xB6")
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.RESET, 0xB6)
        sleep(1)
        # Set mode to SLEEP MODE: CTRL_MEAS reg <1:0>
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CTRL_MEAS, "\x00")
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CTRL_MEAS, 0x00)
        # Set the oversampling rates for Temperature, Pressure and Humidity
        # Humidity: CTRL_HUM bits <2:0>
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CTRL_HUM, str(self.OSRS_2X))
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CTRL_HUM, self.OSRS_2X)
        # Temperature: CTRL_MEAS bits <7:5>     Pressure: CTRL_MEAS bits <4:2>    (Combine and write both in one command)
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CTRL_MEAS, str(((self.OSRS_2X << 5) | (self.OSRS_16X << 2))))
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CTRL_MEAS, ((self.OSRS_2X << 5) | (self.OSRS_16X << 2)))
        
        # IIR Filter: CONFIG bits <4:2>
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CONFIG, str(self.IIR_3 << 2))
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CONFIG, self.IIR_3 << 2)
        
        # Enable gas conversion: CTRL_GAS_1 bit <5>    (although datasheet says <4> - not sure what's going on here...)
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CTRL_GAS_1, "\x20")
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CTRL_GAS_1, 0x20)
        self.bme688InitFlag = True

        # Do an initial data read (will only return temperature, pressure and humidity as no gas sensor parameters have been set)
        self.measureData()

    # Setup the gas sensor (defaults are 300°C and 180ms).
    # targetTemp is the target temperature for the gas sensor plate to reach (200 - 400°C), eg: 300
    # heatDuration is the length of time for the heater to be turned on (0 - 4032ms), eg: 180
    # WARNING: The temperature and duration values can be changed but this is not recommended unless the user is familiar with gas sensor setup
    # The default values have been chosen as they provide a good all-round sensor response for air quality purposes
    def setupGasSensor(self, targetTemp=300, heatDuration=180):
        if (self.bme688InitFlag == False):
            self.bme688Init()

        # Limit targetTemp between 200°C & 400°C
        if (targetTemp < 200):
            targetTemp = 200
        elif (targetTemp > 400):
            targetTemp = 400

        # Limit heatDuration between 0ms and 4032ms
        if (heatDuration < 0):
            heatDuration = 0
        elif (heatDuration > 4032):
            heatDuration = 4032

        # Define the target heater resistance from temperature
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, 0x5A, self.intConvertGasTargetTemp(self.tAmbient, targetTemp).to_bytes(1, 'big'))   # res_wait_0 register - heater step 0
        self.i2c.write_byte_data(self.CHIP_ADDRESS, 0x5A, self.intConvertGasTargetTemp(self.tAmbient, targetTemp))
        
        # Define the heater on time, converting ms to register code (Heater Step 0) - cannot be greater than 4032ms
        # Bits <7:6> are a multiplier (1, 4, 16 or 64 times)    Bits <5:0> are 1ms steps (0 to 63ms)
        codedDuration = 0
        if (heatDuration < 4032):
            factor = 0
            while (heatDuration > 63):
                heatDuration = (heatDuration // 4)
                factor = factor + 1

            codedDuration = heatDuration + (factor * 64)
        else:
            codedDuration = 255

        #self.i2c.writeto_mem(self.CHIP_ADDRESS, 0x64, codedDuration.to_bytes(1, 'big'))     # gas_wait_0 register - heater step 0
        self.i2c.write_byte_data(self.CHIP_ADDRESS, 0x64, codedDuration)
        
        # Select index of heater step (0 to 9): CTRL_GAS_1 reg <3:0>    (Make sure to combine with gas enable setting already there)
        gasEnable = self.getUInt8(self.CTRL_GAS_1) & 0x20
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CTRL_GAS_1, (0x00 | gasEnable).to_bytes(1, 'big'))   # Select heater step 0
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CTRL_GAS_1, (0x00 | gasEnable))

        self.gasInit = True

    # Run all measurements on the BME688: Temperature, Pressure, Humidity & Gas Resistance.
    def measureData(self):
        if (self.bme688InitFlag == False):
            self.bme688Init()

        #self.measTimePrev = self.measTime       # Store previous measurement time (ms since micro:bit powered on)

        # Set mode to FORCED MODE to begin single read cycle: CTRL_MEAS reg <1:0>    (Make sure to combine with temp/pressure oversampling settings already there)
        oSampleTP = self.getUInt8(self.CTRL_MEAS)
        #self.i2c.writeto_mem(self.CHIP_ADDRESS, self.CTRL_MEAS, str((0x01 | oSampleTP)))
        self.i2c.write_byte_data(self.CHIP_ADDRESS, self.CTRL_MEAS, (0x01 | oSampleTP))
        
        # Check New Data bit to see if values have been measured: MEAS_STATUS_0 bit <7>
        newData = (self.getUInt8(self.MEAS_STATUS_0) & 0x80) >> 7
        while (newData != 1):
            newData = (self.getUInt8(self.MEAS_STATUS_0) & 0x80) >> 7

        # Check Heater Stability Status bit to see if gas values have been measured: <4> (heater stability)
        heaterStable = (self.getUInt8(self.GAS_RES_LSB_0) & 0x10) >> 4

        # If there is new data, read temperature ADC registers(this is required for all other calculations)        
        self.tRaw = (self.getUInt8(self.TEMP_MSB_0) << 12) | (self.getUInt8(self.TEMP_LSB_0) << 4) | (self.getUInt8(self.TEMP_XLSB_0) >> 4)

        # Read pressure ADC registers
        self.pRaw = (self.getUInt8(self.PRESS_MSB_0) << 12) | (self.getUInt8(self.PRESS_LSB_0) << 4) | (self.getUInt8(self.PRESS_XLSB_0) >> 4)

        # Read humidity ADC registers
        self.hRaw = (self.getUInt8(self.HUMID_MSB_0) << 8) | (self.getUInt8(self.HUMID_LSB_0) >> 4)
        
        # Read gas resistance ADC registers
        self.gResRaw = (self.getUInt8(self.GAS_RES_MSB_0) << 2) | self.getUInt8(self.GAS_RES_LSB_0) >> 6           # Shift bits <7:6> right to get LSB for gas resistance

        gasRange = self.getUInt8(self.GAS_RES_LSB_0) & 0x0F

        #self.measTime = ticks_ms()  # Capture latest measurement time (ms since Pico powered on)

        # Calculate the compensated reading values from the the raw ADC data
        self.calcTemperature(self.tRaw)
        self.intCalcPressure(self.pRaw)
        self.intCalcHumidity(self.hRaw, self.tRead)
        self.intCalcgRes(self.gResRaw, gasRange)

    # A baseline gas resistance is required for the IAQ calculation - it should be taken in a well ventilated area without obvious air pollutants
    # Take 60 readings over a ~5min period and find the mean
    # Establish the baseline gas resistance reading and the ambient temperature.
    # These values are required for air quality calculations
    # When the baseline process is complete, values for gBase and tAmbient are stored in a file
    # On subsequent power cycles of the board, this function will look for that file and take the baseline values stored there
    # To force the baselines process to be run again, call the function like this: calcBaselines(True)
    def calcBaselines(self, screen, forcedRun=False):
        if (self.bme688InitFlag == False):
            self.bme688Init()
        if (self.gasInit == False):
            self.setupGasSensor()

        screen.clear()
        screen.displayText("Setting Baseline", 2)
        screen.show()
        
        try: # Look for a 'baselines.txt' file existing - if it does, take the baseline values from there (unless 'forcedRun' is set to True)
            if not forcedRun:
                f = open("baselines.txt", "r")
                self.gBase = float(f.readline())
                self.tAmbient = float(f.readline())
            else:
                raise Exception("RUNNING BASELINE PROCESS")
        except: # If there is no file, an exception is raised, and the baseline process will be carried out (creating a new file at the end)
            self.ambTempFlag = False

            burnInReadings = 0
            burnInData = 0
            ambTotal = 0
            progress = 0
            while (burnInReadings < 60):               # Measure data and continue summing gas resistance until 60 readings have been taken
                progress = math.trunc((burnInReadings / 60) * 100)
                screen.clear()
                screen.displayText(str(progress) + "%", 4, 50)
                screen.displayText("Setting Baseline", 2)
                screen.show()
                self.measureData()
                burnInData = burnInData + self.gRes
                ambTotal = ambTotal + self.newAmbTemp
                sleep(5)
                burnInReadings = burnInReadings + 1

            self.gBase = (burnInData / 60)             # Find the mean gas resistance during the period to form the baseline
            self.tAmbient = (ambTotal / 60)            # Calculate the ambient temperature as the mean of the 60 initial readings

            # Save baseline values to a file
            f = open("baselines.txt", "w") #open in write - creates if not existing, will overwrite if it does
            f.write(str(self.gBase) + "\r\n")
            f.write(str(self.tAmbient) + "\r\n")
            f.close()
            
            self.ambTempFlag = True
        
        screen.clear()
        screen.displayText("Setup Complete!", 2)
        screen.show()
        sleep(2)
        screen.clear()
        screen.show()

    # Read Temperature from sensor as a Number.
    # Units for temperature are in °C (Celsius) or °F (Fahrenheit) according to selection.
    def readTemperature(self, temperature_unit="C"):
        temperature = self.tRead
        # Change temperature from °C to °F if user selection requires it
        if (temperature_unit == "F"):
            temperature = ((temperature * 18) + 320) / 10

        return temperature

    # Read Pressure from sensor as a Number.
    # Units for pressure are in Pa (Pascals) or mBar (millibar) according to selection.
    def readPressure(self, pressure_unit="Pa"):
        pressure = self.pRead
        #Change pressure from Pascals to millibar if user selection requires it
        if (pressure_unit == "mBar"):
            pressure = pressure / 100

        return pressure

    # Read Humidity from sensor as a Number.
    # Humidity is output as a percentage.
    def readHumidity(self):
        return self.hRead

    # Read Gas Resistance from sensor as a Number.
    # Units for gas resistance are in Ohms.
    def readGasRes(self):
        if (self.gasInit == False):
            self.screen.clear()
            self.screen.displayText("ERROR", 2)
            self.screen.displayText("Setup Gas Sensor", 3)
            self.screen.show()
            return 0
        return self.gRes

    # Read eCO2 from sensor as a Number (250 - 40000+ppm).
    # Units for eCO2 are in ppm (parts per million).
    def readeCO2(self):
        if (self.gasInit == False):
            self.screen.clear()
            self.screen.displayText("ERROR", 2)
            self.screen.displayText("Setup Gas Sensor", 3)
            self.screen.show()
            return 0
        self.calcAirQuality()

        return self.eCO2Value

    # Return the Air Quality rating as a percentage (0% = Bad, 100% = Excellent).
    def getAirQualityPercent(self):
        if (self.gasInit == False):
            self.screen.clear()
            self.screen.displayText("ERROR", 2)
            self.screen.displayText("Setup Gas Sensor", 3)
            self.screen.show()
            return 0
        self.calcAirQuality()

        return self.iaqPercent

    # Return the Air Quality rating as an IAQ score (500 = Bad, 0 = Excellent).
    # These values are based on the BME688 datasheet, Page 11, Table 6.
    def getAirQualityScore(self):
        if (self.gasInit == False):
            self.screen.clear()
            self.screen.displayText("ERROR", 2)
            self.screen.displayText("Setup Gas Sensor", 3)
            self.screen.show()
            return 0
        self.calcAirQuality()

        return self.iaqScore
    
    # Calculate the Index of Air Quality score from the current gas resistance and humidity readings
    # iaqPercent: 0 to 100% - higher value = better air quality
    # iaqScore: 25 should correspond to 'typically good' air, 250 to 'typically polluted' air
    # airQualityRating: Text output based on the iaqScore
    # Calculate the estimated CO2 value (eCO2)
    def calcAirQuality(self):
        humidityScore = 0
        gasScore = 0
        humidityOffset = self.hRead - self.hBase         # Calculate the humidity offset from the baseline setting
        ambTemp = (self.tAmbient / 100)
        temperatureOffset = self.tRead - ambTemp     # Calculate the temperature offset from the ambient temperature
        humidityRatio = ((humidityOffset / self.hBase) + 1)
        temperatureRatio = (temperatureOffset / ambTemp)

        # IAQ Calculations

        if (humidityOffset > 0):                                       # Different paths for calculating the humidity score depending on whether the offset is greater than 0
            humidityScore = (100 - self.hRead) / (100 - self.hBase)
        else:
            humidityScore = self.hRead / self.hBase
            
        humidityScore = humidityScore * self.hWeight * 100

        gasRatio = (self.gRes / self.gBase)

        if ((self.gBase - self.gRes) > 0):                                            # Different paths for calculating the gas score depending on whether the offset is greater than 0
            gasScore = gasRatio * (100 * (1 - self.hWeight))
        else:
            # Make sure that when the gas offset and humidityOffset are 0, iaqPercent is 95% - leaves room for cleaner air to be identified
            gasScore = math.floor(70 + (5 * (gasRatio - 1)))
            if (gasScore > 75):
                gasScore = 75

        self.iaqPercent = math.trunc(humidityScore + gasScore)               # Air quality percentage is the sum of the humidity (25% weighting) and gas (75% weighting) scores
        self.iaqScore = (100 - self.iaqPercent) * 5                               # Final air quality score is in range 0 - 500 (see BME688 datasheet page 11 for details)

        # eCO2 Calculations
        self.eCO2Value = 250 * math.pow(math.e, (0.012 * self.iaqScore))      # Exponential curve equation to calculate the eCO2 from an iaqScore input

        # Adjust eCO2Value for humidity and/or temperature greater than the baseline values
        if (humidityOffset > 0):
            if (temperatureOffset > 0):
                self.eCO2Value = self.eCO2Value * (humidityRatio + temperatureRatio)
            else:
                self.eCO2Value = self.eCO2Value * humidityRatio
        elif (temperatureOffset > 0):
            self.eCO2Value = self.eCO2Value * (temperatureRatio + 1)

        # If measurements are taking place rapidly, breath detection is possible due to the sudden increase in humidity (~7-10%)
        # If this increase happens within a 5s time window, 1200ppm is added to the eCO2 value
        # (These values were based on 'breath-testing' with another eCO2 sensor with algorithms built-in)
        if ((self.measTime - self.measTimePrev) <= 5000):
            if ((self.hRead - self.hPrev) >= 3):
                self.eCO2Value = self.eCO2Value + 1500

        self.eCO2Value = math.trunc(self.eCO2Value)
