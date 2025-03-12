import numpy as np


def gaussian_25(xx, yy, wx, wy, power):
    return np.exp(-(.25*(xx/wx)**2 + (yy/wy)**2)**power)

def landscaped_gaussian(mesh, wx, wy, I=1., landscape=1., power=1, normed="density"):
    input_state = np.zeros((mesh.Nx, mesh.Ny), dtype=complex)
    
    input_state += gaussian_25(mesh.XX, mesh.YY, wx, wy, power)
    
    input_state *= landscape

    if normed == "density":
        input_state /= np.sum(np.abs(input_state)**2*mesh.dx*mesh.dy)
    elif normed == "max":
        input_state /= np.abs(input_state).max()
    
    input_state = np.sqrt(I) * input_state
    
    return input_state