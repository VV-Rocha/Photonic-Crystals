from .backgrounds.gaussian_2d import CoupledGaussian2D

from .base import CoupledModulation, CoupledFields

from .noise.noise import WhitenoiseCoupledFields

from .landscapes.landscapes_2d import MoireLattice

class SecondMoireLatticeGaussian2D(CoupledGaussian2D, MoireLattice, CoupledModulation, CoupledFields, WhitenoiseCoupledFields):
    """ Second Moire Lattice Gaussian 2D Coupled Field Class."""
    def __init__(
        self,
        modulation_config: dict,
        *args,
        **kwargs,
    ):
        """ Initialize Second Moire Lattice Gaussian 2D Coupled Field.

        Args:
            modulation_config (dict): Modulation configuration dictionary, having keys:
                - "landscape_config": dictionary containing the configuration for the first moire lattice landscape.
                - "landscape1_config": dictionary containing the configuration for the second moire lattice landscape.
                - "envelope_config": dictionary containing the configuration for the Gaussian envelope of the first field.
                - "envelope1_config": dictionary containing the configuration for the Gaussian envelope of the second field.
        """
        super().__init__(
            landscape_config = modulation_config["landscape_config"],
            landscape1_config = modulation_config["landscape1_config"],
            envelope_config = modulation_config["envelope_config"],
            envelope1_config = modulation_config["envelope1_config"],
            *args,
            **kwargs,
            )