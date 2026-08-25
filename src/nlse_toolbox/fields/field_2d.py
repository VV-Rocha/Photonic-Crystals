# backgrounds
from .backgrounds.gaussian.gaussian import GaussianProfile2D
from .backgrounds.uniform.uniform import UniformEnvelope

# landscapes
from .landscapes.uniform.uniform import UniformLandscape
from .landscapes.phase_step.phase_step import PhaseStepLandscape
from .landscapes.lattices.moire_lattices import MoireLatticeLandscape
from .landscapes.lattices.single_lattices.one_dimensional import ShiqiXiaSSH, SiteBySiteSSH

# modulate
from .field.field import Field


class Gaussian(
    GaussianProfile2D,
    UniformLandscape,
    Field,
):
    """ 2D Gaussian beam."""
    def __init__(
        self,
        landscape_config,
        envelope_config,
        dynamics = True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics
        
        super().__init__(
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            *args,
            **kwargs,
        )


class MoireLatticeGaussian(
    GaussianProfile2D,
    MoireLatticeLandscape,
    Field,
):
    """ 2D Gaussian beam with a moire lattice landscape."""
    def __init__(
        self,
        landscape_config,
        envelope_config,
        dynamics = True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics
        super().__init__(
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            *args,
            **kwargs,
        )

  
class ShiqiXiaUniformSSH(
    UniformEnvelope,
    ShiqiXiaSSH,
    Field,
):
    def __init__(
        self,
        landscape_config,
        envelope_config,
        dynamics = True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics
        super().__init__(
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            *args,
            **kwargs,
        )


class SiteBySiteUniformSSH(
    UniformEnvelope,
    SiteBySiteSSH,
    Field,
):
    def __init__(
        self,
        landscape_config,
        envelope_config,
        dynamics = True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics
        super().__init__(
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            *args,
            **kwargs,
        )


class PhaseStepGaussian(
    GaussianProfile2D,
    PhaseStepLandscape,
    Field,
):
    def __init__(
        self,
        landscape_config,
        envelope_config,
        dynamics = True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics
        super().__init__(
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            *args,
            **kwargs,
        )