try:
    from pybricks.parameters import Color
    from pybricks.pupdevices import ColorSensor, ColorDistanceSensor
    import constants
    from utils import LegoSpikeHub
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
               Color.GRAY,
               Color.BLACK,
               Color.NONE]

COLOUR_DIST = ColorDistanceSensor(port=HUB.get_port_from_str(constants.COLOUR_DISTANCE_SENSOR_PORT))
COLOUR_DIST.detectable_colors(ALL_COLOURS)

COLOUR = ColorSensor(port=HUB.get_port_from_str(constants.COLOUR_SENSOR_PORT))
COLOUR.detectable_colors(ALL_COLOURS)

def detect_colour_primary():
    return COLOUR_DIST.color()

def get_distance_forward():
    return COLOUR_DIST.distance()

def detect_colour_secondary():
    return COLOUR.color()

def main():
    print("----------------------")

    print("Detecting forward colour!")
    print(detect_colour_primary())

    print("Detecting distance of foward colour!")
    print(get_distance_forward())

    print("Detecting secondary colour!")
    print(detect_colour_secondary())

    print("Shutting down")
    try:
        COLOUR.send_shutdown_message()
        COLOUR_DIST.send_shutdown_message()
    except:
        pass
    print("All done!")

main()


