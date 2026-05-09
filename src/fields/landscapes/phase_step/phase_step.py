import numpy as np

from .function import phase_step


class PhaseStepLandscape:
    """ Phase step landscape configuration class."""
    def __init__(
        self,
        landscape_config = None,
        *args,
        **kwargs,
        ):
        """ Initialize phase step landscape.

        Args:
            landscape_config (None, optional): Configuration dictionary for the phase step. Defaults to None.
        """
        if landscape_config is not None:
            self.a = landscape_config["a"]
            self.b = landscape_config["b"]
        else:
            self.a = 0.
            self.b = np.pi
        
        super().__init__(
            *args,
            **kwargs,
            )
            
    def landscape_function(self, mesh):
        """ Generate the phase step landscape function."""
        return phase_step(
            mesh.xx,
            a = self.a,
            b = self.b,
        )