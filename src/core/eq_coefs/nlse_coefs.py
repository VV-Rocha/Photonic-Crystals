from numpy import pi
from numpy import float64, ndarray

from functools import wraps

import h5py

# % TODO: Add methods to initialize the classes from previously stored configs.

# % TODO: Change the classes to use @dataclass and @classmethod to initialize.

class PhotorefractiveCoefs:
    """Coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    # % TODO: Add a method to store single equation parameters.
    def __init__(self,
                 crystal_parameters,
                 beam_parameters,
                 adim_method,
                 ):
        """Initialize the coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals.

        Args:
            crystal_parameters (PhotorefractiveCrystalConfig Object): Class Object containing the photorefractive crystal parameters.
            beam_parameters (Beam Object): Class Object containing the fundamental properties of the light beam.
            adim_method (Dimensionless Object): Class Object containing the methods for the adimensionalization applied to the equation.
        """
        k = 2*pi/beam_parameters.wavelength
        c = beam_parameters.c
        
        n = crystal_parameters.n
        alpha = crystal_parameters.alpha
        delta_n_max = crystal_parameters.delta_n_max
            
        self.kinetic = adim_method.longitudinal_adim_factor / (2 * k * n * adim_method.transversal_adim_factor**2)
        self.potential = c * k * adim_method.longitudinal_adim_factor * delta_n_max
        self.absorption = alpha * adim_method.longitudinal_adim_factor
        
        self.Isat = crystal_parameters.Isat
        
    def potential_function(self, I:  float | ndarray) -> float | ndarray:
        """Potential Function

        Args:
            I (float | ndarray): Intensity of the optical field.

        Returns:
            float | ndarray: Nonlinear term of the NLSE in photorefractive crystals.
        """
        return self.potential * I/(self.Isat + I)
    
    def print_coefs(self,):
        """Print Coefficients"""
        print(f"Kinetic: {self.kinetic}, Potential: {self.potential}, Absorption: {self.absorption}")


class CoupledPhotorefractiveCoefs(PhotorefractiveCoefs):
    """Coefficients for a pair of coupled Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    def __init__(self,
                 crystal_parameters,
                 beam_parameters,
                 adim_method,
                 store_config=None,
                 ):
        """Initialize the coefficients of the coupled pair of Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals.

        Args:
            crystal_parameters (_type_): _description_
            beam_parameters (_type_): _description_
            adim_method (_type_): _description_
            store_config (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(crystal_parameters = crystal_parameters,
                         beam_parameters = beam_parameters,
                         adim_method = adim_method,
                         )
        
        n1 = crystal_parameters.n1
        alpha1 = crystal_parameters.alpha1
        delta_n_max1 = crystal_parameters.delta_n_max1
                
        k1 = 2*pi/beam_parameters.wavelength1
        c1 = beam_parameters.c1
        
        self.kinetic1 = adim_method.longitudinal_adim_factor / (2 * k1 * n1 * adim_method.transversal_adim_factor**2)
        self.potential1 = c1 * k1 * adim_method.longitudinal_adim_factor * delta_n_max1
        self.absorption1 = alpha1 * adim_method.longitudinal_adim_factor
        
        # self.Isat = crystal_parameters.Isat
        
        if store_config is not None:
            self.store_coefs(store_config)
        
    def potential_function1(self, I: float | ndarray) -> float | ndarray:
        """Potential Function for the second equation

        Args:
            I (float | ndarray): Intensity of the optical field.

        Returns:
            float | ndarray: Nonlinear term of the NLSE in photorefractive crystals.
        """
        return self.potential1 * I/(self.Isat + I)
        
    def print_coefs(self,):
        """Print Coefficients."""
        super().print_coefs()
        print(f"Kinetic1: {self.kinetic1}, Potential1: {self.potential1}, Absorption1: {self.absorption1}")
    
    def store_coefs(self, store_config):
        """Store the coefficients of the coupled set of NLSE.

        Args:
            store_config (StoreConfig Object): Class Object with the directories in the storage folder.
        """
        filename = store_config.get_coefs_dir()
        with h5py.File(filename, "w") as f:
            f.create_dataset("kinetic", data=self.kinetic)
            f.create_dataset("kinetic1", data=self.kinetic1)
            f.create_dataset("potential", data=self.potential)
            f.create_dataset("potential1", data=self.potential1)
            f.create_dataset("absorption", data=self.absorption)
            f.create_dataset("absorption1", data=self.absorption1)
            f.create_dataset("Isat", data=self.Isat)
        f.close()