import arrayfire as af

from ......arrayfire_utils.facade import Arrayfire

from ......storage.store_methods import CoupledStorageField

from .mesh import SplitStepMesh

from ...iterators.solver import AfTimeSpaceAnalogIterator

class SplitStepMethods:
    def linear_step(self, field, kinetic):
        """Inplace implementation of the linear step of the split-step Fourier method for the 2D NLSE.

        Args:
            field (_type_): _description_
            kinetic (_type_): _description_
        """
        field[:,:] = af.signal.fft2(field)
        
        exp = af.exp((1j * .5*self.dz * (self.kxx**2 + self.kyy**2) * kinetic))  # minus sign is absorbed in the kinetic coefficient
        
        field[:,:] = exp * field
        field[:,:] = af.signal.ifft2(field)
        
    def absorption_step(self, field, exp):
        """Inplace implementation of the absorption step of the split-step Fourier method for the 2D NLSE.

        Args:
            field (ndarray[:,:]): _description_
            absorption (float): _description_
            dz (float): _description_
            np_float (np.float): _description_
            af_complex (af.Dtype.c): _description_
        """
        field[:, :] = field * exp
        
    @property
    def exp(self,):
        return af.exp(af.constant(-self.alpha*self.dz, 1, 1, dtype=self.field.dtype()))

    @property
    def exp1(self,):
        return af.exp(af.constant(-self.alpha1*self.dz, 1, 1, dtype=self.field.dtype()))
        
    def nonlinear_step(self, field, potential):
        """Inplace implementation of the nonlinear step of the split-step Fourier method for the 2D NLSE.

        Args:
            field (ndarray[:,:]): _description_
            potential (float): _description_
            dz (float): _description_
            af_complex (af.Dtype.c): _description_
        """
        
        # nonlinear term
        field[:, :] = af.exp(-1j*self.dz*potential) * field[:, :]
    

class CoupledSplitStepSolver(CoupledStorageField, Arrayfire, SplitStepMesh, SplitStepMethods, AfTimeSpaceAnalogIterator):
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

        Args:
            fields (Fields object): _description_
            mesh (af_Mesh): _description_
            precision_control (PrecisionControl Object): _description_
        """
        # half linear step
        self.linear_step(self.field, self.kinetic)
        self.linear_step(self.field1, self.kinetic1)
        
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
        self.linear_step(self.field, self.kinetic)
        self.linear_step(self.field1, self.kinetic1)