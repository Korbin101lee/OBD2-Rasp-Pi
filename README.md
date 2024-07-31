# Car OBD-2 Reader with Raspberry Pi

## Description
This project connects to your car's OBD-2 port using a Raspberry Pi and retrieves real-time data using the python-obd library. The data is displayed on a user-friendly interface built with PyQt5. This project aims to provide an accessible way to monitor vehicle diagnostics and performance.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Code Examples](#code-examples)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact Information](#contact-information)

## Installation

### Prerequisites
- Raspberry Pi with Raspbian OS installed
- Python 3
- python-obd library
- PyQt5 library

### Steps
1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/obd-reader.git
    cd obd-reader
    ```

2. **Install dependencies**
    ```sh
    pip install pyqt5 python-obd
    ```

3. **Run the application**
    ```sh
    python main.py
    ```

## Usage
1. Connect your Raspberry Pi to the car's OBD-2 port using an OBD-II adapter.
2. Power on the Raspberry Pi and run the application.
3. The interface will display real-time data from the car's OBD-2 system.

### Features
- Display real-time data such as speed, RPM, engine load, and more.
- Clear Diagnostic Trouble Codes (DTCs) from the car's ECU.

## Screenshots
![Main Interface](screenshots/main_interface.png)

## Code Examples

### Main Window Initialization
```python
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1535, 900)
        self.obd_reader = OBDReader()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_lcds)
        self.timer.start(1000)
        self.pushButton.clicked.connect(self.clear_dtc)
