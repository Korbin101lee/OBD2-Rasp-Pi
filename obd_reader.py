import obd
from obd import OBDStatus
from threading import Thread


class OBDReader:
    def __init__(self):
        self.latest_rpm = None
        self.latest_status = None
        self.latest_freeze_dtc = None
        self.latest_fuel_status = None
        self.latest_engine_load = None
        self.latest_coolant_temp = None
        self.latest_fuel_pressure = None
        self.latest_intake_pressure = None
        self.latest_speed = None
        self.latest_timing_advance = None
        self.latest_intake_temp = None
        self.latest_air_flow_rate = None
        self.latest_throttle_pos = None
        self.latest_air_status = None
        self.O2_sensor = None
        self.latest_run_time = None
        self.latest_commanded_egr = None
        self.latest_egr_error = None
        self.latest_evaporative_purge = None
        self.latest_fuel_level = None
        self.latest_evap_vapor_pressure = None
        self.latest_barometric_pressure = None
        self.latest_dtc = None

        self.async_connection = obd.Async(timeout=0.5, start_low_power=True)
        self.sync_connection = obd.OBD(timeout=0.5, start_low_power=True)
        self.setup_async_commands()

    def obd_check(self):
        status = self.sync_connection.status()
        port = self.sync_connection.port_name()  # Get the port name
        protocol = self.sync_connection.protocol_name()  # Get the protocol name

        if status == OBDStatus.NOT_CONNECTED:
            print(f"Not connected to OBD-II adapter on port {port}")
            exit()
        elif status == OBDStatus.ELM_CONNECTED:
            print(f"Connected to ELM327 adapter on port {port}, but not to the car")
        elif status == OBDStatus.OBD_CONNECTED:
            print(f"Connected to the OBD-II socket on port {port}, but the car's ignition is off")
        elif status == OBDStatus.CAR_CONNECTED:
            print(f"Successfully connected to the car with ignition on, on port {port}, using protocol {protocol}")
        else:
            print(f"Unknown status: {status} on port {port}")
            exit()

    def supported_commands(self):
        print("Supported commands:")
        for cmd in self.sync_connection.supported_commands:
            print(f" - {cmd.name}")

    def setup_async_commands(self):
        self.async_connection.watch(obd.commands.RPM, callback=self.update_rpm)
        self.async_connection.watch(obd.commands.ENGINE_LOAD, callback=self.update_engine_load)
        self.async_connection.watch(obd.commands.COOLANT_TEMP, callback=self.update_coolant_temp)
        self.async_connection.watch(obd.commands.FUEL_PRESSURE, callback=self.update_fuel_pressure)
        self.async_connection.watch(obd.commands.SPEED, callback=self.update_speed)
        self.async_connection.watch(obd.commands.TIMING_ADVANCE, callback=self.update_timing_advance)
        self.async_connection.watch(obd.commands.INTAKE_TEMP, callback=self.update_intake_temp)
        self.async_connection.watch(obd.commands.MAF, callback=self.update_air_flow_rate)
        self.async_connection.watch(obd.commands.THROTTLE_POS, callback=self.update_throttle_pos)
        self.async_connection.watch(obd.commands.RUN_TIME, callback=self.update_run_time)
        self.async_connection.watch(obd.commands.COMMANDED_EGR, callback=self.update_commanded_egr)
        self.async_connection.watch(obd.commands.EGR_ERROR, callback=self.update_egr_error)
        self.async_connection.watch(obd.commands.EVAPORATIVE_PURGE, callback=self.update_evaporative_purge)
        self.async_connection.watch(obd.commands.FUEL_LEVEL, callback=self.update_fuel_level)
        self.async_connection.watch(obd.commands.EVAP_VAPOR_PRESSURE, callback=self.update_evap_vapor_pressure)
        self.async_connection.start()

    def update_rpm(self, response):
        self.latest_rpm = response.value
        print(f"RPM: {self.latest_rpm}")

    def update_engine_load(self, response):
        self.latest_engine_load = response.value
        print(f"Engine Load: {self.latest_engine_load}")

    def update_coolant_temp(self, response):
        temp_celsius = response.value
        self.latest_coolant_temp = self.celsius_to_fahrenheit(temp_celsius)
        print(f"Coolant Temperature: {self.latest_coolant_temp} °F")

    def update_fuel_pressure(self, response):
        self.latest_fuel_pressure = response.value
        print(f"Fuel Pressure: {self.latest_fuel_pressure}")

    def update_speed(self, response):
        self.latest_speed = response.value
        print(f"Speed: {self.latest_speed}")

    def update_timing_advance(self, response):
        self.latest_timing_advance = response.value
        print(f"Timing Advance: {self.latest_timing_advance}")

    def update_intake_temp(self, response):
        self.latest_intake_temp = response.value
        print(f"Intake Temp: {self.latest_intake_temp}")

    def update_air_flow_rate(self, response):
        self.latest_air_flow_rate = response.value
        print(f"Air Flow Rate: {self.latest_air_flow_rate}")

    def update_throttle_pos(self, response):
        self.latest_throttle_pos = response.value
        print(f"Throttle Position: {self.latest_throttle_pos}")

    def update_run_time(self, response):
        self.latest_run_time = response.value
        print(f"Run Time: {self.latest_run_time}")

    def update_commanded_egr(self, response):
        self.latest_commanded_egr = response.value
        print(f"Command EGR: {self.latest_commanded_egr}")

    def update_egr_error(self, response):
        self.latest_egr_error = response.value
        print(f"EGR Error: {self.latest_egr_error}")

    def update_evaporative_purge(self, response):
        self.latest_evaporative_purge = response.value
        print(f"Evaporative Purge: {self.latest_evaporative_purge}")

    def update_fuel_level(self, response):
        self.latest_fuel_level = response.value
        print(f"Fuel Level: {self.latest_fuel_level}")

    def update_evap_vapor_pressure(self, response):
        self.latest_evap_vapor_pressure = response.value
        print(f"Vapor Pressure: {self.latest_evap_vapor_pressure}")

    def update_barometric_pressure(self, response):
        self.latest_barometric_pressure = response.value
        print(f"Barometric Pressure: {self.latest_barometric_pressure}")

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return (celsius * 9/5) + 32

    def get_rpm(self):
        return self.latest_rpm

    def get_status(self):
        response = self.sync_connection.query(obd.commands.STATUS)
        if response.is_null():
            self.latest_status = "No data"
        else:
            self.latest_status = response.value
        print(f"Status: {self.latest_status}")
        return self.latest_status

    def get_freeze_dtc(self):
        response = self.sync_connection.query(obd.commands.FREEZE_DTC)
        if response.is_null():
            self.latest_freeze_dtc = "No data"
        else:
            self.latest_freeze_dtc = response.value
        print(f"Freeze DTC: {self.latest_freeze_dtc}")
        return self.latest_freeze_dtc

    def get_fuel_status(self):
        response = self.sync_connection.query(obd.commands.FUEL_STATUS)
        if response.is_null():
            self.latest_fuel_status = "No data"
        else:
            self.latest_fuel_status = response.value
        print(f"Fuel Status: {self.latest_fuel_status}")
        return self.latest_fuel_status

    def get_dtc(self):
        response = self.sync_connection.query(obd.commands.GET_DTC)
        if response.is_null():
            self.latest_dtc = "No data"
        else:
            self.latest_dtc = response.value
        print(f"DTC: {self.latest_dtc}")
        return self.latest_dtc

    def clear_dtc(self):
        response = self.sync_connection.query(obd.commands.CLEAR_DTC)
        if response.is_null():
            print("Failed to clear DTCs")
        else:
            print("DTCs cleared successfully")

    def get_latest_values(self):
        return {
            "speed": self.latest_speed,
            "rpm": self.latest_rpm,
            "engine_load": self.latest_engine_load,
            "fuel_pressure": self.latest_fuel_pressure,
            "egr_error": self.latest_egr_error,
            "fuel_level": self.latest_fuel_level,
            "coolant_temp": self.latest_coolant_temp,
            "intake_temp": self.latest_intake_temp,
            "run_time": self.latest_run_time,
            "air_flow_rate": self.latest_air_flow_rate,
            "barometric_pressure": self.latest_barometric_pressure,
            "command_egr": self.latest_commanded_egr,
            "throttle_position": self.latest_throttle_pos,
            "timing_advance": self.latest_timing_advance,
            "evaporative_purge": self.latest_evaporative_purge,
            "evap_vapor_pressure": self.latest_evap_vapor_pressure,
        }

    def close_connection(self):
        self.async_connection.stop()
        self.sync_connection.close()