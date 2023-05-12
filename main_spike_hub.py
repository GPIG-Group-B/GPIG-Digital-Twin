from rover_spike_hub import RoverSpikeHub
import constants
try:
    from pybricks.tools import wait
except ImportError:
    from mock_pybricks import wait


def main():
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    print("Let's drive!")
    complete = rover.drive(angle=0,
                distance=-500)
    if complete:
        print("Drive successful")
    else:
        print("Aborted! Let's go back!")
        rover.drive(angle=0,
                distance=50)
        print("Safe and sound!")
    wait(10)


    print("Shutting down")
    rover.shutdown()
    print("All done!")




if __name__ == "__main__":
    main()