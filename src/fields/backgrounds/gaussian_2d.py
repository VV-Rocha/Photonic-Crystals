from .base import GaussianConfig2D, CoupledGaussianConfig2D, gaussian_25_2d


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

class CoupledGaussian2D(GaussianProfile2D, CoupledGaussianConfig2D):
    """ Coupled 2D Gaussian envelope field."""
    def envelope_function1(self,):
        """ Compute the second Gaussian envelope function."""
        return gaussian_25_2d(
            self.xx,
            self.yy,
            self.width1,
            self.center1,
            self.I1,
            self.exponent1,
            self.field_shape,
        )