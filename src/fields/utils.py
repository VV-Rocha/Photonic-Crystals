from typing import Tuple


def float_to_tuple(value) -> Tuple[float, float]:
    """ Convert a float or int to a tuple of two identical floats.

    Args:
        value (int | float): The input value to convert.

    Returns:
        Tuple[float, float]: A tuple containing two identical floats.
    """
    if type(value) is not tuple:
        value = (value*1., value*1.)
    return value