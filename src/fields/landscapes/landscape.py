from .phase_step.phase_step import phase_step
from .dark_soliton.base import DarkSolitonConfig, dip


def merge_1d_2d(ret1d, ret2d, field_shape):
    if len(field_shape)==1:
        return_param = ret1d
    elif len(field_shape)==2:
        return_param = ret2d
    else:
        raise ValueError('Pipeline is unable to distinguish between 1D and 2D configurations.')
    return return_param

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
        return phase_step(
            merge_1d_2d(
                self.x,
                self.xx if (hasattr(self, "xx")) else None,
                self.field_shape,
            )
        )
        
    def adimensionalize_landscape(self,):
        """ Adimensionalize landscape parameters."""
        pass
    
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

class DarkSoliton(DarkSolitonConfig):
    def landscape_function(self,):
        """ Generate the dark soliton landscape function."""
        return dip(
            merge_1d_2d(
                self.x,
                self.xx if hasattr(self, "xx") else None, self.field_shape,
            ),
            self.ratio_env,
            self.width_env,
            self.center_env,
            self.exponent_env,
            self.field_shape,
        )