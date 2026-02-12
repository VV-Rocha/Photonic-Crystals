import arrayfire as af

from .....arrayfire_utils.facade import Arrayfire

from .....storage.store_methods import StorageField

from .mesh import SplitStepMesh

from ..iterators.solver import AfTimeSpaceAnalogIterator

from .base import SplitStepMethods

class SplitStepSolver(
    StorageField,
    Arrayfire,
    SplitStepMesh,
    SplitStepMethods,
    AfTimeSpaceAnalogIterator,
):
    @property
    def arrayfire_flag(self,):
        return True
    
    def init_solver(self,):
        self.set_device()
        
        self.init_mesh()
        
    def af_get_intensity(self,):
        return (self.field)*af.conjg(self.field)
    
    def af_potential_function(self,):
        return self.potential * (self.af_get_intensity() / (self.Isat + self.af_get_intensity()))
    
    def step_solver(self,):
        """Inplace single step evolution of the 2D NLSE using the split-step Fourier method.
        """
        # half linear step
        self.linear_step(self.field, self.kinetic, self.dz)
        
        # nonlinear step
        self.nonlinear_step(
            self.field,
            self.af_potential_function(),
        )
        
        # absorption step
        self.absorption_step(self.field, self.exp)
        
        # half linear step
        self.linear_step(self.field, self.kinetic, self.dz)