import numpy as np
import sympy as sp
from math import gcd

from ..utils import approximate_rational, _exact_inputs, _simplify, _all_rational


def _assess_square_lattice(theta):
    """Return (primitive vectors / L, periodic) for square sublattices."""
    theta, _ = _exact_inputs(theta, sp.Integer(1))

    # Floating-point inputs cannot establish exact periodicity.
    if theta.has(sp.Float):
        return None, None

    cos_theta = _simplify(sp.cos(theta))
    sin_theta = _simplify(sp.sin(theta))

    periodic = _all_rational((cos_theta, sin_theta))
    if periodic is not True:
        return None, periodic

    # Avoid the half-angle singularity at theta = pi modulo 2*pi.
    if sin_theta.is_zero is True:
        return np.array([[1, 0], [0, 1]], dtype=object), True

    t = _simplify(sin_theta / (1 + cos_theta))
    m, n = map(int, sp.fraction(t))  # Coprime; n > 0.

    if (((m%2)==0) and ((n%2!=0))) or (((m%2)!=0) and ((n%2==0))):
        a = [
            [n, m],
            [-m, n],
        ]
    elif (((m%2)!=0) and ((n%2!=0))):
        a = [
            [(n + m) // 2, (m - n) // 2],
            [(n - m) // 2, (n + m) // 2],
        ]
    else:
        print("Both cases being even means a common divisor.")

    return np.array(a, dtype=object), True


def _square_lattice_vectors(
    moire_config,
):
    theta = moire_config["theta"]
    alpha = 1
    L = moire_config["a"]
    max_denominator = moire_config["max_denominator"]
    
    a, periodic = _assess_square_lattice(
        theta = theta,
    )

    error = 0. if periodic else None
    
    if not periodic:
        theta = float(theta)
        alpha = float(alpha)
        
        t_target = np.tan(theta / 2) / alpha
        alpha2 = alpha*alpha
        
        m, n, error = approximate_rational(
            t_target,
            max_denominator,
        )
        
        # Reduce m/n first.
        d = gcd(int(m), int(n))
        m, n = int(m) // d, int(n) // d

        g = gcd(n + m, n - m)

        bases = np.array([
            [[n, m], [-m, n]],
            [[(n + m) // g, (m - n) // g],
            [(n - m) // g, (n + m) // g]],
        ], dtype=float)

        areas = np.abs(np.linalg.det(bases))
        a1, a2 = bases[np.argmin(areas)]
        
        a = np.concatenate(
            [
                a1[np.newaxis, :],
                a2[np.newaxis, :],
            ],
            axis = 0,
        )
        
        theta_app = 2 * np.arctan(m/n)
        
    if periodic:
        theta_app = float(theta)
        print("Periodic:", periodic)
    elif not periodic:
        print("Aperiodic:", periodic)
    
    return a * L, error, periodic, theta_app