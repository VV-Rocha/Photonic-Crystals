from ..single_lattices.square import square_planewaves
from functools import wraps

from typing import Tuple

def join_lattices(mesh,
                  a,
                  p,
                  rotation,
                  base_lattice,
                  base_lattice1,
                  ):
    lattice1 = base_lattice(mesh, a[0], rotation[0])
    lattice2 = base_lattice1(mesh, a[1], rotation[1])
    
    return p[0]*lattice1 + p[1]*lattice2
    
def double_square(mesh,
                  a: Tuple[float, float],
                  p: Tuple[float, float],
                  rotation: Tuple[float, float],
                  single_lattice=square_planewaves,
                  join_lattices=join_lattices,
                  ):
    """Calls the join_lattices function to create a two lattice Moiré lattice using the single lattice given in single_lattice.

    Args:
        mesh (_type_): Mesh2D object containing the domain mesh grid.
        a (Tuple[float, float]): Lattice parameters for the two lattices.
        p (Tuple[float, float]): Lattice weights for the two lattices.
        rotation (Tuple[float, float]): Rotation angles of the lattices in radians.
        single_lattice (func, optional): Single lattice function. Defaults to square_planewaves.
        join_lattices (func, optional): Function to join two lattices. Defaults to join_lattices.

    Returns:
        ndarray: Moiré lattice.
    """
    lattice = join_lattices(mesh,
                            a,
                            p,
                            rotation,
                            single_lattice,
                            single_lattice,
                            )
    return lattice