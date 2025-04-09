from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QDial, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from mqtt.mqtt_client import MqttClient


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tractor GUI")
        self.setMinimumSize(500, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # Fonts
        font_label = QFont("Arial", 20, QFont.Bold)
        font_button = QFont("Arial", 16)

        # Sensor Labels
        self.temp_label = QLabel("Temperature: -- °F")
        self.temp_label.setFont(font_label)

        self.speed_label = QLabel("Speed: -- mph")
        self.speed_label.setFont(font_label)

        self.engine_status_label = QLabel("Engine: OFF")
        self.engine_status_label.setFont(font_label)

        # Speed Dial
        self.speed_dial = QDial()
        self.speed_dial.setMinimum(0)
        self.speed_dial.setMaximum(60)
        self.speed_dial.setNotchesVisible(True)
        self.speed_dial.setFixedSize(200, 200)
        self.speed_dial.setEnabled(False)

        # Gauge wrapper with labels
        dial_wrapper = QGridLayout()
        dial_widget = QWidget()
        dial_widget.setLayout(dial_wrapper)

        label_style = "color: white; font-size: 16px; font-weight: bold;"

        labels = {
            (0, 2): "30",   
            (1, 1): "20",   
            (1, 3): "40",   
            (2, 0): "10", 
            (2, 4): "50",  
            (3, 1): "0",   
            (3, 3): "60",  
            (4, 2): "mph"  
        }
        # Add   dial in center
        dial_wrapper.addWidget(self.speed_dial, 2, 2)

        # Add labels
        for pos, text in labels.items():
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            lbl.setAlignment(Qt.AlignCenter)
            dial_wrapper.addWidget(lbl, pos[0], pos[1])


        # Start/Stop Buttons
        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_start.setFont(font_button)
        self.btn_stop.setFont(font_button)
        self.btn_stop.setEnabled(False)

        self.btn_start.clicked.connect(self.start_engine)
        self.btn_stop.clicked.connect(self.stop_engine)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_stop)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.temp_label)
        main_layout.addWidget(self.speed_label)
        main_layout.addWidget(self.engine_status_label)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        main_layout.addWidget(dial_widget, alignment=Qt.AlignHCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # Engine state
        self.engine_on = False

        # MQTT setup
        self.mqtt = MqttClient(
            on_temp=self.update_temp,
            on_speed=self.update_speed,
            on_status=self.update_status
        )
        self.mqtt.connect()
        self.showFullScreen()

    def update_temp(self, value):
        self.temp_label.setText(f"Temperature: {value} °F")

    def update_speed(self, value):
        self.speed_label.setText(f"Speed: {value} mph")
        try:
            val = float(value)
            self.speed_dial.setValue(int(val))
        except ValueError:
            pass

    def update_status(self, state):
        print(f"[MQTT] Status: {state}")

    def start_engine(self):
        if not self.engine_on:
            self.engine_on = True
            self.engine_status_label.setText("Engine: RUNNING")
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.mqtt.publish_command("START")

    def stop_engine(self):
        if self.engine_on:
            self.engine_on = False
            self.engine_status_label.setText("Engine: OFF")
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
            self.mqtt.publish_command("STOP")
