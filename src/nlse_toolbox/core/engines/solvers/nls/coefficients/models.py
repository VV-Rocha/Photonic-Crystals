from numpy import sqrt

from .potential import SaturatedPotential
from .nlse_coefs import NLSECoefs

from numpy import pi, isfinite
        

class PhotorefractiveModel(SaturatedPotential):
    """Coefficients of the Nonlinear Schrodinger Equation emerging in the paraxial propagation of light in photorefractive crystals."""
    @property
    def adimensional_flag(self,):
        return True  #False
    
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
    
    def init(self, box):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self._adimensionalization_factors()
        self.init_coefs(box.media)
    
    def init_coefs(self, media):
        """ Initialize kinetic, potential, and absorption coefficients"""
        self.beam_coefs = {}
        for beam_key, beam_value in media.medium_beams.items():
            self.beam_coefs[beam_key] = NLSECoefs(
                kinetic = self._init_kinetic(beam_value),
                potential = self._init_potential(beam_value),
                absorption = self._init_absorption(beam_value)
            )
    
    def _init_kinetic(self, medium):
        """ Initialize kinetic coefficient"""
        return -(-1)**self.invert_energy_scale / (2 * medium.k * medium.n)
    
    def _init_potential(self, medium):
        """ Initialize potential coefficient"""
        return (-1)**self.invert_energy_scale * medium.c * medium.k * medium.delta_n_max
    
    def _init_absorption(self, medium):
        """ Initialize absorption coefficient"""
        return (-1)**self.invert_energy_scale * medium.alpha / 2
        
    def _adimensionalization_factors(self,):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""
        self.transversal_adim_factor = 1.
        self.longitudinal_adim_factor = 1.


class LatticePhotorefractiveModel(PhotorefractiveModel):
    """Photorefractive model normalized using a sublattice field period.

    Coordinates:
        X = x / transversal_adim_factor
        Y = y / transversal_adim_factor
        Z = z / longitudinal_adim_factor

    The physical field period a maps to dimensionless period pi.
    """

    def __init__(
        self,
        lattice_parameter: float,
        invert_energy_scale: bool = False,
        *args,
        **kwargs,
    ):
        self.lattice_parameter = float(lattice_parameter)
        if not isfinite(self.lattice_parameter) or self.lattice_parameter <= 0:
            raise ValueError("lattice_parameter must be finite and positive.")

        super().__init__(
            invert_energy_scale=invert_energy_scale,
            *args,
            **kwargs,
        )

    @property
    def adimensional_flag(self):
        return True

    def init(self, box, ref_beam="beam_1"):
        self._adimensionalization_factors(box.media, ref_beam)
        self.init_coefs(box.media)

    def _adimensionalization_factors(self, media, ref_beam):
        self.ref_beam = ref_beam
        medium = media.medium_beams[ref_beam]

        self.transversal_adim_factor = self.lattice_parameter / pi
        self.longitudinal_adim_factor = (
            medium.k * medium.n * self.transversal_adim_factor**2
        )

    def _init_kinetic(self, medium):
        return (
            super()._init_kinetic(medium)
            * self.longitudinal_adim_factor
            / self.transversal_adim_factor**2
        )

    def _init_potential(self, medium):
        return (
            super()._init_potential(medium)
            * self.longitudinal_adim_factor
        )

    def _init_absorption(self, medium):
        return (
            super()._init_absorption(medium)
            * self.longitudinal_adim_factor
        )


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