from numpy import exp, pi, abs, zeros, max

from functools import wraps

# % TODO: The mesh.rotate_mesh is reused by every lattice. It should be placed in a decorator.

def square_dimensions(func):
    @wraps(func)
    def wrapper(mesh, a, *args, **kwargs):
        if mesh.dim_flag == "adimensional":
            a = mesh.adim_method.adimensionalize_length(a)
        return func(mesh, a, *args, **kwargs)
    return wrapper

@square_dimensions
def square_planewaves(mesh,
                      a: float,
                      rotation: float,
                      norm: bool = True
                      ):
    """Plots the square lattice in the mesh grid using the superposition of planewaves.

    Args:
        mesh (_type_): Mesh2D object containing the domain mesh grid.
        a (float): Lattice parameter.
        rotation (float): Rotation angle of the lattice in radians.
        norm (bool): Wether to normalize the lattice between [-1,1]. Default True.
        
    Returns:
        ndarray: Square lattice over the mesh grid domain.
    """
    XX, YY = mesh.rotate_mesh(rotation)
    
    lattice = (exp(1j*2*pi*XX/a) + exp(-1j*2*pi*XX/a) + exp(1j*2*pi*YY/a) + exp(-1j*2*pi*YY/a))
    
    if norm:
        lattice /= max(abs(lattice))  ## normalize between [-1,1].
    
    return lattice

@wraps(square_planewaves)
def square(mesh, lattice_parameters, square_planewaves=square_planewaves):
    return square_planewaves(mesh, lattice_parameters)