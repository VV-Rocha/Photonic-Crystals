import numpy as np
from typing import Tuple

def gaussian_25_1d(
    x: float | np.ndarray,
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
    x: float | np.ndarray,
    y: float | np.ndarray,
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

def float_to_tuple(value: int | float) -> Tuple[float, float]:
    """ Convert a float or int to a tuple of two identical floats.

    Args:
        value (int | float): The input value to convert.

    Returns:
        Tuple[float, float]: A tuple containing two identical floats.
    """
    if type(value) is not tuple:
        value = (value*1., value*1.)
    return value

class GaussianConfig1D:
    """ 1D Gaussian background field configuration."""
    def __init__(
        self,
        envelope_config: dict,
        *args,
        **kwargs,
        ):
        """ Initialize the Gaussian configuration.

        Args:
            envelope_config (dict): Configuration dictionary for the Gaussian envelope. keys include:
                - "I": Intensity of the Gaussian envelope.
                - "width": Width of the Gaussian envelope.
                - "center": Center position of the Gaussian envelope.
                - "exponent": Exponent for the Gaussian envelope.
        """
        self.I = envelope_config["I"]
        self.width = envelope_config["width"]
        self.center = envelope_config["center"]
        self.exponent = envelope_config["exponent"]
        super().__init__(
            *args,
            **kwargs,
            )
        
    def adimensionalize_envelope(self,):
        """ Adimensionalize the parameters of the Gaussian envelope."""
        self.width = self.adimensionalize_length(self.width)
        self.center = self.adimensionalize_length(self.center)
        
class GaussianConfig2D:
    """ 2D Gaussian background field configuration."""
    def __init__(
        self,
        envelope_config: dict,
        *args,
        **kwargs,
    ):
        """Initialize the Gaussian configuration.

        Args:
            envelope_config (dict): Configuration dictionary for the Gaussian envelope. keys include:
                - "I": Intensity of the Gaussian envelope.
                - "width": Width of the Gaussian envelope.
                - "center": Center position of the Gaussian envelope.
                - "exponent": Exponent for the Gaussian envelope.
        """
        self.I = envelope_config["I"]
        self.width = float_to_tuple(envelope_config["width"])
        self.center = float_to_tuple(envelope_config["center"])
        self.exponent = envelope_config["exponent"]
        super().__init__(
            *args,
            **kwargs,
        )
    
    def adimensionalize_envelope(self,):
        """ Adimensionalize the parameters of the Gaussian envelope."""
        self.width = (self.adimensionalize_length(self.width[0]), self.adimensionalize_length(self.width[1]))
        self.center = (self.adimensionalize_length(self.center[0]), self.adimensionalize_length(self.center[1]))
        
class CoupledGaussianConfig2D(GaussianConfig2D):
    """ Configuration class for coupled 2D Gaussian envelopes."""
    def __init__(
        self,
        envelope1_config: dict,
        *args,
        **kwargs,
    ):
        """ Initialize the coupled Gaussian configuration.
        
        Args:
            envelope1_config (dict): Configuration dictionary for the second Gaussian envelope. keys include:
                - "I": Intensity of the Gaussian envelope.
                - "width": Width of the Gaussian envelope.
                - "center": Center position of the Gaussian envelope.
                - "exponent": Exponent for the Gaussian envelope.
        """
        self.I1 = envelope1_config["I"]
        self.width1 = float_to_tuple(envelope1_config["width"])
        self.center1 = float_to_tuple(envelope1_config["center"])
        self.exponent1 = envelope1_config["exponent"]        
        super().__init__(
            *args,
            **kwargs,
        )

    def adimensionalize_envelope(self,):
        """ Adimensionalize the parameters of both Gaussian envelopes."""
        super().adimensionalize_envelope()
        self.width1 = (self.adimensionalize_length(self.width1[0]), self.adimensionalize_length(self.width1[1]))
        self.center1 = (self.adimensionalize_length(self.center1[0]), self.adimensionalize_length(self.center1[1]))
