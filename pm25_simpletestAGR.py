# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

import adafruit_bme680
import time
import csv
import board
import busio
import pandas as pd
import numpy as np
from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)

# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

# Create library object, use 'slow' 100KHz frequency!
# i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
# pm25 = PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

file = open('data/simpletest.csv', 'w', newline = None)

csvwriter = csv.writer(file, delimiter=',')

meta = ['time','PM2.5 env','particles 2.5um']
csvwriter.writerow(meta)

# for i in range(10):
#     now = time.time()
#     value = np.random.random()
#     csvwriter.writerow([now,value])

#==========================================
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25

temp_offset = -5
i=0
print("Time = %0.2f" %time.time())
#==========================================

baseTime = time.time()
for i in range(30):
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print()
    print(time.time() - baseTime, "seconds since start")
    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    #==========================================
    print("---------------------------------------")
    print("Weather Data")
    print("---------------------------------------")
    print("Temperature = " bme680.temperature)
    print("Gas: %d ohm" %bme680.gas)
    print("Humidity : %0.1f %%" %bme680.relative_humidity)
    print("Pressure: %0.3f hPa" %bme680.pressure)
    print("Altitude = %0.2f meters" %bme680.altitude)
    print("---------------------------------------")
    i+=1
    #==========================================
    
    now = time.time()
    env = aqdata["pm25 env"]
    particles = aqdata["particles 25um"]
    temp = bme680.temperature
    gas = %bme680.gas
    humidity = %bme680.relative_humidity
    pressure = %bme680.pressure
    altitude = %bme680.altitude
    csvwriter.writerow([now,env,particles,temp,gas,humidity,pressure,altitude])

    

#==========================================

#==========================================

file.close()