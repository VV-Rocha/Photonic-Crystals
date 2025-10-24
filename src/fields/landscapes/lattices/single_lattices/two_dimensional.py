import numpy as np

from typing import Tuple

def lattice_reciprocal_outer(vectors: np.ndarray) -> np.ndarray:
    """Get the reciprocal lattices for the 2D lattice vectors.

    Args:
        vectors (np.ndarray): Lattice vectors.

    Returns:
        np.ndarray: Reciprocal lattice vectors.
    """
    denominator = vectors[0][0]*vectors[1][1] - vectors[0][1]*vectors[1][0]
    # compute reciprocal lattice vectors
    b1 = [2*np.pi*vectors[1][1]/ denominator, -2*np.pi*vectors[1][0]/ denominator]
    b2 = [2*np.pi*vectors[0][1]/ denominator, -2*np.pi*vectors[0][0]/ denominator]
    
    vectors[0, 0], vectors[0, 1] = b1[0], b1[1]
    vectors[1, 0], vectors[1, 1] = b2[0], b2[1]
    return vectors

def general_planewaves(
    xx: np.ndarray,
    yy: np.ndarray,
    reciprocal_vectors: np.ndarray,
) -> np.ndarray:
    """Generate a general planewave lattice.

    Args:
        xx (np.ndarray): -x- coordinates meshgrid.
        yy (np.ndarray): -y- coordinates meshgrid.
        reciprocal_vectors (np.ndarray): Reciprocal lattice vectors.

    Returns:
        np.ndarray: Planewave lattice array.
    """
    lattice = np.exp(1j * (reciprocal_vectors[0][0]*xx + reciprocal_vectors[0][1]*yy)) + np.exp(1j * (reciprocal_vectors[1][0]*xx + reciprocal_vectors[1][1]*yy))
    
    lattice += np.exp(-1j * (reciprocal_vectors[0][0]*xx + reciprocal_vectors[0][1]*yy)) + np.exp(-1j * (reciprocal_vectors[1][0]*xx + reciprocal_vectors[1][1]*yy))  ## c.c.
    
    lattice /= np.max(np.abs(lattice))  ## normalize between [-1,1].
    
    return lattice

def planewave_lattice(
    xx: np.ndarray,
    yy: np.ndarray,
    lattice_parameters: Tuple[float, float],
    lattice_type: str = "square",
) -> np.ndarray:
    """Generate a planewave lattice.

    Args:
        xx (np.ndarray): -x- coordinates meshgrid.
        yy (np.ndarray): -y- coordinates meshgrid.
        lattice_parameters (Tuple[float, float]): Lattice parameters (a1, a2).
        lattice_type (str, optional): Type of lattice to generate. Defaults to "square".

    Returns:
        np.ndarray: Planewave lattice array.
    """
    # choose lattice vectors
    if (lattice_type.lower() == "square") or (lattice_type.lower() == "rectangular"):
        lattice_vectors = np.array([[1.,0.],[0.,1.]])
        
    lattice_vectors[0] *= lattice_parameters[0]
    lattice_vectors[1] *= lattice_parameters[1]
    
    reciprocal_vectors = lattice_reciprocal_outer(lattice_vectors)
    
    return general_planewaves(
        xx,
        yy,
        reciprocal_vectors=reciprocal_vectors,
    )