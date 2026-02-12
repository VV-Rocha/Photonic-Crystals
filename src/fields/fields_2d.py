from .backgrounds.gaussian_2d import GaussianProfile2D, CoupledGaussian2D

from .base import Modulation, CoupledModulation, CoupledFields

from .noise.noise import WhitenoiseCoupledFields, WhitenoiseField

from .landscapes.base import Uniform
from .landscapes.landscapes_2d import MoireLattice
from .landscapes.landscape import DarkSoliton, PhaseStep

from .base import Field

from .utils import UnpackModulationConfig, CoupledUnpackModulationConfig

class SecondMoireLatticeGaussian2D(CoupledGaussian2D, MoireLattice, CoupledModulation, CoupledFields, WhitenoiseCoupledFields, CoupledUnpackModulationConfig):
    """ Second Moire Lattice Gaussian 2D Coupled Field Class."""
    pass

class Gaussian2D(UnpackModulationConfig, GaussianProfile2D, Uniform, Modulation, Field, WhitenoiseField):
    pass

class DarkSolitonGaussian2D(GaussianProfile2D, DarkSoliton, Modulation, Field, WhitenoiseField, UnpackModulationConfig):
    pass

class PhaseStepGaussian2D(UnpackModulationConfig, GaussianProfile2D, PhaseStep, Modulation, Field, WhitenoiseField):
    pass