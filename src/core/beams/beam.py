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

class TwoBeams:
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
        self._beam = Beam(wavelengths[0],
                             cs[0],
                             )
        self._beam1 = Beam(wavelengths[1],
                             cs[1],
                             )
        
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
        
    @property
    def wavelength(self,):
        return self._beam.wavelength
    
    @wavelength.setter
    def wavelength(self, new_wavelength):
        self._beam.wavelength = new_wavelength
        
    @property
    def c(self,):
        return self._beam.c
    
    @c.setter
    def c(self, new_c):
        self._beam.c = new_c
        
    @property
    def wavelength1(self,):
        return self._beam1.wavelength
    
    @wavelength1.setter
    def wavelength1(self, new_wavelength):
        self._beam1.wavelength = new_wavelength
        
    @property
    def c1(self,):
        return self._beam1.c
    
    @c1.setter
    def c1(self, new_c1):
        self._beam1.c = new_c1