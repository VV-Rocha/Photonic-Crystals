from numpy import sqrt

from .potential import SaturatedPotential
from .nlse_coefs import NLSECoefs


class PhotorefractiveModel(SaturatedPotential):
    """Coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    @property
    def adimensional_flag(self,):
        return False
    
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
    
    def init(self,):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self._adimensionalization_factors()
        self.init_coefs()
    
    def init_coefs(self, media):
        """ Initialize kinetic, potential, and absorption coefficients"""
        self.beam_coefs = {}
        for beam_key, beam_value in media.medium_beams.item():
            self.beam_coefs[beam_key] = NLSECoefs(
                kinetic = self._init_kinetic(beam_value),
                potential = self._init_potential(beam_value),
                absorption = self._init_absorption(beam_value)
            )
    
    def _init_kinetic(self, medium):
        """ Initialize kinetic coefficient"""
        self.kinetic = -(-1)**self.invert_energy_scale / (2 * medium.k * medium.n)
    
    def _init_potential(self, medium):
        """ Initialize potential coefficient"""
        self.potential = (-1)**self.invert_energy_scale * medium.c * medium.k * medium.delta_n_max
    
    def _init_absorption(self, medium):
        """ Initialize absorption coefficient"""
        self.absorption = (-1)**self.invert_energy_scale * medium.alpha / 2
        
    def _adimensionalization_factors(self,):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""
        self.transversal_adim_factor = 1.
        self.longitudinal_adim_factor = 1.


class WavevectorPhotorefractiveModel:
    """ Wavevector Photorefractive Model."""
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
    
    @property
    def adimensional_flag(self,):
        return True
    
    def init(self, box, ref_beam="beam_1"):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self._adimensionalization_factors(box.media, ref_beam)
        self.init_coefs(box.media)
        
    def _adimensionalization_factors(self, media, ref_beam):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""
        self.ref_beam = ref_beam
        self.transversal_adim_factor = 1. / (media.medium_beams[ref_beam].k * sqrt(media.medium_beams[ref_beam].n * media.medium_beams[ref_beam].delta_n_max))
        self.longitudinal_adim_factor = 1. / (media.medium_beams[ref_beam].k * media.medium_beams[ref_beam].delta_n_max)
    
    def init_coefs(self, media):
        """ Initialize the coefficients for the model based on adimensionalization factors."""
        self.beam_coefs = {}
        for beam_key, beam_value in media.medium_beams.items():
            if beam_key == self.ref_beam:
                self.beam_coefs[beam_key] = NLSECoefs(
                    kinetic = - .5 * (-1)**self.invert_energy_scale,
                    potential = (-1)**self.invert_energy_scale * beam_value.c,
                    absorption = self.longitudinal_adim_factor * (-1)**self.invert_energy_scale * beam_value.alpha / 2
                )
            else:
                self.beam_coefs[beam_key] = NLSECoefs(
                    kinetic = - .5 * (-1)**self.invert_energy_scale * (media.medium_beams[self.ref_beam].k/beam_value.k),
                    potential = (-1)**self.invert_energy_scale * beam_value.c * (beam_value.k/media.medium_beams[self.ref_beam].k),
                    absorption = self.longitudinal_adim_factor * (-1)**self.invert_energy_scale * beam_value.alpha / 2
                )