# tractor_gui
Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
Traceback (most recent call last):
  File "/home/cpp/tractor_gui/main.py", line 7, in <module>
    window = MainWindow()
  File "/home/cpp/tractor_gui/gui/main_window.py", line 97, in __init__
    self.mqtt = MqttClient(
  File "/home/cpp/tractor_gui/mqtt/mqtt_client.py", line 11, in __init__
    self.client.on_connect = self.on_connect
AttributeError: 'MqttClient' object has no attribute 'on_connect'. Did you mean: 'connect'?

