# Import required libraries
import can                             # For working with CAN messages
import cantools                        # For decoding CAN messages using a DBC file
import paho.mqtt.client as mqtt        # For communicating with an MQTT broker
import time                            # For time-related functions
import os                              # For checking file paths

# === Configuration ===
DBC_FILE = "tractor.dbc"               # Path to the DBC file describing CAN message formats
CAN_INTERFACE = "vcan0"                # Virtual CAN channel name (must match test sender)
MQTT_BROKER = "localhost"              # IP or hostname of the MQTT broker (localhost = same machine)
MQTT_PORT = 1883                       # Standard MQTT port number

# === MQTT Setup ===
client = mqtt.Client()                 # Create an MQTT client instance

# Try to connect to the MQTT broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)  # Establish connection to broker
    client.loop_start()                     # Start background network loop to handle messages
    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"MQTT connection failed: {e}")
    exit(1)  # Exit the program if connection fails

# === Load DBC File ===
# Check if the DBC file exists at the given path
if not os.path.exists(DBC_FILE):
    print(f"DBC file not found: {DBC_FILE}")
    exit(1)

# Try to parse the DBC file to understand message structure
try:
    db = cantools.database.load_file(DBC_FILE)  # Load and parse the DBC file
    print("Messages loaded from DBC:")
    for msg in db.messages:  # Print each message ID and name from the DBC
        print(f" - ID={msg.frame_id}, Hex={hex(msg.frame_id)}, Name={msg.name}")
except Exception as e:
    print(f"Failed to load DBC file: {e}")
    exit(1)

# === Setup CAN Bus ===
# Try to open a virtual CAN interface for reading messages
try:
    bus = can.ThreadSafeBus(channel=CAN_INTERFACE, interface='virtual')
    print(f"Listening on CAN interface: {CAN_INTERFACE}")
except Exception as e:
    print(f"Failed to initialize CAN interface: {e}")
    exit(1)

# === Main Loop: Listen for and decode CAN messages ===
print("Waiting for CAN messages...")

try:
    while True:
        # Block until a CAN message is received from the bus
        msg = bus.recv()
        if msg is None:
            continue  # If no message is received, skip this loop

        # Print the raw CAN message ID and data payload
        print(f"Received raw CAN message: ID=0x{msg.arbitration_id:X}, Data={msg.data.hex()}")

        # Try to find a matching message format from the DBC based on the message ID
        message = db.get_message_by_frame_id(msg.arbitration_id)
        if not message:
            print(f"No matching message found in DBC for ID: {msg.arbitration_id} (0x{msg.arbitration_id:X})")
            continue  # Skip this message if it's not recognized

        print(f"Matched message: {message.name}")  # Confirm which message type matched

        # Attempt to decode the message using the matched format
        try:
            decoded = message.decode(msg.data)  # Decode the raw bytes into signal values
            for name, value in decoded.items():
                topic = f"tractor/sensor/{name.lower()}"  # Format MQTT topic
                client.publish(topic, str(value))         # Send value to MQTT broker
                print(f"Published to MQTT: {topic} = {value}")
        except Exception as e:
            print(f"Failed to decode message ID {msg.arbitration_id}: {e}")

# Handle exit on Ctrl+C
except KeyboardInterrupt:
    print("Shutdown requested by user.")

# Cleanup: disconnect from MQTT broker when done
finally:
    client.loop_stop()
    client.disconnect() 
    print("MQTT client disconnected. Exiting.")
