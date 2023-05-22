try:
    from pybricks.parameters import Color
    from pybricks.pupdevices import ColorSensor, ColorDistanceSensor
    import constants
    from utils import LegoSpikeHub
    from colour_test_cases import COLOUR_TESTS
except ImportError:
    pass


HUB = LegoSpikeHub()

ALL_COLOURS = [Color.RED,
               Color.ORANGE,
               Color.YELLOW,
               Color.GREEN,
               Color.BLUE,
               Color.VIOLET,
               Color.MAGENTA,
               Color.WHITE,
               Color.BLACK,
               Color.NONE]

COLOUR_DIST_FORWARD = ColorDistanceSensor(port=HUB.get_port_from_str(constants.COLOUR_DISTANCE_SENSOR_PORT))
COLOUR_DIST_FORWARD.detectable_colors(ALL_COLOURS)

COLOUR_BOTTOM = ColorSensor(port=HUB.get_port_from_str(constants.COLOUR_SENSOR_PORT))
COLOUR_BOTTOM.detectable_colors(ALL_COLOURS)

def detect_colour_forward():
    print(COLOUR_DIST_FORWARD.color(), COLOUR_DIST_FORWARD.hsv())

def detect_distance_forward():
    print(COLOUR_DIST_FORWARD.distance())

def detect_colour_secondary():
    print((COLOUR_BOTTOM.color(), COLOUR_BOTTOM.hsv()))

def run_test_case(test_id):
    parameters = COLOUR_TESTS[test_id]
    if parameters["sensor"] == "front":
        detect_colour_forward()
        detect_distance_forward()
        
    elif parameters["sensor"] == "floor":
        detect_colour_secondary()

def main():
    test_id = "CD_BLUE"

    print("----------------------")
    print(f"Starting test with ID = {test_id}.")
    print("----------------------")

    run_test_case(test_id)
    print("Test Complete")

main()


