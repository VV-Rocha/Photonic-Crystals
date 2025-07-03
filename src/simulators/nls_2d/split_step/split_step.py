import arrayfire as af

def linear_step(field, kinetic, mesh, np_complex, af_complex):
    """Inplace implementation of the linear step of the split-step Fourier method for the 2D NLSE.
    
    Args:
        field (ndarray[:,:]): _description_
        kinetic (float): _description_
        mesh (af_Mesh2D): _description_
        np_complex (np.complex): _description_
        af_complex (af.Dtype.c): _description_
    """
    field[:,:] = af.signal.fft2(field)
    
    exp = af.exp((1j * .5*mesh.mesh.dz * (mesh.kXX**2 + mesh.kYY**2) * kinetic))  # minus sign is absorbed in the kinetic coefficient
    
    field[:,:] = exp * field
    field[:,:] = af.signal.ifft2(field)
    
def absorption(field, absorption, dz, np_float, af_complex):
    """Inplace implementation of the absorption step of the split-step Fourier method for the 2D NLSE.

    Args:
        field (ndarray[:,:]): _description_
        absorption (float): _description_
        dz (float): _description_
        np_float (np.float): _description_
        af_complex (af.Dtype.c): _description_
    """
    exp = af.exp(af.constant(-np_float(absorption*dz), 1, 1, dtype=af_complex))  # absorption is defined as alpha/2
    field[:, :] = field * exp
    
def nonlinear_step(field, potential, dz, af_complex):
    """Inplace implementation of the nonlinear step of the split-step Fourier method for the 2D NLSE.

    Args:
        field (ndarray[:,:]): _description_
        potential (float): _description_
        dz (float): _description_
        af_complex (af.Dtype.c): _description_
    """
    
    # nonlinear term
    field[:, :] = af.exp(-1j*dz*potential) * field[:, :]
    
# % TODO: The solver should be adapted to accept an input_field object rather than the fields separately. The the first function or decorator should be constructed to handle the field pre-processing to the solving methods.
class CoupledSplitStep:
    def __init__(self,):
        self.numerical = "Arrayfire"
        
    def solver(self,
               fields,
               mesh,
               coefs,
               precision_control,
               ):
        """Inplace single step evolution of the coupled 2D NLSE using the split-step Fourier method.

        Args:
            fields (Fields object): _description_
            mesh (af_Mesh): _description_
            coefs (NLSE Coefficients Object): _description_
            precision_control (PrecisionControl Object): _description_
        """
        # half linear step
        linear_step(fields.field, coefs.kinetic, mesh, precision_control.np_complex, precision_control.af_complex)
        linear_step(fields.field1, coefs.kinetic1, mesh, precision_control.np_complex, precision_control.af_complex)
        
        # nonlinear step
        auxiliary_intensity = coefs.potential_function1(fields)
        nonlinear_step(fields.field,  # apply nonlinearity in first field.
                    coefs.potential_function(fields),
                    mesh.mesh.dz,
                    precision_control.af_complex,
                    )
        # apply nonlinearity in second field with intensity field stored from initial step conditions
        nonlinear_step(fields.field1,
                    auxiliary_intensity,
                    mesh.mesh.dz,
                    precision_control.af_complex,
                    )
        
        # absorption step
        absorption(fields.field, coefs.absorption, mesh.mesh.dz, precision_control.np_float, precision_control.af_complex)
        absorption(fields.field1, coefs.absorption1, mesh.mesh.dz, precision_control.np_float, precision_control.af_complex)
        
        # half linear step
        linear_step(fields.field, coefs.kinetic, mesh, precision_control.np_complex, precision_control.af_complex)
        linear_step(fields.field1, coefs.kinetic1, mesh, precision_control.np_complex, precision_control.af_complex)
    
class SplitStep():
    """Inplace single step evolution of the 2D NLSE using the split-step Fourier method.

    Args:
        field (Field object): _description_
        mesh (af_Mesh): _description_
        coefs (NLSE Coefficients Object): _description_
        precision_control (PrecisionControl Object): _description_
    """
    def __init__(self,):
        self.numerical = "Arrayfire"
        
    def solver(self,
               field,
               mesh,
               coefs,
               precision_control,
               ):
        # half linear step
        linear_step(field.field, coefs.kinetic, mesh, precision_control.np_complex, precision_control.af_complex)
        
        # nonlinear step
        nonlinear_step(field.field,  # apply nonlinearity in first field.
                    coefs.potential_function(field),
                    mesh.mesh.dz,
                    precision_control.af_complex,
                    )
        
        # absorption step
        absorption(field.field, coefs.absorption, mesh.mesh.dz, precision_control.np_float, precision_control.af_complex)

        # half linear step
        linear_step(field.field, coefs.kinetic, mesh, precision_control.np_complex, precision_control.af_complex)