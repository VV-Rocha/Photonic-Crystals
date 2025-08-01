from ..single_lattices.two_dimensional import planewave_lattice
from functools import wraps

from typing import Tuple

from numpy import max

def check_tuple(func):
    @wraps(func)
    def wrapper(mesh, a, p, *args, **kwargs):
        if type(a) is not tuple:
            a = (a, a)
        if type(p) is not tuple:
            p = (p, p)
        return func(mesh, a, p, *args, **kwargs)
    return wrapper

def join_lattices(mesh,
                  a,
                  p,
                  rotation,
                  base_lattice,
                  ):
    lattice1 = base_lattice[0](mesh, a[0], rotation[0])
    lattice2 = base_lattice[1](mesh, a[1], rotation[1])
    
    lattice = (p[0]*lattice1 + p[1]*lattice2)/max(p[0]*lattice1 + p[1]*lattice2)
    
    return lattice
    
@check_tuple
def double_lattice(mesh,
                  a: Tuple[float, float],
                  p: Tuple[float, float],
                  rotation: Tuple[float, float],
                  single_lattice=planewave_lattice,
                  join_lattices=join_lattices,
                  ):
    """Calls the join_lattices function to create a two lattice Moiré lattice using the single lattice given in single_lattice.

    Args:
        mesh (_type_): Mesh2D object containing the domain mesh grid.
        a (Tuple[float, float]): Lattice parameters for the two lattices.
        p (Tuple[float, float]): Lattice weights for the two lattices.
        rotation (Tuple[float, float]): Rotation angles of the lattices in radians.
        single_lattice (func, optional): Single lattice function. Defaults to planewave_lattice.
        join_lattices (func, optional): Function to join two lattices. Defaults to join_lattices.

    Returns:
        ndarray: Moiré lattice.
    """
    lattice = join_lattices(mesh,
                            a,
                            p,
                            rotation,
                            single_lattice,
                            )
    return lattice