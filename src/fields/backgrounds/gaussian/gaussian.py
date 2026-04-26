from .gaussian_config import GaussianConfig1D, GaussianConfig2D
from .func import gaussian_25_1d, gaussian_25_2d


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

class GaussianProfile2D(GaussianConfig2D):
    def envelope_function(self,):
        """ Compute the first Gaussian envelope function."""
        return gaussian_25_2d(
            self.xx,
            self.yy,
            self.width,
            self.center,
            self.I,
            self.exponent,
            self.field_shape,
        )