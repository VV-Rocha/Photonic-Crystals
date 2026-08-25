import arrayfire as af

from ......arrayfire_utils.facade import Arrayfire
from ...iterators.solver import AfTimeSpaceAnalogIterator
from ......storage.store_methods import StorageField

from .mesh import SplitStepMesh

class SplitStepMethods:
    def linear_step(self, field, kinetic):
        """ Perform the linear step in the split-step method."""
        field[:] = af.signal.fft(field)
        
        exp = af.exp(1j * .5*self.dz * self.kx**2 * kinetic)
        
        field[:] = exp * field
        field[:] = af.signal.ifft(field)
        
    def absorption_step(self, field, absorption):
        """ Perform the absorption step in the split-step method."""
        x = -absorption*self.dz
        exp = af.exp(af.constant(x, 1, 1, dtype=field.dtype()))
        field[:] = field * exp
        
    def nonlinear_step(self, field, potential):
        """ Perform the nonlinear step in the split-step method."""
        field[:] = af.exp(-1j*self.dz*potential) * field[:]
        
class SplitStepSolver(StorageField, Arrayfire, SplitStepMesh, SplitStepMethods, AfTimeSpaceAnalogIterator):
    def init_solver(self,):
        """ Initialize the solver by setting device and initializing mesh."""
        self.set_device()
        
        self.init_mesh()
    
    def af_get_intensity(self,):
        """ Compute the intensity of the field in arrayfire."""
        return (self.field) * af.conjg(self.field)
    
    def af_potential_function(self, field, potential):
        """ Compute the nonlinear potential function in arrayfire."""
        return self.potential * (self.af_get_intensity() / (self.Isat + self.af_get_intensity()))
    
    def step_solver(self, ):
        """ Perform a single step of the split-step solver."""
        self.linear_step(self.field, self.kinetic)
        
        self.nonlinear_step(self.field,
                            self.af_potential_function(self.field, self.potential))
        
        self.absorption_step(self.field, self.absorption)
        
        self.linear_step(self.field, self.kinetic)