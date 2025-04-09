# simulate.py
import paho.mqtt.publish as publish
import time
import random

while True:
    temp = round(random.uniform(20, 35), 1)
    speed = round(random.uniform(5, 15), 1)

    publish.single("tractor/sensor/temperature", str(temp), hostname="localhost")
    publish.single("tractor/sensor/speed", str(speed), hostname="localhost")

    print(f"Sent → Temp: {temp} °F | Speed: {speed} mph")
    time.sleep(2)
