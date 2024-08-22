#from retry import retry
import time
import colorsys
import os
import sys
import socket
import ST7735

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

#fvalent
from pms5003 import PMS5003

from bme280 import BME280
from enviroplus import gas
from subprocess import PIPE, Popen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

print("""
Press Ctrl+C to exit!
""")

# BME280 temperature/pressure/humidity sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

#fvalent
pms5003 = PMS5003()

# Create ST7735 LCD display class
st7735 = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display
st7735.begin()

WIDTH = st7735.width
HEIGHT = st7735.height

# Set up canvas and font
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
path = os.path.dirname(os.path.realpath(__file__))
font = ImageFont.truetype(path + "/fonts/Asap/Asap-Bold.ttf", 20)

# Set up InfluxDB
influx_url = "*************"
influx_token = "*************"
bucket = "**************"
org = "*************"

client = InfluxDBClient(url=influx_url, token=influx_token)

write_api = client.write_api(write_options=SYNCHRONOUS)

# The position of the top bar
top_pos = 25

# Create a values dict to store the data
variables = ["temperature",
             "pressure",
             "humidity",
             "light",
             "oxidised",
             "reduced",
             "nh3",
             "pm010",
             "pm025",
             "pm100"]

values = {}

for v in variables:
    values[v] = [1] * WIDTH

# Get the temperature of the CPU for compensation
def get_cpu_temperature():

    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()
    return float(output[output.index('=') + 1:output.rindex("'")])

# Tuning factor for compensation. Decrease this numebr to adjust the 
# temperature down, adn increase to adjust up
factor = 1

# The main loop
try:
    iterations = 0
    cpu_temps = []
    while True:
        proximity = ltr559.get_proximity()

        # Compensated Temperature
        cpu_temp = get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        compensated_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

        # Create a Point with data
        point = Point("enviroplus").tag("host", "enviroplusJapan").field("ltr559.proximity", proximity).field("bme280.temperature.raw", bme280.get_temperature()).field("bme280.temperature.compensated", compensated_temp).field("cpu.temperature", get_cpu_temperature()).field("bme280.pressure", bme280.get_pressure()).field("bme280.humidity", bme280.get_humidity())

        if proximity < 10:
            point.field("ltr559.lux", ltr559.get_lux())
        else:
            point.field("ltr559.lux", 1.0)

        gas_data = gas.read_all()
        point.field("mics6814.oxidising", gas_data.oxidising).field("mics6814.reducing", gas_data.reducing).field("mics6814.nh3", gas_data.nh3)

        #fvalent
        data = pms5003.read()
        point.field("pms5003.pm010", data.pm_ug_per_m3(1.0)).field("pms5003.pm025", data.pm_ug_per_m3(2.5)).field("pms5003.pm100", data.pm_ug_per_m3(10))

        # Write the point to InfluxDB
        if iterations > 5:
            write_api.write(bucket=bucket, org=org, record=point, timeout=30)
            print(point)
            print("Data successfully written to InfluxDB.")
        else:
            print("Skipping for Data Accuracy.")
        time.sleep(10)
        iterations += 1

# Exit cleanly
except KeyboardInterrupt:
    sys.exit(0)
