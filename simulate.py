# simulate.py
import paho.mqtt.publish as publish
import time
import random

while True:
    temp = round(random.uniform(20, 35), 1)         # °F
    speed = round(random.uniform(5, 15), 1)         # mph
    voltage = round(random.uniform(11.5, 13.0), 2)  # V
    fuel = round(random.uniform(10, 100), 1)        # %

    publish.single("tractor/sensor/temperature", str(temp), hostname="localhost")
    publish.single("tractor/sensor/speed", str(speed), hostname="localhost")
    publish.single("tractor/sensor/voltage", str(voltage), hostname="localhost")
    publish.single("tractor/sensor/fuel", str(fuel), hostname="localhost")

    print(f"Sent → Temp: {temp} °F | Speed: {speed} mph | Voltage: {voltage} V | Fuel: {fuel}%")
    time.sleep(2)
