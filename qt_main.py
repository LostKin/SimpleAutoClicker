import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal
from json_config import JsonConfig

from qt_autoclicker import AutoClicker
import multiprocessing as mp
import threading

class IndicatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.inactiveColor = QColor("#FF0000")
        self.activeColor = QColor("#00FF00")
        self.color = self.inactiveColor
        self.activeState = False
        self.setWindowTitle("AutoClickerPauseIndicator")
        self.resize(40, 40)
        self.move(0, 0)

        layout = QVBoxLayout(self)

        # Set the window flag to keep it always on top
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.activeState:
            painter.fillRect(self.rect(), self.activeColor)
        else:
            painter.fillRect(self.rect(), self.inactiveColor)

    def changeActiveState(self):
        self.activeState = not self.activeState
        self.repaint()


def full_stop():
    sys.exit(app.exec_())

class AutoClickerWindow(QWidget):
    stop_ac = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Auto Clicker")
        self.resize(600, 200)
        self.config_file = "config.json"
        self.config = JsonConfig(self.config_file)

        layout = QGridLayout()

        # Add some buttons to the grid (row, column)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(full_stop)

        self.start_button = QPushButton("Start Macro")
        self.start_button.clicked.connect(self.start_macro)

        self.cps_input = QLineEdit()
        self.cps_input.setFixedWidth(150)  # Set width in pixels
        self.cps_button = QPushButton("Set Clicks Per Second")
        self.cps_button.clicked.connect(self.update_cps)

        self.pause_button = QPushButton("Set Pause Button")
        self.pause_label = QLabel("")
        self.pause_button.clicked.connect(self.start_listening)

        layout.addWidget(self.pause_button, 0, 0)
        layout.addWidget(self.pause_label, 0, 1)
        layout.addWidget(self.cps_button, 1, 0)
        layout.addWidget(self.cps_input, 1, 1)
        layout.addWidget(self.exit_button, 2, 0)
        layout.addWidget(self.start_button, 2, 1)

        self.listening = False

        self.setLayout(layout)

        self.read_config()
        self.ac = AutoClicker(self.config.get("clicks_per_second"),
                         self.config.get("pause_button"))
        self.thread = None

        self.ac.update_state.connect(indicator_window.changeActiveState)
        self.stop_ac.connect(self.ac.update_mainloop)

    def read_config(self):
        if self.config.empty():
            # creating empty config
            self.config.set("clicks_per_second", 1)
            self.config.set("pause_button", "F7")
        self.cps_input.setText(str(self.config.get("clicks_per_second")))
        self.cps_input.update()
        self.pause_label.setText(str(self.config.get("pause_button")))
        self.pause_label.update()

    def update_cps(self):
        text = self.cps_input.text()
        try:
            cps = int(text)
            if cps > 0:
                self.config.set("clicks_per_second", cps)
                self.ac.cps = cps
                self.read_config()
            else:
                self.read_config()
        except ValueError:
            self.read_config()

    def start_listening(self):
        self.listening = True
        self.pause_label.setText("Press any key now...")

    def keyPressEvent(self, event):
        if self.listening:
            key = event.key()
            # Convert key code to human-readable text
            key_name = QKeySequence(key).toString()
            if not key_name:
                key_name = event.text()  # fallback to the text representation
            self.pause_label.setText(f"{key_name}")
            self.listening = False
            self.config.set("pause_button", key_name)
            self.ac.pause_key = key_name


    def closeEvent(self, event):
        sys.exit(app.exec_())
        # Close all other windows before main window closes
        indicator_window.close()
        self.thread.stop()
        self.ac.die()
        event.accept()

    def start_macro(self):
        if self.thread and self.thread.is_alive():
            print("Thread is already running")
            self.thread.join()
            return
        self.start_button.setText("Stop Macro")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.stop_macro)
        self.start_button.update()
        self.thread = threading.Thread(target=self.ac.mainloop, daemon=True)
        self.stop_ac.emit(False)
        self.thread.start()

    def stop_macro(self):
        self.start_button.setText("Start Macro")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start_macro)
        self.start_button.update()

        self.stop_ac.emit(True)
        self.thread.join()

if __name__ == "__main__":
    mp.freeze_support()

    app = QApplication([])
    indicator_window = IndicatorWindow()
    indicator_window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    indicator_window.show()
    main_window = AutoClickerWindow()
    main_window.show()
    app.exec()