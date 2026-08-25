
from .base import Field, Modulation

from .noise.noise import WhitenoiseField

from .backgrounds.gaussian_1d import Gaussian1D
from .landscapes.landscape import PhaseStep, Plane, DarkSoliton

class PhaseStepGaussian1D(Gaussian1D, PhaseStep, Modulation, Field, WhitenoiseField):
    """ Phase Step Gaussian 1D Field Class."""
    def __init__(
        self,
        modulation_config: dict,
        *args,
        **kwargs,
    ):
        """ Initialize Phase Step Gaussian 1D Field.

        Args:
            modulation_config (dict): Modulation configuration dictionary, having keys:
                - "envelope_config": dictionary containing the configuration for the Gaussian envelope.
                - "landscape_config": dictionary containing the configuration for the phase step landscape.
        """
        super().__init__(
            envelope_config = modulation_config["envelope_config"],
            landscape_config = modulation_config["landscape_config"],
            *args,
            **kwargs,
        )
        
class PlaneGaussian1D(Gaussian1D, Plane, Modulation, Field, WhitenoiseField):
    """ Plane Wave Gaussian 1D Field Class."""
    def __init__(
        self,
        modulation_config: dict,
        *args,
        **kwargs,
    ):
        """ Initialize Plane Wave Gaussian 1D Field.

        Args:
            modulation_config (dict): Modulation configuration dictionary, having keys:
                - "envelope_config": dictionary containing the configuration for the Gaussian envelope.
        """
        super().__init__(
            envelope_config = modulation_config["envelope_config"],
            landscape_config = {},
            *args,
            **kwargs,
        )
        
class DarkSolitonGaussian1D(Gaussian1D, DarkSoliton, Modulation, Field, WhitenoiseField):
    """ Dark Soliton Gaussian 1D Field Class."""
    def __init__(
        self,
        modulation_config: dict,
        *args,
        **kwargs,
    ):
        """ Initialize Dark Soliton Gaussian 1D Field.

        Args:
            modulation_config (dict): Modulation configuration dictionary, having keys:
                - "envelope_config": dictionary containing the configuration for the Gaussian envelope.
                - "landscape_config": dictionary containing the configuration for the dark soliton landscape.
        """
        super().__init__(
            envelope_config = modulation_config["envelope_config"],
            landscape_config = modulation_config["landscape_config"],
            *args,
            **kwargs,
        )