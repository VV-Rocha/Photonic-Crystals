import numpy as np

def whitenoise_field(
    A: float,
    shape,
    ) -> np.ndarray:
    """ Generate a white noise field with given amplitude and shape.

    Args:
        A (float): Amplitude of the noise.
        shape (int | tuple): Shape of the noise array.

    Returns:
        np.ndarray: Generated white noise array.
    """
    new_field = np.random.normal(0,
                       scale=A,
                       size=shape,
                       )
    return new_field

def introduce_noise(
    field: np.ndarray,
    A: float,
    ) -> None:
    """ Introduce white noise into the given field.

    Args:
        field (np.ndarray): Field to which noise will be added.
        A (float): Amplitude of the noise.
    """
    field *= (1. + whitenoise_field(A, field.shape))