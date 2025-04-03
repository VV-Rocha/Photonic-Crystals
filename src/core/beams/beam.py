import h5py

from functools import wraps

from typing import Tuple

# % TODO: Add a method to initialize the classes from a previously stored configuration file.

class Beam:
    """Beam class holding fundamental beam properties."""
    def __init__(self,
                 wavelength: float,
                 c: float,
                 ):
        """Initialize the class holding the fundamental beam properties.

        Args:
            wavelength (float): Wavelength of light used.
            c (float): Coupling coefficient of the electric field polarization with the axis of the crystal.
        """
        self.wavelength = wavelength
        self.c = c

class TwoBeams(Beam):
    """Two beam class for holding fundamental beam properties."""
    def __init__(self,
                 wavelengths: Tuple[float, float],
                 cs: Tuple[float, float],
                 store_config = None,
                 ):
        """Initializes the class holding the fundamental properties of two beams.

        Args:
            wavelengths (Tuple[float, float]): Tuple with the wavelength of each beam.
            cs (Tuple[float, float]): Tuple with the coupling with the medium for each beam.
            store_config (StoreConfig, optional): Class object from control.storage_config. Defaults to None.
        """
        super().__init__(wavelength = wavelengths[0],
                         c = cs[0],
                         )

        self.wavelength1 = wavelengths[1]
        self.c1 = cs[1]
        
        if store_config is not None:
            self.store_beams(store_config)
        
    def store_beams(self, store_config):
        filename = store_config.get_beam_dir()
        with h5py.File(filename, "w") as f:
            f.create_dataset("wavelenghts",
                             data = (self.wavelength, self.wavelength1),
                             )
            f.create_dataset("cs",
                             data = (self.c, self.c1),
                             )
        f.close()