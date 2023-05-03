class PortIPStruct:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

class LegoSpikeHub:

    A = "who knows"

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
            self.port_a = PortIPStruct(ip = "localhost", port = 65490)
            self.port_b = PortIPStruct(ip="localhost", port=65491)
            self.port_c = PortIPStruct(ip="localhost", port=65492)
            self.port_d = PortIPStruct(ip="localhost", port=65493)
            self.port_e = PortIPStruct(ip="localhost", port=65494)
            self.port_f = PortIPStruct(ip="localhost", port=65495)

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
            self.port_a = PortIPStruct(ip = "localhost", port = 65496)
            self.port_b = PortIPStruct(ip="localhost", port=65497)
            self.port_c = PortIPStruct(ip="localhost", port=65498)
            self.port_d = PortIPStruct(ip="localhost", port=65499)

        self.str_conversion_dict = {"A" : self.port_a,
                                    "B" : self.port_b,
                                    "C" : self.port_c,
                                    "D" : self.port_d}

    def get_port_from_str(self, port_as_string):
        return self.str_conversion_dict[port_as_string.upper()]

