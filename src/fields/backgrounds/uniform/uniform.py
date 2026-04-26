from .uniform_config import UniformConfig
from .func import uniform_field


class UniformEnvelope(UniformConfig,):
    def envelope_function1(self,):
        return uniform_field(self.I, self.field_shape)
