import numpy as np

class FeatureMacropixel:
    def feature_macropixel(self, size, dtype=np.complex128):
        width_px = len(np.where((self.x>-size//2) * (self.x<size//2))[0])
        height_px = len(np.where((self.y>-size//2) * (self.y<size//2))[0])
        
        feature = np.zeros((width_px, height_px), dtype=dtype)
        return feature, width_px, height_px
        
class PhaseEncoding(FeatureMacropixel):
    def phase_encoded_feature(self, f, size):
        feature, width_px, height_px = self.feature_macropixel(size, dtype=np.complex128)
        feature = np.exp(1.j * np.pi * f)
        return feature, width_px, height_px
    
class AmplitudeEncoding(FeatureMacropixel):
    def amplitude_encoded_feature(self, f, size):
        feature, width_px, height_px = self.feature_macropixel(size, dtype=np.complex128)
        feature += f
        return feature, width_px, height_px