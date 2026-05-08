import arrayfire as af


def _linear_step(
    field,
    kinetic,
    kxx,
    kyy,
    dz,
    step = .5,
):
    """
    Inplace implementation of the linear step of the split-step Fourier method for the 2D NLSE.

    Args:
        field (_type_): field to be evolved
        kinetic (_type_): kinetic coefficient
        kxx (_type_): x-component of the wavevector
        kyy (_type_): y-component of the wavevector
        dz (_type_): step size
        step (float, optional): fraction of the linear step to be applied. Defaults to .5.
    """
    field[:,:] = af.signal.fft2(field)

    exp = af.exp((1j * step*dz * (kxx**2 + kyy**2) * kinetic))  # minus sign is absorbed in the kinetic coefficient
        
    field[:,:] = exp * field
    field[:,:] = af.signal.ifft2(field)

def _nonlinear_step(
    field,
    potential,
    dz,
):
    """
    Inplace implementation of the nonlinear step of the split-step Fourier method for the 2D NLSE.

    Args:
        field (ndarray[:,:]): field to be evolved
        potential (float): potential function and nonlinear coefficient
        dz (float): step size
    """
        
    # nonlinear term
    field[:, :] = af.exp(-1j*dz*potential) * field[:, :]

def _absorption_step(field, exp):
    """
    Inplace implementation of the absorption step of the split-step Fourier method for the 2D NLSE.

    Args:
        field (ndarray[:,:]): field to be evolved
        exp (float): absorption coefficient
    """
    field[:, :] = field[:, :] * exp