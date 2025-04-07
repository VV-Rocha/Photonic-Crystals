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
    
    exp = af.exp(-(1j * .5*mesh.mesh.dz * (mesh.kXX**2 + mesh.kYY**2) * kinetic))
    
    field[:,:] = field * exp
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
    exp = af.exp(af.constant(-np_float(absorption*dz), 1, 1, dtype=af_complex))
    field[:, :] = field * exp
    
def nonlinear_step(field_a, field_b, coefs, dz, af_complex):
    """Inplace implementation of the nonlinear step of the split-step Fourier method for the 2D NLSE.

    Args:
        field_a (ndarray[:,:]): _description_
        field_b (ndarray[:,:]): _description_
        potential (float): _description_
        potential1 (float): _description_
        dz (float): _description_
        Isat (float): _description_
        Isat1 (float): _description_
        af_complex (af.Dtype.c): _description_
    """
    field_intensity = af.constant(1.0, *field_a.dims(), dtype=af_complex)
    field_intensity[:,:] *= af.abs(field_a)*af.abs(field_a) + af.abs(field_b)*af.abs(field_b)
    
    # nonlinear term
    field_a[:, :] = field_a * af.exp(-1j*dz*coefs.potential_function(field_intensity))
    field_b[:, :] = field_b * af.exp(-1j*dz*coefs.potential_function1(field_intensity))
    
# % TODO: The solver should be adapted to accept an input_field object rather than the fields separately. The the first function or decorator should be constructed to handle the field pre-processing to the solving methods.
def split_step_solver(field, field1, mesh, coefs, precision_control):
    """Inplace single step evolution of the 2D NLSE using the split-step Fourier method.

    Args:
        field (af.Array): _description_
        field1 (af.Array): _description_
        mesh (af_Mesh): _description_
        coefs (NLSE Coefficients Object): _description_
        coefs1 (NLSE Coefficients Object): _description_
        precision_control (PrecisionControl Object): _description_
    """
    linear_step(field, coefs.kinetic, mesh, precision_control.np_complex, precision_control.af_complex)
    linear_step(field1, coefs.kinetic1, mesh, precision_control.np_complex, precision_control.af_complex)
    
    nonlinear_step(field, field1, coefs, mesh.mesh.dz, precision_control.af_complex)
    
    absorption(field, coefs.absorption, mesh.mesh.dz, precision_control.np_float, precision_control.af_complex)
    absorption(field1, coefs.absorption1, mesh.mesh.dz, precision_control.np_float, precision_control.af_complex)
    
    linear_step(field, coefs.kinetic, mesh, precision_control.np_complex, precision_control.af_complex)
    linear_step(field1, coefs.kinetic1, mesh, precision_control.np_complex, precision_control.af_complex)