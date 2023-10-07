"""
    Battery_Management_App  Copyright (C) 2023 Krishna Reddy
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
"""

import sys
import psutil
import serial
from PyQt5 import QtWidgets, QtGui
from Design import Ui_BatteryManager
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QAction, QSystemTrayIcon, QApplication, QMainWindow, QMenu

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_BatteryManager()
        self.ui.setupUi(self)
        self.setWindowTitle("Battery Manager")

        #setting icon for the window
        self.setWindowIcon(QtGui.QIcon('iconApp.ico'))

        # Connect buttons to functions
        self.ui.pushButton.clicked.connect(self.trigger_action)
        self.ui.pushButton_2.clicked.connect(self.start_action)
        self.ui.pushButton_3.clicked.connect(self.connect_action)
        # Create a QTimer to update battery status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_battery_status)
        self.timer.start(1000)  # Update every 1 seconds
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.send_battery_percentage_update)
        # Initial status values
        
        self.battery_status = "Unknown"
        self.battery_percentage = 0
         
        # keep fixedsize
        self.setFixedSize(self.size())  # Set the window size to its current size

        self.update_status_labels()
        # Connect sliders to functions for updating limits
        self.ui.horizontalSlider.valueChanged.connect(self.update_lower_limit)
        self.ui.horizontalSlider_2.valueChanged.connect(self.update_upper_limit)
        self.start_process_active = False
        # Initial limit values
        self.lower_limit = self.ui.horizontalSlider.value()
        self.upper_limit = self.ui.horizontalSlider_2.value()
        self.update_limit_labels()
        self.serial_connection = None

        
               # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(QtGui.QIcon('app.png'))
        self.tray_icon.setToolTip('Battery Manager')
        self.tray_icon.activated.connect(self.toggle_window)
        self.tray_icon_menu = QMenu()
        self.show_action = QAction('Show', self)
        self.exit_action = QAction('Exit', self)
        self.show_action.triggered.connect(self.show_window)
        self.exit_action.triggered.connect(self.close_application)
        self.tray_icon_menu.addAction(self.show_action)
        self.tray_icon_menu.addAction(self.exit_action)
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

        # Hide the main window by default
        self.hide()
        # Set custom styles using CSS
        self.setStyleSheet("""
QMainWindow {
    background-color: #2c3e50;
}

QLabel {
    color: #ecf0f1;
}

QPushButton {
    background-color: #e74c3c;
    color: white;
    border: 1px solid #c0392b;
    border-radius: 5px;
    padding: 5px 10px;
    transition: background-color 0.3s;
}

QPushButton:hover {
    background-color: #c0392b;
}

QPushButton:disabled {
    background-color: #dcdde1;
    border: 1px solid #dcdde1;
}

QSlider::groove:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e67e22, stop:1 #f39c12);
    height: 6px;
    border: 1px solid #d35400;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f39c12, stop:1 #e67e22);
    border: 1px solid #d35400;
    width: 18px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 9px;
}

#errorLabel {
    color: red;
}
""")

# Level bars
        self.ui.horizontalSlider.setStyleSheet("""
QSlider::groove:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2ecc71);
    height: 6px;
    border: 1px solid #239b56;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
    border: 1px solid #239b56;
    width: 18px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 9px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e74c3c, stop:1 #c0392b);
    height: 6px;
    border: 1px solid #d35400;
    border-radius: 3px;
}
""")

        self.ui.horizontalSlider_2.setStyleSheet("""
QSlider::groove:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498db, stop:1 #2ecc71);
    height: 6px;
    border: 1px solid #239b56;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2ecc71, stop:1 #27ae60);
    border: 1px solid #239b56;
    width: 18px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 9px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e74c3c, stop:1 #c0392b);
    height: 6px;
    border: 1px solid #d35400;
    border-radius: 3px;
}
""")



    def update_limit_labels(self):
          self.ui.lbl_L.setText(f"Lower Limit: {self.lower_limit}")
          self.ui.lbl_U.setText(f"Upper Limit: {self.upper_limit}")

    def update_lower_limit(self, value):
           self.lower_limit = value
           self.update_limit_labels()

    def update_upper_limit(self, value):
          self.upper_limit = value
          self.update_limit_labels()
    def update_status_labels(self):
         
         self.ui.lbl_Bs.setText(f"Battery Status: {self.battery_status}")
         self.ui.lbl_Bp.setText(f"Battery Percentage: {self.battery_percentage}%")

    def update_battery_status(self):
        battery = psutil.sensors_battery()
        if battery is not None:
            self.battery_status = "Charging" if battery.power_plugged else "Discharging"
            self.battery_percentage = battery.percent
        else:
            self.battery_status = "Unknown"
            self.battery_percentage = 0

        self.update_status_labels()

         
    def trigger_action(self):
          if self.start_process_active:
            # Terminate the start process
            self.start_process_active = False
            self.ui.label.setText("Start process terminated")
          else:
            self.ui.label.setText("Start process is not active")
            pass

    def start_action(self):
        if self.serial_connection is not None:
          try:
            # Send the lower limit, upper limit, and initial battery percentage to ESP32
            lower_limit = self.ui.horizontalSlider.value()
            upper_limit = self.ui.horizontalSlider_2.value()
            lower_limit_command = f"Lower:{lower_limit}\n"
            upper_limit_command = f"Upper:{upper_limit}\n"

            # Format the data to send
            data_to_send = f"{lower_limit_command}{upper_limit_command}Battery:{self.battery_percentage}\n"
            self.serial_connection.write(data_to_send.encode())
            
            # Start the timer to periodically send battery percentage updates
            self.update_timer.start(30000)  # Send every 30 seconds

            self.ui.label.setText("ESP32 started")

          except Exception as e:
            # Handle command sending errors
            self.ui.label.setText(f"Command Error: {str(e)}")
        else:
         self.ui.label.setText("Not connected to ESP32")
    pass
    def send_battery_percentage_update(self):
        if self.serial_connection is not None:
            try:
                # Send updated battery percentage to ESP32
                data_to_send = f"Battery:{self.battery_percentage}\n"
                self.serial_connection.write(data_to_send.encode())

            except Exception as e:
                # Handle sending errors
                self.ui.label.setText(f"Update Error: {str(e)}")

    def connect_action(self):
        try:
            # Replace 'COMX' with the appropriate COM port (e.g., 'COM3' on Windows)
            serial_port = 'COM9'  # Example COM port

            # Open a serial connection to the ESP32
            self.serial_connection = serial.Serial(serial_port, baudrate=9600, timeout=1)

            # Update the label at the bottom of the app
            self.ui.label.setText("Connected to ESP32 via Serial")

        except Exception as e:
            # Handle connection errors
            self.ui.label.setText(f"Connection Error: {str(e)}")
        pass


    def toggle_window(self, reason):
     if reason == QSystemTrayIcon.Trigger:
        if self.isHidden():
            self.show_window()
        else:
            self.hide()

    def show_window(self):
     self.show()
     self.setWindowState(Qt.WindowActive)  # Use Qt.WindowActive
     self.activateWindow()

    def close_application(self):
        self.tray_icon.hide()
        self.close()
def main():
    app = QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
