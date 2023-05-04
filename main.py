from rover_spike_hub import RoverSpikeHub
import constants
from sensors import UltrasonicScanner


def main():
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)
    print("Pre-scan")
    rover.scan_surroundings()
    print("Scan complete")
    print("Pre-Drive")
    rover.drive(angle=0,
                distance=100)
    print("Driven")
    rover.shutdown()
    print("All done!")




if __name__ == "__main__":
    main()