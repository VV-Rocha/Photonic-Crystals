from .....media.photorefractive import PhotorefractiveCrystalParameters, CoupledPhotorefractiveCrystalParameters
from .....beams.beam import Beam, TwoBeams

from .decorators import default_potential, default_potential1

from numpy import ndarray

def potential_function(potential: float, total_intensity: ndarray, Isat: float) -> ndarray:
    """ Potential Function.

    Args:
        potential (float): Scalar value of the potential coefficient.
        total_intensity (ndarray): Intensity field.
        Isat (float): Saturation intensity of the crystal.

    Returns:
        ndarray: Potential field. 
    """
    return potential * total_intensity()/(Isat + total_intensity())
    

class PhotorefractiveCoefs(Beam, PhotorefractiveCrystalParameters):
    """Coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    def __init__(self,
                 invert_energy_scale: bool = False,
                 *args,
                 **kwargs,
                 ):
        """ Initialize the coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals.

        Args:
            invert_energy_scale (bool, optional): Inversion of the kinetic, potential and absorption coefficients. Defaults to False.
        """
        self.invert_energy_scale = invert_energy_scale
        super().__init__(
            *args,
            **kwargs,
        )
        
    def init_coefs(self,):
        """ Initialize kinetic, potential, and absorption coefficients"""
        self.init_kinetic()
        self.init_potential()
        self.init_absorption()
        
    def init_kinetic(self,):
        """ Initialize kinetic coefficient"""
        self.kinetic = -(-1)**self.invert_energy_scale / (2 * self.k * self.n)
    
    def init_potential(self,):
        """ Initialize potential coefficient"""
        self.potential = (-1)**self.invert_energy_scale * self.c * self.k * self.delta_n_max
    
    def init_absorption(self,):
        """ Initialize absorption coefficient"""
        self.absorption = (-1)**self.invert_energy_scale * self.alpha / 2
        
    @default_potential
    def potential_function(self, ) -> ndarray:
        """ Potential Function.

        Returns:
            ndarray: Potential field.
        """
        return potential_function(self.potential, self.get_total_intensity(), self.Isat)
    
    def print_coefs(self,):
        """Print Coefficients"""
        print(f"Kinetic: {self.kinetic}, Potential: {self.potential}, Absorption: {self.absorption}")

class CoupledPhotorefractiveCoefs(TwoBeams, CoupledPhotorefractiveCrystalParameters):
    """Coefficients for a pair of coupled Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    def __init__(self,
                 invert_energy_scale: bool = False,
                 *args,
                 **kwargs,
                 ):
        """Initialize the coefficients of the coupled pair of Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals.

        Args:
            crystal_config (_type_): _description_
            beam_config (_type_): _description_
            adim_method (_type_): _description_
            store_config (_type_, optional): _description_. Defaults to None.
        """
        self.invert_energy_scale = invert_energy_scale
        super().__init__(
            *args,
            **kwargs,
        )
        
    def init_coefs(self,):
        """ Initialize kinetic, potential, and absorption coefficient"""
        self.init_kinetic()
        self.init_potential()
        self.init_absorption()
        
    def init_kinetic(self,):
        """ Initialize kinetic coefficient"""
        self.kinetic = -(-1)**self.invert_energy_scale / (2 * self.k * self.n)
        self.kinetic1 = -(-1)**self.invert_energy_scale / (2 * self.k1 * self.n1)
    
    def init_potential(self,):
        """ Initialize potential coefficient"""
        self.potential = (-1)**self.invert_energy_scale * self.c * self.k * self.delta_n_max
        self.potential1 = (-1)**self.invert_energy_scale * self.c1 * self.k1 * self.delta_n_max1
        
    def init_absorption(self,):
        """ Initialize absorption coefficient"""
        self.absorption = (-1)**self.invert_energy_scale * self.alpha / 2
        self.absorption = (-1)**self.invert_energy_scale * self.alpha1 / 2
        
    @default_potential
    def potential_function(self, ) -> ndarray:
        """ Potential Function.

        Returns:
            ndarray: Potential field.
        """
        return potential_function(self.potential, self.get_total_intensity(), self.Isat)
        
    @default_potential1
    def potential_function(self, ) -> ndarray:
        """ Potential Function.

        Returns:
            ndarray: Potential field.
        """
        return potential_function(self.potential1, self.get_total_intensity(), self.Isat)
    
    def print_coefs(self,):
        """Print Coefficients"""
        print(f"Kinetic: {self.kinetic}, Potential: {self.potential}, Absorption: {self.absorption}")
