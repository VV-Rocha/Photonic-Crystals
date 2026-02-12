import numpy as np

class DarkSolitonConfig:
    def __init__(
        self,
        landscape_config: dict,
        *args,
        **kwargs,
        ):
        """ Initialize Dark Soliton landscape configuration.

        Args:
            landscape_config (dict): Configuration dictionary containing parameters for the dark soliton. keys include:
                - "width": Width of the dark soliton.
                - "center": Center position of the dark soliton.
                - "exponent": Exponent defining the shape of the dark soliton.
                - "ratio": Depth ratio of the dark soliton.
        """
        self.width_env = landscape_config["width"]
        self.center_env = landscape_config["center"]
        self.exponent_env = landscape_config["exponent"]
        self.ratio_env = landscape_config["ratio"]
        super().__init__(*args, **kwargs)
        
    def adimensionalize_landscape(self,):
        """ Adimensionalize the landscape parameters."""
        self.width_env = self.adimensionalize_length(self.width_env)
        self.center_env = self.adimensionalize_length(self.center_env)
        
def dip(
    x: np.ndarray,
    r: float,
    w: float,
    center: float,
    power: int,
    shape: int,
    ) -> np.ndarray:
    """ Generate a dark soliton (dip) landscape.

    Args:
        x (np.ndarray): -x- coordinates meshgrid.
        r (float): ratio of the dip depth.
        w (float): width of the dip.
        center (float): center position of the dip.
        power (int): exponent defining the shape of the dip.
        shape (int | Tuple[int, int]): shape of the output array.

    Returns:
        np.ndarray: Dark soliton landscape array.
    """
    canvas = np.zeros(shape, dtype=np.complex128)
    canvas[:] = np.exp(-.5*(2*((x - center)/w)**2)**power)

    canvas /= np.max(np.abs(canvas))
    
    return 1. - canvas * r**2