import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from mqtt.mqtt_client import MqttClient


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPP 2025 Tractor Dashboard")
        self.setStyleSheet("background-color: black; color: white;")
        self.setMinimumSize(1280, 480)

        # Fonts
        big_font = QFont("Arial", 36, QFont.Bold)
        label_font = QFont("Arial", 16, QFont.Bold)
        small_font = QFont("Arial", 12)

        def create_display(title, unit, value_text="--"):
            layout = QVBoxLayout()
            title_label = QLabel(title)
            title_label.setFont(label_font)
            title_label.setAlignment(Qt.AlignCenter)

            value_label = QLabel(value_text)
            value_label.setFont(big_font)
            value_label.setStyleSheet("border: 3px solid red; padding: 10px;")
            value_label.setAlignment(Qt.AlignCenter)

            unit_label = QLabel(unit)
            unit_label.setFont(label_font)
            unit_label.setAlignment(Qt.AlignCenter)

            layout.addWidget(title_label)
            layout.addWidget(value_label)
            layout.addWidget(unit_label)
            return layout, value_label

        # Display sections
        rpm_box, self.rpm_value = create_display("ENGINE SPEED", "RPM")
        mph_box, self.mph_value = create_display("WHEEL SPEED", "MPH")
        volts_box, self.volts_value = create_display("GENERATOR", "VOLTS")
        fuel_box, self.fuel_value = create_display("FUEL", "%")

        # Gear Display
        gear_layout = QVBoxLayout()
        gear_title = QLabel("GEAR ⚙")
        gear_title.setFont(label_font)
        gear_title.setAlignment(Qt.AlignCenter)

        self.gear_label = QLabel("N")
        self.gear_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.gear_label.setStyleSheet("border: 3px solid red; padding: 20px;")
        self.gear_label.setAlignment(Qt.AlignCenter)

        gear_layout.addWidget(gear_title)
        gear_layout.addWidget(self.gear_label)

        # Warnings
        warning_box = QVBoxLayout()
        warning_title = QLabel("WARNINGS ⚠")
        warning_title.setFont(label_font)
        warning_title.setAlignment(Qt.AlignCenter)

        self.warning_labels = []
        for i in range(4):
            w_label = QLabel("")
            w_label.setFont(small_font)
            w_label.setAlignment(Qt.AlignCenter)
            w_label.setStyleSheet("color: red;" if i == 0 else "color: gray;")
            self.warning_labels.append(w_label)
            warning_box.addWidget(w_label)

        warning_layout = QVBoxLayout()
        warning_frame = QWidget()
        warning_frame.setStyleSheet("border: 3px solid red; padding: 10px;")
        warning_frame.setLayout(warning_box)
        warning_layout.addWidget(warning_title)
        warning_layout.addWidget(warning_frame)

        # Main layout assembly
        main_layout = QHBoxLayout()
        main_layout.addLayout(rpm_box)
        main_layout.addLayout(mph_box)

        generator_layout = QVBoxLayout()
        generator_layout.addLayout(volts_box)
        generator_layout.addLayout(fuel_box)
        main_layout.addLayout(generator_layout)

        main_layout.addLayout(gear_layout)
        main_layout.addLayout(warning_layout)

        self.setLayout(main_layout)

        # Connect MQTT
        self.mqtt = MqttClient(
            on_temp=self.update_temp,
            on_speed=self.update_speed,
            on_voltage=self.update_voltage,
            on_fuel=self.update_fuel,
            on_gear=self.update_gear,
            on_warning=self.update_warning,
            on_status=self.update_status
        )
        self.mqtt.connect()

        self.showFullScreen()

    def update_temp(self, value):
        self.rpm_value.setText(value)

    def update_speed(self, value):
        self.mph_value.setText(value)

    def update_voltage(self, value):
        self.volts_value.setText(value)

    def update_fuel(self, value):
        self.fuel_value.setText(value)

    def update_gear(self, value):
        self.gear_label.setText(value)

    def update_warning(self, value):
        warning_map = {
            "0": "",
            "1": "⚠ Engine Overheat",
            "2": "⚠ Low Fuel",
            "3": "⚠ Transmission Fault",
        }
        self.warning_labels[0].setText(warning_map.get(value, f"⚠ Unknown ({value})"))

    def update_status(self, state):
        print(f"[MQTT STATUS] → {state}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
