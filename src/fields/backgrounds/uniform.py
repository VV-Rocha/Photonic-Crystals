from .base import Uniform1Config

from .functions import uniform_field


class UniformEnvelope1(Uniform1Config,):
    def envelope_function1(self,):
        return uniform_field(self.I1, self.field_shape)
