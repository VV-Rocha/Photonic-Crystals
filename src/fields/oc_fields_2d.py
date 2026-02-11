from .backgrounds.gaussian_2d import GaussianProfile2D, CoupledGaussian2D

from .base import Modulation, CoupledModulation, CoupledFields

from .noise.noise import WhitenoiseCoupledFields, WhitenoiseField

from .landscapes.landscapes_2d import Uniform
from .landscapes.encodings.single_mask import PhaseSingleFeature
from .landscapes.encodings.single_mask import AmplitudeSingleFeature

from .utils import CoupledUnpackModulationConfig

# class CoupledPhaseEncodingTwoFeatureGaussian2D(CoupledGaussian2D, Uniform, PhaseTwoFeature, CoupledModulation, CoupledFields, WhitenoiseCoupledFields, CoupledUnpackModulationConfig):
#     """ Phase Encoding Two Features Gaussian 2D Coupled Field Class."""
#     pass

class CoupledPhaseEncodingSingleFeatureGaussian2D(CoupledUnpackModulationConfig, CoupledGaussian2D, Uniform, PhaseSingleFeature, CoupledModulation, CoupledFields, WhitenoiseCoupledFields):
    """ Phase Encoding Single Feature Gaussian 2D Coupled Field Class."""
    pass

class CoupledAmplitudeEncodingSingleFeatureGaussian2D(CoupledUnpackModulationConfig, CoupledGaussian2D, Uniform, AmplitudeSingleFeature, CoupledModulation, CoupledFields, WhitenoiseCoupledFields):
    """ Amplitude Encoding Single Feature Gaussian 2D Coupled Field Class."""
    pass