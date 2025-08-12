from .nlse_coefs import PhotorefractiveCoefs

from numpy import sqrt

class WavevectorPhotorefractiveModel(PhotorefractiveCoefs):
    def __init__(
        self,
        crystal_config,
        beam_config,
        invert_energy_scale: bool = False,
    ):
        super().__init__(
            crystal_config = crystal_config,
            beam_config = beam_config,
            invert_energy_scale = invert_energy_scale,
        )
        
        self.adimensional_flag = True  # indicates if adimensionalization occurs
        
        self.adimensionalization_factors()
        
        self.adimensional_coefs()
        
    def adimensionalization_factors(self,):
        self.transversal_adim_factor = 1. / (self.k * sqrt(self.n * self.delta_n_max))
        self.longitudinal_adim_factor = 1. / (self.k * self.delta_n_max)
    
    def reset_coefs(func):
        def wrapper(self,):
            super().kinetic()
            super().potential()
            super().absorption()
            func(self,)
        return wrapper
    
    @reset_coefs
    def adimensional_coefs(self,):
        self.kinetic = - .5 * (-1)**self.invert_energy_scale
        self.potential = (-1)**self.invert_energy_scale
        self.absorption *= self.longitudinal_adim_factor
        
class PhotorefractiveModel(PhotorefractiveCoefs):
    def __init__(
        self,
        crystal_config,
        beam_config,
        invert_energy_scale: bool = False,
    ):
        super().__init__(
            crystal_config = crystal_config,
            beam_config = beam_config,
            invert_energy_scale = invert_energy_scale,
        )
        
        self.adimensional_flag = False
        
        self.adimensionalization_factors()
        
    def adimensionalization_factors(self,):
        self.transversal_adim_factor = 1.
        self.longitudinal_adim_factor = 1.