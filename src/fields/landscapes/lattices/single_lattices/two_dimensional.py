from numpy import exp, pi, abs, zeros, max
from numpy import ndarray, array

from functools import wraps
from typing import Tuple


# % TODO: The mesh.rotate_mesh is reused by every lattice. It should be placed in a decorator.

def lattice_reciprocal_outer(vectors):
    """Get the reciprocal lattices for the 2D lattice vectors."""
    denominator = vectors[0][0]*vectors[1][1] - vectors[0][1]*vectors[1][0]
    # compute reciprocal lattice vectors
    b1 = [2*pi*vectors[1][1]/ denominator, -2*pi*vectors[1][0]/ denominator]
    b2 = [2*pi*vectors[0][1]/ denominator, -2*pi*vectors[0][0]/ denominator]
    
    vectors[0, 0], vectors[0, 1] = b1[0], b1[1]
    vectors[1, 0], vectors[1, 1] = b2[0], b2[1]
    return vectors

def general_planewaves(mesh,
                      reciprocal_vectors: float | Tuple[float, float],
                      rotation: float,
                      ):
    XX, YY = mesh.rotate_mesh(rotation)
    
    lattice = exp(1j * (reciprocal_vectors[0][0]*XX + reciprocal_vectors[0][1]*YY)) + exp(1j * (reciprocal_vectors[1][0]*XX + reciprocal_vectors[1][1]*YY))
    
    lattice += exp(-1j * (reciprocal_vectors[0][0]*XX + reciprocal_vectors[0][1]*YY)) + exp(-1j * (reciprocal_vectors[1][0]*XX + reciprocal_vectors[1][1]*YY))  ## c.c.
    
    lattice /= max(abs(lattice))  ## normalize between [-1,1].
    
    return lattice

def dimensions(func):
    @wraps(func)
    def wrapper(mesh, a, *args, **kwargs):
        if mesh.dim_flag == "adimensional":
            if (type(a) == list) or (type(a) == ndarray) or (type(a) == tuple):
                a[0] = mesh.adim_method.adimensionalize_length(a[0])
                a[1] = mesh.adim_method.adimensionalize_length(a[1])
            elif type(a) == float:
                a = mesh.adim_method.adimensionalize_length(a)
                a = array([a,a])
        return func(mesh, a, *args, **kwargs)
    return wrapper

@dimensions
def planewave_lattice(mesh,
                      lattice_parameters,
                      rotation: float = 0.,
                      lattice_type: str = "square",
                      ):
    # choose lattice vectors
    if (lattice_type.lower() == "square") or (lattice_type.lower() == "rectangular"):
        lattice_vectors = array([[1.,0.],[0.,1.]])
        
    lattice_vectors[0] *= lattice_parameters[0]
    lattice_vectors[1] *= lattice_parameters[1]
    
    reciprocal_vectors = lattice_reciprocal_outer(lattice_vectors)
    
    return general_planewaves(mesh,
                              reciprocal_vectors=reciprocal_vectors,
                              rotation=rotation)