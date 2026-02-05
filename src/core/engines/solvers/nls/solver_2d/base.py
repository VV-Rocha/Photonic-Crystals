import arrayfire as af

class SplitStepMethods:
    def linear_step(self, field, kinetic, dz, step=.5):
        """Inplace implementation of the linear step of the split-step Fourier method for the 2D NLSE.

        Args:
            field (_type_): _description_
            kinetic (_type_): _description_
        """
        field[:,:] = af.signal.fft2(field)
        
        exp = af.exp((1j * step*dz * (self.kxx**2 + self.kyy**2) * kinetic))  # minus sign is absorbed in the kinetic coefficient
        
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
        return af.exp(af.constant(-self.absorption*self.dz, 1, 1, dtype=self.field.dtype()))

    @property
    def exp1(self,):
        return af.exp(af.constant(-self.absorption1*self.dz, 1, 1, dtype=self.field.dtype()))
        
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
