# % TODO: Later change this code to enable to import the function that makes the lattice and beam as a input variable.

import h5py

from functools import wraps
from typing import Tuple

from ..core.control.storage_config import CoupledStorageConfig

# % TODO: The lattice_method should receive an object with all the parameters of the lattice. The use of the parameters should be regulated inside the lattice_method function. Towards this goal, remove the lattice_method out of the LatticeConfig class and create a new class Lattice that will be used to create the lattice. The Lattice class should have a method that will return the lattice_method function. The LatticeConfig class should be used to set the parameters of the lattice and the Lattice class should be used to create the lattice.

# % TODO: Add a method to initialize the objects from a previously stored hdf5 file. This method should receive a StoreConfig and find the required files automatically.

class LatticeConfig:
    """Class to store the lattice configuration variables."""
    # % TODO: Change this class to be a @dataclass to avoid the heavy text. The storing and loading methods should be moved outside this class.
    def __init__(self,
                 lattice_parameter: float | Tuple[float, ...],
                 p: float | Tuple[float, ...]=1.,
                 rotation: float | Tuple[float, ...]=(0., 0.),
                 store_config = None,
                 ):
        """Initializes the lattice configuration variables.

        Args:
            lattice_parameter (float | Tuple[float, ...]): Lattice parameters with dimensions
            p (float | Tuple[float, ...], optional): Constant multiplicative factor. Defaults to (1., 1.).
            rotation (float | Tuple[float, ...], optional): Rotation of the lattice(s). Defaults to (0., 0.).
            store_config (StorageConfig, optional): StorageConfig objects containing the directories where the files are stored. Defaults to None.
        """
        self.lattice_parameter = lattice_parameter
        self.p = p
        self.rotation = rotation
        if self.lattice_parameter is not None:
            if type(self.lattice_parameter) == float:
                self.a = self.lattice_parameter
            else:
                self.a = self.lattice_parameter[0]
            
    def store_lattice(self, store_config):
        """Stores the lattice parameters in a hdf5 file.
        The lattice parameters are stored with the key "lattice_parameter", p with the key "p" and rotation with the key 'rotation'."""
        filename = store_config.get_input_dir()
        with h5py.File(filename, "a") as f:
            f.create_dataset("lattice_parameter", data=self.lattice_parameter)
            f.create_dataset("p", data=self.p)
            f.create_dataset("rotation", data=self.rotation)
        f.close()


class Lattice(LatticeConfig):
    """Class to define the lattice and lattice method."""
    def __init__(self,
                 lattice_parameter: float | Tuple[float, ...],
                 p: float | Tuple[float, ...] = (1., 1.),
                 rotation: float | Tuple[float, ...] = (0., 0.),
                 store_config = None,
                 lattice_method = None,
                 **kwargs
                 ):
        """Initializes the lattice configuration.

        Args:
            lattice_parameter (float | Tuple[float, ...]): Lattice parameters with dimensions
            p (float | Tuple[float, ...], optional): Constant multiplicative factor. Defaults to (1., 1.).
            rotation (float | Tuple[float, ...], optional): Rotation of the lattice(s). Defaults to (0., 0.).
            store_config (StoreConfig, optional): StorageConfig objects containing the directories where the files are stored. Defaults to None.
            lattice_method (func, optional): Function returning the lattice landscape. If no function is given the field defaults to a constant landscape. Defaults to None.
        """
        super().__init__(lattice_parameter = lattice_parameter,
                         p = p,
                         rotation = rotation,
                         store_config = store_config,
                         )
        if lattice_method is None:
            self.landscape = lambda mesh: 1.
        else:
            self.landscape = lambda mesh: lattice_method(mesh,
                                                   lattice_parameter,
                                                   p,
                                                   rotation,
                                                   )
    
class UniformBeamConfig:
    def __init__(self, I, *args, **kwargs):
        self.I = I
        super().__init__(*args,
                         **kwargs,
                         )
    
    def modulation_function(self,
                            mesh = None,
                            ):
        from numpy import sqrt
        return sqrt(self.I)
    
class LatticeUniformConfig(UniformBeamConfig, Lattice):
    def __init__(self,
                 lattice_parameter: float | Tuple[float, ...],
                 p: float | Tuple[float, ...] = 1.,
                 rotation: float | Tuple[float, ...] = (0., 0.),
                 I: float = 1.,
                 lattice_method=None,
                 store_config=None,
                 ):
        super().__init__(lattice_parameter = lattice_parameter,
                         p = p,
                         rotation = rotation,
                         I = I,
                         lattice_method = lattice_method,
                         store_config = store_config,
                         )
        
        self.beam = LatticeGaussianBeamConfig(lattice_parameter,
                                               p,
                                               rotation,
                                               I,
                                               lattice_method = lattice_method,
                                               store_config = None,
                                               )
            
def cache_import_function(init_func):
    @wraps(init_func)
    def wrapper(self, width, center, I, power, *args, **kwargs):
        from .backgrounds.gaussian_profiles import gaussian_25
        GaussianBeamConfig._gaussian = gaussian_25
        return init_func(self, width, center, I, power, *args, **kwargs)
    return wrapper
 
class GaussianBeamConfig:
    """Class to define the Gaussian beam shape."""
    @cache_import_function
    def __init__(self,
                 width: float | Tuple[float, float],
                 center: float | Tuple[float, float],
                 I: float,
                 power: int = 1,
                 store_config = None,
                 **kwargs,
                 ):
        """Initializes the Gaussian beam configuration.
        The Gaussian beam is defined by its width, intensity and power.

        Args:
            width (float | Tuple[float, float]): FWHM of the Gaussian beam. If a tuple is given, the first element is the width in x direction and the second element is the width in y direction. Given a float the width is the same in both directions.
            I (float): Intensity of the Gaussian beam. The amplitude of the Gaussian beam is given by the square root of the intensity.
            power (int, optional): (super)Gaussian power. Defaults to 1.
            store_config (StoreConfig object, optional): StoreConfig object containing the directories on which to store the configuration. Defaults to None.
        """
        self.width = width
        self.center = center
        self.power = power
        self.I = I
        
        super().__init__(store_config=store_config,
                         **kwargs,
                         )
        
    def modulation_function(self, mesh):
        """Returns the Gaussian beam profile.

        Args:
            mesh (Mesh2D object): Mesh2D object of the domain of the modulation function.

        Returns:
            ndarray: Gaussian beam profile.
        """
        return self.__class__._gaussian(mesh = mesh,
                                        w = self.width,
                                        center = self.center,
                                        I = self.I,
                                        power = self.power,
                                        )
        
    def if_file(func):
        @wraps(func)
        def wrapper(self, file, *args, **kwargs):
            if isinstance(file, h5py.File):
                return func(self, file, *args, **kwargs)
            else:
                filename = file.get_input_dir()
                with h5py.File(filename, "w") as f:
                    func(self, f, *args, **kwargs)
                f.close()
        return wrapper
        
    @if_file
    def store_envelope(self, file: h5py.File):
        """Stores the Gaussian beam parameters in a hdf5 file.

        Args:
            file (h5py.File, optional): Can be an open instance of h5py.File to which the parameteres are appended or the StoreConfig object containing the directories where the files are stored.
        """
        file.create_dataset("width", data=self.width)
        file.create_dataset("power", data=self.power)
        file.create_dataset("I", data=self.I)
        
class LatticeGaussianBeamConfig(GaussianBeamConfig, Lattice):
    """Class to define the Gaussian beam profile with a lattice landscape."""
    def __init__(self,
                 lattice_parameter: float | Tuple[float, ...] = None,
                 p: float | Tuple[float, ...] = 1.,
                 rotation: float | Tuple[float, ...] = (0., 0.),
                 width: float | Tuple[float, float] = 1.,
                 center: float | Tuple[float, float] = (0., 0.),
                 power: int = 1,
                 I: float = 1.,
                 lattice_method=None,
                 store_config=None,
                 ):
        """Initializes the Gaussian beam configuration with a lattice landscape.

        Args:
            lattice_parameter (float | Tuple[float, ...]): Lattice parameters with dimensions
            p (float | Tuple[float, ...], optional): Constant multiplicative factor. Defaults to (1., 1.).
            rotation (float | Tuple[float, ...], optional): Rotation of the lattice(s). Defaults to (0., 0.).
            
            width (float | Tuple[float, float]): FWHM of the Gaussian beam. If a tuple is given, the first element is the width in x direction and the second element is the width in y direction. Given a float the width is the same in both directions.
            power (int, optional): (super)Gaussian power. Defaults to 1.
            I (float): Intensity of the Gaussian beam. The amplitude of the Gaussian beam is given by the square root of the intensity.
            
            lattice_method (func, optional): Function returning the lattice landscape. If no function is given the field defaults to a constant landscape. Defaults to None.
            store_config (StorageConfig, optional): StorageConfig objects containing the directories where the files are stored. Defaults to None.
        """
        super().__init__(lattice_parameter = lattice_parameter,
                         p = p,
                         rotation = rotation,
                         width = width,
                         center = center,
                         power = power,
                         I = I,
                         lattice_method = lattice_method,
                         store_config = store_config,
                         )
        
        if store_config is not None:
            self.store_config = store_config
            self.store_properties(store_config)
        
    def store_properties(self,
                         store_config,
                         ):
        """Stores the properties of the Gaussian beam and the lattice in a hdf5 file.

        Args:
            store_config (StoreConfig object): StoreConfig object containing the directories where the files are stored.
        """
        self.store_envelope(store_config)
        try:
            self.store_lattice(store_config)
        except:
            print("Lattice not defined.")


class LatticeGaussianCoupledConfig:
    """Class to define the Gaussian beam profile with a modulated lattice landscape."""
    def __init__(self,
                 lattice_parameter: float | Tuple[float, ...],
                 lattice1_parameter: float | Tuple[float, ...],
                 p: float | Tuple[float, ...],
                 p1: float | Tuple[float, ...],
                 rotation: float | Tuple[float, ...],
                 rotation1: float | Tuple[float, ...],
                 width: float | Tuple[float, float],
                 width1: float | Tuple[float, float],
                 power: int,
                 power1: int,
                 I: float,
                 I1: float,
                 center: float | Tuple[float, float] = (0., 0.),
                 center1: float | Tuple[float, float] = (0., 0.),
                 lattice_method = None,
                 lattice1_method = None,
                 store_config = None,
                 ):
        """Initializes two (super)Gaussian fields with a lattice landscape.
        
        Args:
            lattice_parameter (float | Tuple[float, ...]): (first) Lattice parameters with dimensions
            lattice1_parameter (float | Tuple[float, ...]): (second) Lattice parameters with dimensions
            p (float | Tuple[float, ...]): (first) Constant multiplicative factor. Defaults to (1., 1.).
            p1 (float | Tuple[float, ...]): (second) Constant multiplicative factor. Defaults to (1., 1.).
            rotation (float | Tuple[float, ...]): (first) Rotation of the lattice(s). Defaults to (0., 0.).
            rotation1 (float | Tuple[float, ...]): (second) Rotation of the lattice(s). Defaults to (0., 0.).
            width (float | Tuple[float, float]): (first) FWHM of the Gaussian beam. If a tuple is given, the first element is the width in x direction and the second element is the width in y direction. Given a float the width is the same in both directions.
            width1 (float | Tuple[float, float]): (second) FWHM of the Gaussian beam. If a tuple is given, the first element is the width in x direction and the second element is the width in y direction. Given a float the width is the same in both directions.
            power (int): (first) (super)Gaussian power. Defaults to 1.
            power1 (int): (second) (super)Gaussian power. Defaults to 1.
            I (float): (first) Intensity of the Gaussian beam. The amplitude of the Gaussian beam is given by the square root of the intensity.
            I1 (float): (second) Intensity of the Gaussian beam. The amplitude of the Gaussian beam is given by the square root of the intensity.
            lattice_method (func, optional): (first) Function returning the lattice landscape. If no function is given the field defaults to a constant landscape. Defaults to None.
            lattice1_method (func, optional): (second) Function returning the lattice landscape. If no function is given the field defaults to a constant landscape. Defaults to None.
            store_config (_type_, optional): StorageConfig objects containing the directories where the files are stored. Defaults to None.
        """
        self.beam =  LatticeGaussianBeamConfig(lattice_parameter,
                                               p,
                                               rotation,
                                               width,
                                               center,
                                               power,
                                               I,
                                               lattice_method = lattice_method,
                                               store_config = None,
                                               )
        self.beam1 =  LatticeGaussianBeamConfig(lattice1_parameter,
                                                p1,
                                                rotation1,
                                                width1,
                                                center1,
                                                power1,
                                                I1,
                                                lattice_method = lattice1_method,
                                                store_config = None,
                                                )
        
        self.a = lattice1_parameter[0]
        
        if store_config is not None:
            self.store_parameters(store_config)
            
    def store_parameters(self, store_config):
        """Store both fields configuration in a hdf5 file.

        Args:
            store_config (StoreConfig object): StoreConfig object containing the directories where the files are stored.
        """
        filename = store_config.get_input_dir()
        with h5py.File(filename, "w") as f:
            f.create_dataset("width", data=self.beam.width)
            f.create_dataset("power", data=self.beam.power)
            f.create_dataset("I", data=self.beam.I)
            f.create_dataset("width1", data=self.beam1.width)
            f.create_dataset("power1", data=self.beam1.power)
            f.create_dataset("I1", data=self.beam1.I)
            
            try:
            
                f.create_dataset("lattice_parameter", data=self.beam.lattice_parameter)
                f.create_dataset("p", data=self.beam.p)
                f.create_dataset("rotation", data=self.beam.rotation)
            except:
                print("Lattice parameters on the first beam are not defined.")
                
            try:
                f.create_dataset("lattice1_parameter", data=self.beam1.lattice_parameter)
                f.create_dataset("p1", data=self.beam1.p)
                f.create_dataset("rotation1", data=self.beam1.rotation)
            except:
                print("Lattice parameters on the second beam are not defined.")
        f.close()
    
    # % TODO: Add a method to initialize the objects from a previously stored hdf5 file. This method should receive a StoreConfig and find the required files automatically.