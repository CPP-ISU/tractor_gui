import can
import cantools
import paho.mqtt.client as mqtt
import time

# === Configuration ===
DBC_FILE = "Tractor.dbc"  # Path to your DBC file
CAN_INTERFACE = "can0"    # Or "vcan0", "can1", etc.
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# === MQTT Setup ===
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

# === CAN Setup ===
db = cantools.database.load_file(DBC_FILE)
bus = can.interface.Bus(channel=CAN_INTERFACE, bustype='socketcan')  # use 'pcan' or 'usbcan' if needed

print("🚜 Listening for CAN messages...")

try:
    while True:
        msg = bus.recv()
        if msg is None:
            continue
        try:
            decoded = db.decode_message(msg.arbitration_id, msg.data)
            for name, value in decoded.items():
                topic = f"tractor/sensor/{name.lower()}"
                client.publish(topic, str(value))
                print(f"📡 {topic}: {value}")
        except Exception as e:
            print(f"⚠️ Failed to decode CAN message: {e}")

except KeyboardInterrupt:
    print("🛑 Stopped by user")
    client.loop_stop()
    client.disconnect()
