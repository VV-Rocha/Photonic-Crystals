import numpy as np

def phase_step(
    x: np.ndarray,
    a: float=0.,
    b: float=np.pi
) -> np.ndarray:
    """ Generate a phase step landscape.

    Args:
        x (np.ndarray): -x- coordinate array.
        a (float, optional): Constant phase for x<=0. Defaults to 0..
        b (float, optional): Constant phase for x>0. Defaults to np.pi.

    Returns:
        np.ndarray: _description_
    """
    phase_field = np.zeros(x.shape, dtype=np.complex128)
    phase_field[np.where(x<=0.)] = np.exp(1j*a)
    phase_field[np.where(x>0.)] = np.exp(1j*b)
    return phase_field