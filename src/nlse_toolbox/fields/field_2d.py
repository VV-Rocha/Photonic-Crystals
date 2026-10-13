# __init__
from .utils import _BeamInitMixin

# backgrounds
from .backgrounds.gaussian.gaussian import GaussianProfile2D
from .backgrounds.uniform.uniform import UniformEnvelope

# landscapes
from .landscapes.uniform.uniform import UniformLandscape
from .landscapes.phase_step.phase_step import PhaseStepLandscape
from .landscapes.lattices.moire_lattices import MoireLatticeLandscape
from .landscapes.lattices.single_lattices.one_dimensional import ShiqiXiaSSH, SiteBySiteSSH
from .landscapes.bogoliubov.excitations import BogoliubovExcitations

# modulate
from .field.field import Field


class Gaussian(
    _BeamInitMixin,
    GaussianProfile2D,
    UniformLandscape,
    Field,
):
    """ 2D Gaussian beam."""
    pass


class MoireLatticeGaussian(
    _BeamInitMixin,
    GaussianProfile2D,
    MoireLatticeLandscape,
    Field,
):
    """ 2D Gaussian beam with a moire lattice landscape."""
    pass


class MoireLatticeUniform(
    _BeamInitMixin,
    UniformEnvelope,
    MoireLatticeLandscape,
    Field,
):
    """ Uniform beam with a moire lattice landscape."""
    pass


class ShiqiXiaUniformSSH(
    _BeamInitMixin,
    UniformEnvelope,
    ShiqiXiaSSH,
    Field,
):
    _BeamInitMixin,


class SiteBySiteUniformSSH(
    _BeamInitMixin,
    UniformEnvelope,
    SiteBySiteSSH,
    Field,
):
    pass


class PhaseStepGaussian(
    _BeamInitMixin,
    GaussianProfile2D,
    PhaseStepLandscape,
    Field,
):
    pass


class BogoliubovGaussian(
    _BeamInitMixin,
    GaussianProfile2D,
    BogoliubovExcitations,
    Field,
):
    pass