from functools import wraps
from typing import Tuple

class LatticeConfig:
    """Class to store the lattice configuration variables."""
    def __init__(
        self,
        structure_config,
        ):
        """Initializes the lattice configuration variables.

        Args:
            lattice_parameter (float | Tuple[float, ...]): Lattice parameters with dimensions
            p (float | Tuple[float, ...], optional): Constant multiplicative factor. Defaults to (1., 1.).
            rotation (float | Tuple[float, ...], optional): Rotation of the lattice(s). Defaults to (0., 0.).
        """
        self.lattice_parameter = structure_config["a"]
        self.p = structure_config["p"]
        self.rotation = structure_config["angle"]
        
        if self.lattice_parameter is not None:
            if type(self.lattice_parameter) == float:
                self.a = self.lattice_parameter
            else:
                self.a = self.lattice_parameter[0]


class Lattice(LatticeConfig):
    """Class to define the lattice and lattice method."""
    def __init__(self,
                 structure_config,
                 *args,
                 **kwargs,
                 ):
        """Initializes the lattice configuration.

        Args:
            lattice_parameter (float | Tuple[float, ...]): Lattice parameters with dimensions
            p (float | Tuple[float, ...], optional): Constant multiplicative factor. Defaults to (1., 1.).
            rotation (float | Tuple[float, ...], optional): Rotation of the lattice(s). Defaults to (0., 0.).
            store_config (StoreConfig, optional): StorageConfig objects containing the directories where the files are stored. Defaults to None.
            lattice_method (func, optional): Function returning the lattice landscape. If no function is given the field defaults to a constant landscape. Defaults to None.
        """
        super().__init__(structure_config=structure_config, *args, **kwargs)
        
        if structure_config["lattice_method"] is None:
            self.landscape = lambda mesh: 1.
        else:
            self.landscape = lambda mesh: structure_config["lattice_method"](
                mesh,
                self.lattice_parameter,
                self.p,
                self.rotation,
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
                 ):
        super().__init__(lattice_parameter = lattice_parameter,
                         p = p,
                         rotation = rotation,
                         I = I,
                         lattice_method = lattice_method,
                         )
        
        self.beam = LatticeGaussianBeamConfig(lattice_parameter,
                                               p,
                                               rotation,
                                               I,
                                               lattice_method = lattice_method,
                                               )
            
def cache_import_function(init_func):
    @wraps(init_func)
    def wrapper(*args, **kwargs):
        from ..backgrounds.gaussian_profiles import gaussian_25
        GaussianBeamConfig._gaussian = gaussian_25
        return init_func(*args, **kwargs)
    return wrapper

class GaussianBeamConfig:
    """Class to define the Gaussian beam shape."""
    @cache_import_function
    def __init__(self,
                 modulation_config,
                 *args,
                 **kwargs,
                 ):
        """Initializes the Gaussian beam configuration.
        The Gaussian beam is defined by its width, intensity and power.

        Args:
            width (float | Tuple[float, float]): FWHM of the Gaussian beam. If a tuple is given, the first element is the width in x direction and the second element is the width in y direction. Given a float the width is the same in both directions.
            I (float): Intensity of the Gaussian beam. The amplitude of the Gaussian beam is given by the square root of the intensity.
            power (int, optional): (super)Gaussian power. Defaults to 1.
        """
        self.width = modulation_config["waist"]
        self.center = modulation_config["center"]
        self.power = modulation_config["exponent"]
        self.I = modulation_config["I"]
        
        super().__init__(*args, **kwargs,)
        
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


class LatticeGaussianBeamConfig(GaussianBeamConfig, Lattice):
    """Class to define the Gaussian beam profile with a lattice landscape."""
    def __init__(
        self,
        landscape_config,
        modulation_config,
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
        """
        super().__init__(
            structure_config=landscape_config,
            modulation_config=modulation_config,
            )


class LatticeGaussianCoupledConfig(LatticeGaussianBeamConfig):
    """Class to define the Gaussian beam profile with a modulated lattice landscape."""
    def __init__(
        self,
        modulation_config,
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
        """
        super().__init__(
            landscape_config=modulation_config["structure"],
            modulation_config=modulation_config["modulation"],
            )
        
        self.beam1 =  LatticeGaussianBeamConfig(
            landscape_config = modulation_config["structure1"],
            modulation_config = modulation_config["modulation1"],
        )