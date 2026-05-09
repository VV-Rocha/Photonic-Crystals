# backgrounds
from .backgrounds.gaussian.gaussian import GaussianProfile2D

# optical computing feature encoding
from .landscapes.encodings.embeddings import ContinuousFeatureEmbeddings

# modulate
from .field.field import Field


class ContinuousFeatureGaussian(
    GaussianProfile2D,
    ContinuousFeatureEmbeddings,
    Field,
):
    """ 2D Gaussian beam with continuous macropixel encodings."""
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