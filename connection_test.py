import time
def main():
    from connections import TCPWorker
    from mock_pybricks import Motor, Port, Direction
    from sensors import UltrasonicScanner
    import constants
    from map import Map

    minimap = Map(size_x = 1,
                  size_y = 1,
                  resolution=0.01,
                  starting_position_x=0,
                  starting_position_y=0.025)
    # test_worker = TCPWorker()
    # test_worker.start()

    test_motor_left = Motor(port = Port.A,
                    positive_direction=Direction.CLOCKWISE,
                    gears=[],
                    reset_angle=False)
    test_motor_right = Motor(port = Port.B,
                    positive_direction=Direction.CLOCKWISE,
                    gears=[],
                    reset_angle=False)
    test_steering_motor = Motor(port = Port.C,
                    positive_direction=Direction.CLOCKWISE,
                    gears=[],
                    reset_angle=False)
    test_us_scanner = UltrasonicScanner(motor_port="D",
                                        sensor_port = "E",
                                        default_scan_start_deg=constants.SCAN_START,
                                        default_scan_end_deg=constants.SCAN_END,
                                        gear_ratio=constants.GEAR_RATIO)
    print("RUNNING MOTOR")
    #test_motor_left.run(100)
    #test_motor_right.run(100)
    #test_steering_motor.track_target(45)
    scan_data = test_us_scanner.sweep()
    print(scan_data)
    print("Waiting")
    time.sleep(2)
    #test_steering_motor.track_target(-45)
    #test_us_scanner.track_target(180)
    #print("RUNNING MOTOR")
    #test_motor.run(0)
    #print("Waiting")
    #time.sleep(2)
    print("FInished waiting. Sending shutdown message")
    test_motor_left.send_shutdown_message()
    test_motor_right.send_shutdown_message()
    test_steering_motor.send_shutdown_message()
    test_us_scanner.send_shutdown_message()
    
    print("Finished sending shutdown message. End of program")
    # test_worker.join()

if __name__ == "__main__":
    main()