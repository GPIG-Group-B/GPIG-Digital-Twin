try:
    from pybricks.parameters import Color
    from pybricks.pupdevices import ColorSensor, ColorDistanceSensor
    import constants
    from utils import LegoSpikeHub
    from pybricks.tools import wait
except ImportError:
    pass

# Run with constants.py and utils.py on the Rover

HUB = LegoSpikeHub()

Color.CUSTOM_GREY = Color(h=0, s=0, v=60)

ALL_COLOURS = [Color.RED,
               Color.ORANGE,
               Color.YELLOW,
               Color.GREEN,
               Color.BLUE,
               Color.VIOLET,
               Color.MAGENTA,
               Color.WHITE,
               Color.CUSTOM_GREY,
               Color.BLACK,
               Color.NONE]

COLOUR_DIST_FORWARD = ColorDistanceSensor(port=HUB.get_port_from_str(constants.COLOUR_DISTANCE_SENSOR_PORT))
COLOUR_DIST_FORWARD.detectable_colors(ALL_COLOURS)

COLOUR_BOTTOM = ColorSensor(port=HUB.get_port_from_str(constants.COLOUR_SENSOR_PORT))
COLOUR_BOTTOM.detectable_colors(ALL_COLOURS)

def detect_colour_forward():
    return (COLOUR_DIST_FORWARD.color(), COLOUR_DIST_FORWARD.hsv())

def get_distance_forward():
    return COLOUR_DIST_FORWARD.distance()

def detect_colour_secondary():
    return (COLOUR_BOTTOM.color(), COLOUR_BOTTOM.hsv())

def main():
    print("----------------------")
    wait(2000)
    print("Detecting forward colour using the colour distance sensor!")
    print(detect_colour_forward())

    print("\nDetecting distance of foward colour!")
    print(get_distance_forward())

    print("\nDetecting secondary colour!")
    print(detect_colour_secondary())

    wait(2000)

    print("Shutting down")
    try:
        COLOUR.send_shutdown_message()
        COLOUR_DIST.send_shutdown_message()
    except:
        pass
    print("All done!")
    print("----------------------")

main()


