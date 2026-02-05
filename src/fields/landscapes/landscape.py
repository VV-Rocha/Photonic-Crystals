from .phase_step.phase_step import phase_step
from .dark_soliton.base import DarkSolitonConfig1D, dip

class PhaseStep:
    """ Phase step landscape configuration class."""
    def __init__(
        self,
        landscape_config: None=None,
        *args,
        **kwargs,
        ):
        """ Initialize phase step landscape.

        Args:
            landscape_config (None, optional): Configuration dictionary for the phase step. Defaults to None.
        """
        super().__init__(
            *args,
            **kwargs,
            )
            
    def landscape_function(self,):
        """ Generate the phase step landscape function."""
        return phase_step(self.x)
    
class Plane:
    def __init__(
        self,
        landscape_config: None=None,
        *args,
        **kwargs,
        ):
        """ Initialize plane landscape.

        Args:
            landscape_config (None, optional): Configuration dictionary for the plane. Defaults to None.
        """
        super().__init__(*args, **kwargs)
            
    def landscape_function(self,):
        """ Generate the constant plane landscape function."""
        return 1.
    
    def adimensionalize_landscape(self,):
        """ Adimensionalize landscape parameters."""
        pass

class DarkSoliton(DarkSolitonConfig1D):
    """ Dark soliton landscape configuration class."""
    def __init__(
        self,
        landscape_config: None=None,
        *args,
        **kwargs,
    ):
        """ Initialize dark soliton landscape.

        Args:
            landscape_config (None, optional): Configuration dictionary for the dark soliton. Defaults to None.
        """
        super().__init__(
            *args,
            **kwargs,
            )
    
    def landscape_function(self,):
        """ Generate the dark soliton landscape function."""
        return dip(
            self.x,
            self.ratio_env,
            self.width_env,
            self.center_env,
            self.exponent_env,
            self.field_shape,
        )