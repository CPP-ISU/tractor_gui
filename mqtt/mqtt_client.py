import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, on_temp, on_speed, on_voltage=None, on_fuel=None, on_status=None):
        self.on_temp = on_temp
        self.on_speed = on_speed
        self.on_voltage = on_voltage
        self.on_fuel = on_fuel
        self.on_status = on_status

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def connect(self, broker="localhost", port=1883):
        if self.on_status:
            self.on_status("connecting")
        try:
            self.client.connect(broker, port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"MQTT connection error: {e}")
            if self.on_status:
                self.on_status("error")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker")
        if self.on_status:
            self.on_status("connected")

        client.subscribe("tractor/sensor/temperature")
        client.subscribe("tractor/sensor/speed")
        client.subscribe("tractor/sensor/voltage")
        client.subscribe("tractor/sensor/fuel")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker")
        if self.on_status:
            self.on_status("disconnected")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"MQTT → {topic}: {payload}")

        if topic == "tractor/sensor/temperature":
            self.on_temp(payload)
        elif topic == "tractor/sensor/speed":
            self.on_speed(payload)
        elif topic == "tractor/sensor/voltage" and self.on_voltage:
            self.on_voltage(payload)
        elif topic == "tractor/sensor/fuel" and self.on_fuel:
            self.on_fuel(payload)

    def publish_command(self, command):
        print(f"MQTT ← Command: {command}")
        self.client.publish("tractor/control", command)
