# simulate.py
import paho.mqtt.publish as publish
import time
import random

MQTT_HOST = "localhost"
MQTT_PORT = 1883

# Optional gear and warnings for realism
gears = ['P', 'R', 'N', 'D', 'L']
warnings_pool = [
    "", "HIGH TEMP", "LOW OIL", "CHECK ENGINE", "FAULT"
]

while True:
    temp = round(random.uniform(20, 35), 1)         # °F
    speed = round(random.uniform(5, 15), 1)         # mph
    voltage = round(random.uniform(11.5, 13.0), 2)  # Volts
    fuel = round(random.uniform(10, 100), 1)        # Fuel %
    gear = random.choice(gears)
    warning = random.choice(warnings_pool)

    # Publish simulated sensor data
    publish.single("tractor/sensor/temperature", str(temp), hostname=MQTT_HOST, port=MQTT_PORT)
    publish.single("tractor/sensor/speed", str(speed), hostname=MQTT_HOST, port=MQTT_PORT)
    publish.single("tractor/sensor/voltage", str(voltage), hostname=MQTT_HOST, port=MQTT_PORT)
    publish.single("tractor/sensor/fuel", str(fuel), hostname=MQTT_HOST, port=MQTT_PORT)
    publish.single("tractor/sensor/gear", gear, hostname=MQTT_HOST, port=MQTT_PORT)
    publish.single("tractor/sensor/warning", warning, hostname=MQTT_HOST, port=MQTT_PORT)

    print(f"Sent → Temp: {temp} °F | Speed: {speed} mph | Voltage: {voltage} V | Fuel: {fuel}% | Gear: {gear} | Warning: {warning}")
    time.sleep(2)
