# Import necessary libraries
import can               # python-can for working with CAN bus messages
import cantools          # For working with DBC files and encoding messages
import time              # Used for simulating delay between messages

# === Configuration ===
DBC_FILE = "tractor.dbc"       # Path to your DBC file (must match exactly with can_to_mqtt.py)
CAN_INTERFACE = "vcan0"        # Virtual CAN interface name (used by both sender and receiver)

# Load the DBC file so we can encode messages properly
db = cantools.database.load_file(DBC_FILE)

# Get the message definition from the DBC by its name (must match BO_ name in the DBC)
msg_def = db.get_message_by_name("EngineData")

# Create a virtual CAN bus that supports multiple threads (shared between scripts)
bus = can.ThreadSafeBus(channel=CAN_INTERFACE, interface="virtual")

# Sample data to simulate engine sensor values
test_frames = [
    {"RPM": 1200.0, "Speed": 15.5, "Voltage": 13.5, "Temp": 90, "Fuel": 60, "Gear": 3, "Warning": 0},
    {"RPM": 2200.0, "Speed": 25.3, "Voltage": 13.2, "Temp": 95, "Fuel": 45, "Gear": 4, "Warning": 1},
    {"RPM": 500.0,  "Speed": 5.0,  "Voltage": 12.8, "Temp": 85, "Fuel": 75, "Gear": 2, "Warning": 2},
]

print("Sending CAN messages on virtual interface...")

# Loop through messages and send them repeatedly
try:
    while True:
        for frame in test_frames:
            # Extract and encode only the signal values defined in the DBC
            signals = {k: frame[k] for k in msg_def.signal_tree}
            payload = msg_def.encode(signals)  # Encode signal values into raw CAN data

            # Create a CAN message with the correct arbitration ID and encoded payload
            msg = can.Message(arbitration_id=msg_def.frame_id, data=payload, is_extended_id=False)

            # Send the message on the virtual CAN bus
            bus.send(msg)

            # Print debug output to verify message was sent
            print(f"Sent: ID=0x{msg.arbitration_id:X}, Data={msg.data.hex()}, Frame={frame}")

            # Wait for 1 second before sending the next frame
            time.sleep(1)

# Allow shutdown with Ctrl+C
except KeyboardInterrupt:
    print("Simulation stopped.")

# Shutdown the CAN interface cleanly
finally:
    bus.shutdown()
