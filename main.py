import sys
from PyQt5 import QtWidgets, QtCore
from obd_reader_gui import Ui_MainWindow  # Import the converted UI file
from obd_reader import OBDReader  # Import your OBD reader class

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1535, 900)  # Resolution: 1920x1080

        # Initialize the OBD reader
        self.obd_reader = OBDReader()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_lcds)
        self.timer.start(1000)  # Update every second

        # Connect buttons to functions
        self.pushButton.clicked.connect(self.clear_dtc)
        # Add more connections here for other buttons

    def update_lcds(self):
        values = self.obd_reader.get_latest_values()
        self.lcdNumber.display(values["speed"])
        self.lcdNumber_2.display(values["rpm"])
        self.lcdNumber_3.display(values["engine_load"])
        self.lcdNumber_4.display(values["coolant_temp"])
        self.lcdNumber_5.display(values["fuel_pressure"])
        self.lcdNumber_6.display(values["timing_advance"])
        self.lcdNumber_7.display(values["intake_temp"])
        self.lcdNumber_8.display(values["air_flow_rate"])
        self.lcdNumber_9.display(values["throttle_position"])
        self.lcdNumber_10.display(values["run_time"])
    def clear_dtc(self):
        self.obd_reader.clear_dtc()
        self.statusBar().showMessage('DTCs cleared successfully!')

    # Add more methods here to handle other button clicks

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
