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
        computing_config,
        dynamics = True,
        *args,
        **kwargs,
    ):
        self.dynamics = dynamics
        
        self._get_parameters(computing_config)
        
        super().__init__(
            landscape_config=landscape_config,
            envelope_config=envelope_config,
            *args,
            **kwargs,
        )
    
    def _get_parameters(self, computing_config):
        if ("random_phase" in computing_config.keys()):
            self.random_phase = computing_config["random_phase"]
            if self.random_phase:
                self.speckle_size = computing_config["speckle_size"]
        else:
            self.random_phase = False
        
        if ("fixed_phase_mask" in computing_config.keys()):
            self.fixed_phase_mask = computing_config["fixed_phase_mask"]
        else:
            self.fixed_phase_mask = False
    
    def encode_feature(
        self,
        f,
        box,
    ):
        self._set_feature(f)
        box.init_beams(
            box.solver.encoding_noise,
        )