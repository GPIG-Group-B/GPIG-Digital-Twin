import time
def main():
    from connections import TCPWorker
    from mock_pybricks import Motor, Port, Direction
    # test_worker = TCPWorker()
    # test_worker.start()
    test_motor = Motor(port = Port.A,
                    positive_direction=Direction.CLOCKWISE,
                    gears=[],
                    reset_angle=False)
    print("RUNNING MOTOR")
    test_motor.run(100)
    print("Waiting")
    time.sleep(2)
    #print("RUNNING MOTOR")
    #test_motor.run(0)
    #print("Waiting")
    #time.sleep(2)
    print("FInished waiting. Sending shutdown message")
    test_motor.send_shutdown_message()
    print("Finished sending shutdown message. End of program")
    # test_worker.join()

if __name__ == "__main__":
    main()