from ....core.media.photorefractive import PhotorefractiveCrystalParameters
from ....core.beams import Beam

from numpy import pi, abs
from numpy import float64, ndarray

from functools import wraps

class PhotorefractiveCoefs(Beam, PhotorefractiveCrystalParameters):
    """Coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    # % TODO: Add a method to store single equation parameters.
    def __init__(self,
                 crystal_config,
                 beam_config,
                 invert_energy_scale: bool = False
                 ):
        """Initialize the coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals.

        Args:
            crystal_config (PhotorefractiveCrystalConfig Object): Class Object containing the photorefractive crystal parameters.
            beam_config (Beam Object): Class Object containing the fundamental properties of the light beam.
            adim_method (Dimensionless Object): Class Object containing the methods for the adimensionalization applied to the equation.
        """   
        super().__init__(
            crystal_config = crystal_config,
            beam_config = beam_config,
        )
                 
        self.invert_energy_scale = invert_energy_scale
        
        self.kinetic()
        self.potential()
        self.absorption()
        
    def kinetic(self,):
        self.kinetic = -(-1)**self.invert_energy_scale / (2 * self.k * self.n)
    
    def potential(self,):
        self.potential = (-1)**self.invert_energy_scale * self.c * self.k * self.delta_n_max
    
    def absorption(self,):
        self.absorption = (-1)**self.invert_energy_scale * self.alpha / 2
        
    def potential_function(self, field):
        """Potential Function

        Args:
            field (Field object): Fields object containing the fields and a get_total_intensity() method.

        Returns:
            float | ndarray: Nonlinear term of the NLSE in photorefractive crystals.
        """
        return self.potential * field.get_total_intensity()/(self.Isat + field.get_total_intensity())
    
    def print_coefs(self,):
        """Print Coefficients"""
        print(f"Kinetic: {self.kinetic}, Potential: {self.potential}, Absorption: {self.absorption}")


class CoupledPhotorefractiveCoefs(PhotorefractiveCoefs):
    """Coefficients for a pair of coupled Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    def __init__(self,
                 crystal_config,
                 beam_config,
                 invert_energy_scale: bool = False,
                 ):
        """Initialize the coefficients of the coupled pair of Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals.

        Args:
            crystal_config (_type_): _description_
            beam_config (_type_): _description_
            adim_method (_type_): _description_
            store_config (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(crystal_config = crystal_config,
                         beam_config = beam_config,
                         adim_method = adim_method,
                         invert_energy_scale = invert_energy_scale,
                         )
        
        n1 = crystal_config.n1
        alpha1 = crystal_config.alpha1
        delta_n_max1 = crystal_config.delta_n_max1
                
        k1 = 2*pi/beam_config.wavelength1
        c1 = beam_config.c1
        
        self.kinetic1 = - (-1)**invert_energy_scale * adim_method.longitudinal_adim_factor / (2 * k1 * n1 * adim_method.transversal_adim_factor**2)
        self.potential1 = (-1)**invert_energy_scale * c1 * k1 * adim_method.longitudinal_adim_factor * delta_n_max1
        self.absorption1 = (-1)**invert_energy_scale * alpha1 * adim_method.longitudinal_adim_factor / 2

    def potential_function1(self, field) -> float | ndarray:
        """Potential Function for the second equation

        Args:
            field (Field2D object): Field object containing the electric fields.

        Returns:
            float | ndarray: Nonlinear term of the NLSE in photorefractive crystals.
        """
        return self.potential1 * field.get_total_intensity()/(self.Isat + field.get_total_intensity())
        
    def print_coefs(self,):
        """Print Coefficients."""
        super().print_coefs()
        print(f"Kinetic1: {self.kinetic1}, Potential1: {self.potential1}, Absorption1: {self.absorption1}")