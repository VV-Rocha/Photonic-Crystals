import numpy as np
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

    def adimensionalize_envelope1(self,):
        """ Adimensionalize the parameters of both Gaussian envelopes."""
        self.width1 = (self.adimensionalize_length(self.width1[0]), self.adimensionalize_length(self.width1[1]))
        self.center1 = (self.adimensionalize_length(self.center1[0]), self.adimensionalize_length(self.center1[1]))
        
class CoupledBesselGaussianConfig2D(GaussianConfig2D):
    def __init__(
        self,
        envelope1_config: dict,
        *args,
        **kwargs,
    ):
        self.kr = envelope1_config["kr"]
        
        super().__init__(
            *args,
            **kwargs,
        )
        
    def adimensionalize_envelope1(self,):
        """ Adimensionalize the parameters of both Gaussian envelopes."""
        self.kr = self.dimensionalize_length(self.kr)  # inverse of length (dimensionalization <-> adimensionalization)

class Uniform1Config:
    def __init__(
        self,
        envelope1_config,
        *args,
        **kwargs
    ):
        self.I1 = envelope1_config["I"]
        super().__init__(*args, **kwargs)
    
    def adimensionalize_envelope1(self,):
        pass