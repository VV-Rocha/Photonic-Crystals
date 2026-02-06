from .nlse_coefs import PhotorefractiveCoefs, CoupledPhotorefractiveCoefs

from numpy import sqrt

class ModelVerbose:
    def print_adimensionalization_factors(self,):
        """ Print the adimensionalization factors for reference."""
        print(r"$\chi_{\perp} =$", self.transversal_adim_factor)
        print(r"$\chi_{\parallel} = $", self.longitudinal_adim_factor)

class WavevectorPhotorefractiveModel(PhotorefractiveCoefs, ModelVerbose):
    """ Wavevector Photorefractive Model."""
    @property
    def adimensional_flag(self,):
        return True
    
    def init_model(self,):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self.adimensionalization_factors()
        self.init_coefs()
        
    def adimensionalization_factors(self,):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""
        self.transversal_adim_factor = 1. / (self.k * sqrt(self.n * self.delta_n_max))
        self.longitudinal_adim_factor = 1. / (self.k * self.delta_n_max)
    
    def init_coefs(self,):
        """ Initialize the coefficients for the model based on adimensionalization factors."""
        self.kinetic = - .5 * (-1)**self.invert_energy_scale
        self.potential = (-1)**self.invert_energy_scale * self.c
        self.absorption = self.longitudinal_adim_factor * (-1)**self.invert_energy_scale * self.alpha / 2
        
class PhotorefractiveModel(PhotorefractiveCoefs):
    @property
    def adimensional_flag(self,):
        return True
                
    def init_model(self,):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self.adimensionalization_factors()
        self.init_coefs()
        
    def adimensionalization_factors(self,):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""
        self.transversal_adim_factor = 1.
        self.longitudinal_adim_factor = 1.
        
class CoupledPhotorefractiveModel(CoupledPhotorefractiveCoefs):
    @property
    def adimensional_flag(self,):
        return False
    
    def init_model(self,):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self.adimensionalization_factors()
        self.init_coefs()
        
    def adimensionalization_factors(self,):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""

        self.transversal_adim_factor = 1.
        self.longitudinal_adim_factor = 1.
        
class CoupledWavevectorPhotorefractiveModel(CoupledPhotorefractiveCoefs):
    @property
    def adimensional_flag(self,):
        return True
        
    def init_model(self,):
        """ Initialize the model by computing adimensionalization factors and coefficients."""
        self.adimensionalization_factors()
        self.init_coefs()
        
    def adimensionalization_factors(self,):
        """ Compute adimensionalization factors for transversal and longitudinal directions."""
        self.transversal_adim_factor = 1. / (self.k * sqrt(self.n * self.delta_n_max))
        self.longitudinal_adim_factor = 1. / (self.k * self.delta_n_max)
    
    def init_coefs(self,):
        """ Initialize the coefficients for the model based on adimensionalization factors."""
        self.kinetic = - .5 * (-1)**self.invert_energy_scale
        self.potential = (-1)**self.invert_energy_scale * self.c
        self.absorption = self.longitudinal_adim_factor * self.alpha / 2
        
        self.kinetic1 = - .5 * (-1)**self.invert_energy_scale * (self.k/self.k1)
        self.potential1 = (-1)**self.invert_energy_scale * self.c1 * (self.k1/self.k)
        self.absorption1 = (-1)**self.invert_energy_scale * self.longitudinal_adim_factor * self.alpha1 / 2