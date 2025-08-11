from functools import wraps

from typing import Tuple

from numpy import pi

class Beam:
    """Beam class holding fundamental beam properties."""
    def __init__(self,
                 beam_config,
                 ):
        """Initialize the class holding the fundamental beam properties.

        Args:
            wavelength (float): Wavelength of light used.
            c (float): Coupling coefficient of the electric field polarization with the axis of the crystal.
        """
        self.wavelength = beam_config["wavelength"]
        self.c = beam_config["c"]
        
        self.k = 2*pi/self.wavelength

class TwoBeams(Beam):
    """Two beam class for holding fundamental beam properties."""
    def __init__(
        self,
        beam_config,         
        ):
        """Initializes the class holding the fundamental properties of two beams.

        Args:
            wavelengths (Tuple[float, float]): Tuple with the wavelength of each beam.
            cs (Tuple[float, float]): Tuple with the coupling with the medium for each beam.
            store_config (StoreConfig, optional): Class object from control.storage_config. Defaults to None.
        """
        super().__init__(beam_config=beam_config)

        self.wavelength1 = beam_config["wavelength1"]
        self.c1 = beam_config["c1"]
        