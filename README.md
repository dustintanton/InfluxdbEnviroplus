# InfluxdbEnviroplus
This Project uses a Raspberry Pi with the Enviro+ Board from Pimoroni to acquire weather data and send to an InfluxDB server for data logging.

Raspberry Pi Weather Data Logger with Enviro+ and InfluxDB

This project utilizes a Raspberry Pi, Enviro+ board, and various sensors to acquire weather data and log it to an InfluxDB server. The data includes temperature, pressure, humidity, air quality, and particulate matter.

Features

- Weather Data Acquisition: Collects temperature, pressure, and humidity using the BME280 sensor.
- Air Quality Monitoring: Measures air quality parameters using the PMS5003 sensor and the MICS6814 gas sensor.
- Light Measurement: Reads light levels using the LTR559 sensor.
- Data Logging: Sends collected data to an InfluxDB server for logging and analysis.
- Display Integration: Outputs data to an ST7735 LCD display (optional for visualization).

Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Enviro+ board
- ST7735 LCD display (optional)
- PMS5003 sensor
- BME280 sensor
- MICS6814 gas sensor
- LTR559 sensor

Software Requirements

- Python 3
- Required Python packages:
  - influxdb-client
  - Pillow
  - ST7735
  - bme280
  - pms5003
  - enviroplus
  - ltr559 (or use ltr559 fallback)
  - smbus2 (or smbus fallback)

Setup and Installation

1. Clone the Repository:

   git clone https://github.com/yourusername/raspberrypi-weather-data-logger.git
   cd raspberrypi-weather-data-logger

2. Install Required Python Packages:

   You can install the required packages using pip. Ensure you are in the project directory and run:

   pip install -r requirements.txt

   Create a requirements.txt file with the following content:

   influxdb-client
   Pillow
   ST7735
   bme280
   pms5003
   enviroplus
   ltr559
   smbus2

3. Configure InfluxDB:

   Edit the script to set your InfluxDB credentials:

   influx_url = "http://localhost:8086"
   influx_token = "your_token_here"
   bucket = "your_bucket_here"
   org = "your_org_here"

4. Run the Script:

   Ensure your hardware is connected and run the script:

   python weather_data_logger.py

5. Optional: Display Data:

   If you are using an ST7735 LCD display, it will show data readings as the script runs.

Script Overview

- Data Acquisition: Collects data from various sensors.
- Data Processing: Compensates temperature readings and averages CPU temperature.
- Data Logging: Sends data to InfluxDB in points with fields and tags.
- Display: Updates LCD display with sensor readings (optional).

Troubleshooting

- Import Errors: Ensure all required libraries are installed and correctly named.
- Connection Issues: Verify InfluxDB URL, token, and network connection.
