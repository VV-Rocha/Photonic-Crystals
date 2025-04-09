import numpy as np

from functools import wraps

from typing import Tuple

def gaussian_25_dimensions(func):
    @wraps(func)
    def wrapper(mesh, w, I, power):
        if mesh.dim_flag == "adimensional":
            w = (mesh.adim_method.adimensionalize_length(w[0]), mesh.adim_method.adimensionalize_length(w[1]))
        return func(mesh, w, I, power)
    return wrapper

def check_width(func):
    @wraps(func)
    def wrapper(mesh, w, I, power):
        if type(w) is float:
            w = (w, w)
        return func(mesh, w, I, power)
    return wrapper

@check_width
@gaussian_25_dimensions
def gaussian_25(mesh,
                w: float | Tuple[float, float],
                I: float,
                power: int,
                norm: str = "density",
                ):
    """Returns the Gaussian beam profile in 2D.

    Args:
        mesh (Mesh2D object): Mesh2D object containing the domain mesh grid.
        w (float | Tuple[float, float]): FWHM of the gaussian profile.
        I (float): Intensity of the gaussian profile. The magnitude of the field is the square root of the intensity.
        power (int): (super)Gaussian power.

    Returns:
        ndarray: Gaussian profile over the mesh grid domain.
    """
    canvas = np.zeros(mesh.XX.shape, dtype=np.complex128)
    canvas[:,:] = np.exp(-(((mesh.XX/w[0])**2 + (mesh.YY/w[1])**2))**power)
    if norm == "density":
        canvas *= np.sqrt(2/(np.pi*w[0]*w[1])) # Normalize Gaussian
    elif norm == "max":
        canvas /= np.max(np.abs(canvas)**2)
    canvas /= np.max(np.abs(canvas)**2)
    canvas *= np.sqrt(I)
    return canvas