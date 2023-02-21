from connections import TCPWorker
from mock_pybricks import Motor, Port, Direction

test_worker = TCPWorker()
test_worker.start()
test_motor = Motor(port = Port.A,
                   positive_direction=Direction.CLOCKWISE,
                   gears=[],
                   reset_angle=False)
test_motor.run(4)
test_worker.join()