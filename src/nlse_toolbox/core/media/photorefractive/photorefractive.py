import numpy as np
from dataclasses import dataclass

from .delta_n_max import _delta_n_max


@dataclass
class BeamMediumProperties:
    wavelength: float
    n: float
    electro_optic_coef: float
    alpha: float
    c: float


@dataclass
class CrystalSharedProperties:
    tension: float
    Isat: float
    Lx: float
    Ly: float
    Lz: float


class PhotorefractiveCrystal:
    """A class representing a photorefractive crystal parameters with a single incident beam."""
    def __init__(
        self,
        crystal_config,
        *args,
        **kwargs,
        ):
        """Initialize the photorefractive crystal when a single beam is being used.

        Args:
            crystal_config (dict): Dictionary with all the physical parameters required to initiate the object.
        """
        self.shared_properties = CrystalSharedProperties(**crystal_config["shared"])
        
        self.init_beam_medium_properties(crystal_config["beam_properties"])
                        
        super().__init__(
            *args,
            **kwargs,
            )
        
    def init_beam_medium_properties(
        self,
        beam_properties_config,
    ):
        self.medium_beams = {}
        for beam_key, beam_properties in beam_properties_config.items():
            self.medium_beams[beam_key] = BeamMediumProperties(**beam_properties)
            
            self.medium_beams[beam_key].delta_n_max = _delta_n_max(
                self.medium_beams[beam_key].n,
                self.medium_beams[beam_key].electro_optic_coef,
                self.shared_properties.tension,
                self.shared_properties.Lx,
            )
            
            self.medium_beams[beam_key].k = 2 * np.pi / self.medium_beams[beam_key].wavelength