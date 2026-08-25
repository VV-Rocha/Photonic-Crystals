from .uniform_config import UniformConfig
from .func import uniform_field


class UniformEnvelope(UniformConfig):
    def envelope_function(self, mesh):
        return uniform_field(self.I, mesh.field_shape)