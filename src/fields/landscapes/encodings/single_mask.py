import numpy as np

from .base import PhaseEncoding
from .base import AmplitudeEncoding


class SingleFeatureConfig:
    def __init__(
        self,
        landscape1_config: dict,
        *args,
        **kwargs,
    ):
        self.f = landscape1_config["feature"]
        self.feature_size = landscape1_config["size"]
        
        super().__init__(*args, **kwargs)
        
class PhaseSingleFeature(SingleFeatureConfig, PhaseEncoding):
    def landscape_function1(self,):
        return self.single_feature()
    
    def single_feature(self,):
        mx, my = self.field_shape[0]//2, self.field_shape[1]//2

        landscape = np.ones(self.field_shape, dtype=np.complex128)
        feature, width_px, height_px = self.phase_encoded_feature(self.f, self.feature_size)
        
        landscape[mx-width_px//2:mx+width_px//2 +1, my-height_px//2:my+height_px//2 +1] = feature
        
        return landscape
    
    def adimensionalize_landscape1(self,):
        self.feature_size = self.adimensionalize_length(self.feature_size)
        
class AmplitudeSingleFeature(SingleFeatureConfig, AmplitudeEncoding):
    def landscape_function1(self,):
        return self.single_feature()
    
    def single_feature(self,):
        mx, my = self.field_shape[0]//2, self.field_shape[1]//2

        landscape = np.ones(self.field_shape, dtype=np.complex128)
        feature, width_px, height_px = self.amplitude_encoded_feature(self.f, self.feature_size)
        
        landscape[mx-width_px//2:mx+width_px//2 +1, my-height_px//2:my+height_px//2 +1] = feature
        
        return landscape
    
    def adimensionalize_landscape1(self,):
        self.feature_size = self.adimensionalize_length(self.feature_size)