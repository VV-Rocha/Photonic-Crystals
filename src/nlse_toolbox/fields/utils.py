import numpy as np
from typing import Tuple


class _BeamInitMixin:
    def __init__(
        self,
        landscape_config,
        envelope_config,
        dynamics=True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics

        super().__init__(
            *args,
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            **kwargs,
        )


def float_to_tuple(value) -> Tuple[float, float]:
    """ Convert a float or int to a tuple of two identical floats.

    Args:
        value (int | float): The input value to convert.

    Returns:
        Tuple[float, float]: A tuple containing two identical floats.
    """
    if type(value) is np.ndarray:
        value = tuple(i for i in value)
    if type(value) is not tuple:
        value = (value*1., value*1.)
    return value