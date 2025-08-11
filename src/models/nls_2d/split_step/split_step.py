import arrayfire as af

class SplitStepMethods:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def linear_step(self, field, kinetic, np_complex, af_complex):
        """Inplace implementation of the linear step of the split-step Fourier method for the 2D NLSE.
        
        Args:
            field (ndarray[:,:]): _description_
            kinetic (float): _description_
            np_complex (np.complex): _description_
            af_complex (af.Dtype.c): _description_
        """
        field[:,:] = af.signal.fft2(field)
        
        exp = af.exp((1j * .5*self.mesh.dz * (self.mesh.kXX**2 + self.mesh.kYY**2) * kinetic))  # minus sign is absorbed in the kinetic coefficient
        
        field[:,:] = exp * field
        field[:,:] = af.signal.ifft2(field)
        
    def absorption(self, field, absorption, np_float, af_complex):
        """Inplace implementation of the absorption step of the split-step Fourier method for the 2D NLSE.

        Args:
            field (ndarray[:,:]): _description_
            absorption (float): _description_
            dz (float): _description_
            np_float (np.float): _description_
            af_complex (af.Dtype.c): _description_
        """
        exp = af.exp(af.constant(-np_float(absorption*self.mesh.dz), 1, 1, dtype=af_complex))  # absorption is defined as alpha/2
        field[:, :] = field * exp
        
    def nonlinear_step(self, field, potential, af_complex):
        """Inplace implementation of the nonlinear step of the split-step Fourier method for the 2D NLSE.

        Args:
            field (ndarray[:,:]): _description_
            potential (float): _description_
            dz (float): _description_
            af_complex (af.Dtype.c): _description_
        """
        
        # nonlinear term
        field[:, :] = af.exp(-1j*self.mesh.dz*potential) * field[:, :]
    
# % TODO: The solver should be adapted to accept an input_field object rather than the fields separately. The the first function or decorator should be constructed to handle the field pre-processing to the solving methods.
class CoupledSplitStep(SplitStepMethods):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numerical = "Arrayfire"
        
    def step_solver(self,
               fields,
               precision_control,
               ):
        """Inplace single step evolution of the coupled 2D NLSE using the split-step Fourier method.

        Args:
            fields (Fields object): _description_
            mesh (af_Mesh): _description_
            precision_control (PrecisionControl Object): _description_
        """
        # half linear step
        self.linear_step(fields.field, self.kinetic, precision_control.np_complex, precision_control.af_complex)
        self.linear_step(fields.field1, self.kinetic1, precision_control.np_complex, precision_control.af_complex)
        
        # nonlinear step
        auxiliary_intensity = self.potential_function1(fields)
        self.nonlinear_step(fields.field,  # apply nonlinearity in first field.
                    self.potential_function(fields),
                    precision_control.af_complex,
                    )
        # apply nonlinearity in second field with intensity field stored from initial step conditions
        self.nonlinear_step(fields.field1,
                    auxiliary_intensity,
                    precision_control.af_complex,
                    )
        
        # absorption step
        self.absorption(fields.field, self.absorption, precision_control.np_float, precision_control.af_complex)
        self.absorption(fields.field1, self.absorption1, precision_control.np_float, precision_control.af_complex)
        
        # half linear step
        self.linear_step(fields.field, self.kinetic, precision_control.np_complex, precision_control.af_complex)
        self.linear_step(fields.field1, self.kinetic1, precision_control.np_complex, precision_control.af_complex)
    
class SplitStep(SplitStepMethods):
    """Inplace single step evolution of the 2D NLSE using the split-step Fourier method.

    Args:
        field (Field object): _description_
        mesh (af_Mesh): _description_
        precision_control (PrecisionControl Object): _description_
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numerical = "Arrayfire"
        
    def step_solver(self,
               field,
               precision_control,
               ):
        # half linear step
        self.linear_step(field.field, self.kinetic, precision_control.np_complex, precision_control.af_complex)
        
        # nonlinear step
        self.nonlinear_step(field.field,  # apply nonlinearity in first field.
                    self.potential_function(field),
                    precision_control.af_complex,
                    )
        
        # absorption step
        self.absorption(field.field, self.absorption, precision_control.np_float, precision_control.af_complex)

        # half linear step
        self.linear_step(field.field, self.kinetic, precision_control.np_complex, precision_control.af_complex)