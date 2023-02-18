class Port:
    A = ("localhost", 65432)
    B = ("localhost", 65433)
    C = ("localhost", 65434)
    D = ("localhost", 65435)
    E = ("localhost", 65436)
    F = ("localhost", 65437)

class Direction:

    COUNTER_CLOCKWISE = "counter_clockwise"
    CLOCKWISE = "clockwise"

class Motor:

    def __init__(self,
                 port : Port,
                 positive_direction : Direction):
        self.port = port
        self.positive_direction = positive_direction

