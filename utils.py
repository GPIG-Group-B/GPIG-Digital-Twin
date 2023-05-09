class PortIPStruct:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

class LegoSpikeHub:

    def __init__(self):
        try:
            from pybricks.parameters import Port
            self.port_a = Port.A
            self.port_b = Port.B
            self.port_c = Port.C
            self.port_d = Port.D
            self.port_e = Port.E
            self.port_f = Port.F
        except ImportError:
            self.port_a = PortIPStruct(ip = "localhost", port = 60001)
            self.port_b = PortIPStruct(ip="localhost", port=60002)
            self.port_c = PortIPStruct(ip="localhost", port=60003)
            self.port_d = PortIPStruct(ip="localhost", port=60004)
            self.port_e = PortIPStruct(ip="localhost", port=60005)
            self.port_f = PortIPStruct(ip="localhost", port=60006)

        self.str_conversion_dict = {"A" : self.port_a,
                                    "B" : self.port_b,
                                    "C" : self.port_c,
                                    "D" : self.port_d,
                                    "E" : self.port_e,
                                    "F" : self.port_f}

    def get_port_from_str(self, port_as_string):
        return self.str_conversion_dict[port_as_string.upper()]


class PoweredUpHub:


    def __init__(self):
        try:
            from pybricks.parameters import Port
            self.port_a = Port.A
            self.port_b = Port.B
            self.port_c = Port.C
            self.port_d = Port.D
        except:
            self.port_a = PortIPStruct(ip = "localhost", port = 60007)
            self.port_b = PortIPStruct(ip="localhost", port=60008)
            self.port_c = PortIPStruct(ip="localhost", port=60009)
            self.port_d = PortIPStruct(ip="localhost", port=60010)

        self.str_conversion_dict = {"A" : self.port_a,
                                    "B" : self.port_b,
                                    "C" : self.port_c,
                                    "D" : self.port_d}

    def get_port_from_str(self, port_as_string):
        return self.str_conversion_dict[port_as_string.upper()]

