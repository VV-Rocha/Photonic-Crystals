from typing import Tuple
from numpy import pi

class Beam:
    """Beam class holding fundamental beam properties."""
    def __init__(
        self,
        beam_config,
        *args,
        **kwargs,
        ):
        """Initialize the class holding the fundamental beam properties.

        Args:
            wavelength (float): Wavelength of light used.
            c (float): Coupling coefficient of the electric field polarization with the axis of the crystal.
        """
        self.wavelength = beam_config["wavelength"]
        self.c = beam_config["c"]
        
        self.k = 2*pi/self.wavelength
                
        super().__init__(
            beam_config = beam_config,
            *args,
            **kwargs,
            )

def second_value(key: str, beam_config: dict) -> float:
    if key in beam_config.keys():
        param = beam_config[key]
    else:
        param = beam_config[key[:-1]]
    return param

class TwoBeams(Beam):
    """Two beam class for holding fundamental beam properties."""
    def __init__(
        self,
        beam_config,
        *args,
        **kwargs,
        ):
        """Initializes the class holding the fundamental properties of two beams.

        Args:
            wavelengths (Tuple[float, float]): Tuple with the wavelength of each beam.
            cs (Tuple[float, float]): Tuple with the coupling with the medium for each beam.
            store_config (StoreConfig, optional): Class object from control.storage_config. Defaults to None.
        """
        self.wavelength1 = second_value("wavelength1", beam_config)
        self.c1 = second_value("c1", beam_config)
        
        self.k1 = 2*pi/self.wavelength1
        
        super().__init__(
            beam_config = beam_config,
            *args,
            **kwargs,
            )