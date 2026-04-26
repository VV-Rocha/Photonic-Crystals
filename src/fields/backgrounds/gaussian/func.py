import numpy as np
from typing import Tuple


def gaussian_25_1d(
    x,
    w: float,
    center: float,
    I: float,
    power: int,
    shape: int,
    ) -> np.ndarray:
    """ Generate a 1D Gaussian envelope field.

    Args:
        x (float | np.ndarray): -x- grid points
        w (float): width of the Gaussian
        center (float): center position of the Gaussian
        I (float): intensity of the Gaussian
        power (int): exponent power of the Gaussian
        shape (int): shape of the output array

    Returns:
        np.ndarray: The generated 1D Gaussian envelope field.
    """
    canvas = np.zeros(shape, dtype=np.complex128)
    canvas[:] = np.exp(-.5*(2*((x - center)/w)**2)**power)

    canvas /= np.max(np.abs(canvas)**2)
    
    canvas *= np.sqrt(I)
    return canvas

def gaussian_25_2d(
    x,
    y,
    width: Tuple[float, float],
    center: Tuple[float, float],
    I: float,
    power: int,
    shape: Tuple[int, int],
) -> np.ndarray:
    """ Generate a 2D Gaussian envelope field.

    Args:
        x (float | np.ndarray): -x- grid points
        y (float | np.ndarray): -y- grid points
        width (Tuple[float, float]): widths of the Gaussian in x and y directions
        center (Tuple[float, float]): center position of the Gaussian in x and y directions
        I (float): intensity of the Gaussian
        power (int): exponent power of the Gaussian
        shape (Tuple[int, int]): shape of the output array

    Returns:
        np.ndarray: The generated 2D Gaussian envelope field.
    """
    canvas = np.zeros(shape, dtype=np.complex128)
    canvas[:, :] = np.exp(-.5*(2*(((x - center[0])/width[0])**2 + ((y - center[1])/width[1])**2))**power)
    
    canvas /= np.max(np.abs(canvas)**2)
    
    canvas *= np.sqrt(I)
    
    return canvas