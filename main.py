from rover import Rover
import constants
from sensors import UltrasonicScanner


def main():

    ultrasonic_scanner = UltrasonicScanner(motor_port=constants.ULTRASONIC_MOTOR_PORT,
                                           sensor_port=constants.ULTRASONIC_SENSOR_PORT,
                                           default_scan_start_deg=constants.SCAN_START,
                                           default_scan_end_deg=constants.SCAN_END,
                                           gear_ratio=constants.GEAR_RATIO)

    rover = Rover(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  left_motor_port=constants.LEFT_MOTOR_PORT,
                  right_motor_port=constants.RIGHT_MOTOR_PORT,
                  steering_motor_port=constants.STEERING_MOTOR_PORT,
                  ultrasonic_scanner= ultrasonic_scanner,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    rover.drive(angle=0,
                distance=300)
    rover.scan_surroundings()




if __name__ == "__main__":
    main()