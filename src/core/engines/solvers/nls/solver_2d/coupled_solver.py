import arrayfire as af

from .....arrayfire_utils.facade import Arrayfire

from .....storage.store_methods import CoupledStorageField

from .mesh import CoupledSplitStepMesh

from ..iterators.solver import AfTimeSpaceAnalogIterator

from .base import SplitStepMethods

class CoupledSplitStepSolver(CoupledStorageField, Arrayfire, CoupledSplitStepMesh, SplitStepMethods, AfTimeSpaceAnalogIterator):
    @property
    def arrayfire_flag(self,):
        return True
        
    def init_solver(self,):
        self.set_device()
        
        self.init_mesh()
        
    def af_get_intensity(self,):
        return (self.field)*af.conjg(self.field) + (self.field1)*af.conjg(self.field1)
    
    def af_potential_function(self,):
        return self.potential * (self.af_get_intensity() / (self.Isat + self.af_get_intensity()))

    def af_potential_function1(self,):
        return self.potential1 * (self.af_get_intensity() / (self.Isat + self.af_get_intensity()))
        
    def step_solver(self,):
        """Inplace single step evolution of the coupled 2D NLSE using the split-step Fourier method.
        """
        # half linear step
        self.linear_step(self.field, self.kinetic, self.dz)
        self.linear_step(self.field1, self.kinetic1, self.dz)
        
        # nonlinear step
        auxiliary_intensity = self.af_potential_function1()
        self.nonlinear_step(self.field,  # apply nonlinearity in first field.
                    self.af_potential_function(),
                    )
        # apply nonlinearity in second field with intensity field stored from initial step conditions
        self.nonlinear_step(self.field1,
                    auxiliary_intensity,
                    )
        
        # absorption step
        self.absorption_step(self.field, self.exp)
        self.absorption_step(self.field1, self.exp1)
        
        # half linear step
        self.linear_step(self.field, self.kinetic, self.dz)
        self.linear_step(self.field1, self.kinetic1, self.dz)
        
    def freespace_solver(self, dz, kinetic):
        self.linear_step(self.field1, kinetic, dz, step=1.)