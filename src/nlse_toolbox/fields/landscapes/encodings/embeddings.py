import numpy as np

from .config import FeaturesConfig
from .macropixels.macropixels import continuous_macropixels
from .macropixels.tile_macropixels import _tile_macropixels


class ContinuousFeatureEmbeddings(FeaturesConfig):
    def landscape_function(self, mesh):
        # get individual macropixels
        macropixels = continuous_macropixels(
            mesh = mesh,
            fs = self.f,
            sizes = self.feature_size,
            encodings = self.encoding,
        )
        
        mask = _tile_macropixels(
            macropixels,
            mesh.field_shape,
        )
        
        return mask