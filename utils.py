from pybricks.parameters import Port


def convert_str_to_port(
        port_as_string: str):
    """Utility method for getting the pybricks Port object from a string

    Args:
        port_as_string:
            The port letter as a string to convert

    Returns:
        Pybricks Port object

    """
    conversion_dict = {"A": Port.A,
                       "B": Port.B,
                       "C": Port.C,
                       "D": Port.D,
                       "E": Port.E,
                       "F": Port.F}
    if port_as_string not in conversion_dict:
        raise ValueError(f"Port identifier string must be one of {conversion_dict.keys()}")

    return conversion_dict[port_as_string]