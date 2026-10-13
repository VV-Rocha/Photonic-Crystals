import numpy as np

from typing import Tuple


def lattice_reciprocal_outer(vectors: np.ndarray) -> np.ndarray:
    a1, a2 = np.asarray(vectors, dtype=float)
    denominator = a1[0]*a2[1] - a1[1]*a2[0]

    return (2*np.pi / denominator) * np.array([
        [ a2[1], -a2[0]],
        [-a1[1],  a1[0]],
    ])

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