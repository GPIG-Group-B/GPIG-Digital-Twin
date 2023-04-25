try:
    from pybricks.parameters import Direction
    from pybricks.pupdevices import Motor, UltrasonicSensor
except:
    from mock_pybricks import Direction
    from mock_pybricks import Motor, UltrasonicSensor
from utils import convert_str_to_port


class UltrasonicScanner:
    """ Class for Ultrasonic Scanner

    Attributes:
        _motor (Motor) :
            The motor the ultrasonic sensor is attached to
        _sensor (UltrasonicSensor) :
            The ultrasonic sensor object
        _gear_ratio (float) :
            The gear ratio for the motor
        _default_scan_start_deg (int) :
            The degrees to start scan by default
        _default_scan_end_deg (int) :
            The degrees to end scan by default

    """

    def __init__(self,
                 motor_port: str,
                 sensor_port: str,
                 default_scan_start_deg: int,
                 default_scan_end_deg: int,
                 gear_ratio: float):
        """ Init method for ultrasonic scanner
        Args:
            motor_port:
                Letter port assignment for ultrasonic scanner motor
            sensor_port:
                Letter port assignment for ultrasonic sensor
            default_scan_start_deg:
                Degree to start scan by default
            default_scan_end_deg:
                Degrees to end scan by default
            gear_ratio:
                Gear ratio used on motor
        """
        print(f"Initialising sensor motor on {motor_port}")
        self._motor = Motor(port=convert_str_to_port(motor_port),
                            positive_direction=Direction.CLOCKWISE,
                            gears=[gear_ratio],
                            reset_angle=False)
        print("Completed initialising sensor motor")
        self._sensor = UltrasonicSensor(port=convert_str_to_port(sensor_port))
        self._gear_ratio = gear_ratio
        self._default_scan_start_deg = default_scan_start_deg
        self._default_scan_end_deg = default_scan_end_deg

    def custom_sweep(self,
                     scan_start_deg : int,
                     scan_end_deg : int):
        """ Method to run a sweep using custom start and end degrees

        Args:
            scan_start_deg:
                The degrees to start the scan
            scan_end_deg:
                The degrees to end the scan

        Returns:
            list[Tuple(angle, distance))] : List of angles and distance tuples
        """
        self._motor.run_target(360,
                               scan_start_deg)
        print(f"Moving US Sensor to {scan_start_deg} degrees")
        self._motor.run_target(200,
                               scan_end_deg,
                               wait=False)
        self._sensor.lights.on(100)
        scan_data = []
        while self._motor.angle() != (scan_end_deg):
            print(self._motor.angle())
            scan_data.append(self.poll())
        self._sensor.lights.off()
        self._motor.run_target(360,
                               0,
                               wait=True)
        return scan_data


    def sweep(self):
        """ Run scanner sweep using default start and end degrees

        Returns:
            list[Tuple(angle, distance))] : List of angles and distance tuples
        """
        self.custom_sweep(scan_start_deg=self._default_scan_start_deg,
                          scan_end_deg=self._default_scan_end_deg)

    def poll(self):
        """ Run a poll of the ultrasonic sensor

        Returns:
            angle sensor currently at, distance of object sensor detected
        """
        true_angle = self.get_true_angle
        detection_distance = self._sensor.distance()
        return true_angle, detection_distance

    def get_true_angle(self):
        """Utility method for getting true angle of ultrasonic sensor

        Returns:
            float : Current angle the sensor is at (not the same as the motor angle)

        """
        return self._motor.angle()
