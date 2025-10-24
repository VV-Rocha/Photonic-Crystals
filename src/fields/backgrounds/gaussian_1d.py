from .base import GaussianConfig1D, gaussian_25_1d
        
class Gaussian1D(GaussianConfig1D):
    """ 1D Gaussian background field"""
    def envelope_function(self,):
        """ Generate the 1D Gaussian envelope field."""
        return gaussian_25_1d(
            self.x,
            self.width,
            self.center,
            self.I,
            self.exponent,
            self.field_shape,
        )