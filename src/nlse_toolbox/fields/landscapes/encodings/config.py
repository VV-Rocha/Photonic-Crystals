import numpy as np

from .utils import _macropixel_size
from .utils import _encoding


class FeaturesConfig:
    def __init__(
        self,
        landscape_config,
        *args,
        **kwargs,
    ):
        self.nfeatures = len(landscape_config["f"])
        self._set_feature(landscape_config["f"])

        self.encoding_size = landscape_config["size"]
        
        self.feature_size = _macropixel_size(self.encoding_size, self.nfeatures)
        
        self.encoding = _encoding(landscape_config["encoding"], self.nfeatures)
        
        super().__init__(*args, **kwargs)
        
    def _set_feature(
        self,
        f,
    ):
        self.f = {f"f{i}": f[i] for i in range(self.nfeatures)}