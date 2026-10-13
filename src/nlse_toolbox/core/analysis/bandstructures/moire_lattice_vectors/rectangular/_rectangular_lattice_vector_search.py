import numpy as np
import sympy as sp

from ..utils import approximate_rational, _exact_inputs, _simplify, _all_rational


def _assess_rational_rectangle(
    theta,
    alpha,
):
    theta, alpha = _exact_inputs(theta, alpha)
    
    alpha2 = _simplify(alpha**2)
    
    terms = tuple(_simplify(expr) for expr in (
        sp.cos(theta),
        alpha * sp.sin(theta),
        sp.sin(theta) / alpha,
    ))
    
    periodic = _all_rational(terms)

    if periodic is not True:
        return None, periodic

    # theta = k*pi: the original rectangular basis suffices.
    if terms[1].is_zero is True:
        a = [[1, 0], [0, alpha]]
    else:
        # tan(theta/2) / alpha = (sin(theta)/alpha) / (1 + cos(theta))
        t = _simplify(terms[2] / (1 + terms[0]))
        m, n = sp.fraction(t)
        P, Q = sp.fraction(alpha2)

        a = [
            [n, alpha * m],
            [-P * m, Q * alpha * n],
        ]

    return np.array(a, dtype=object), True
    
def _assess_irrational_rectangle(theta, alpha):
    """Assumes real theta, positive alpha, and irrational alpha**2."""
    theta, alpha = _exact_inputs(theta, alpha)

    sin_theta = _simplify(sp.sin(theta))
    trivial = sin_theta.is_zero

    # theta = k*pi: both constituent lattices coincide.
    if trivial is True:
        return sp.diag(1, alpha), True

    t1 = _simplify(sp.tan(theta / 2) / alpha)
    t2 = _simplify(alpha * sp.tan(theta / 2))

    if t1.is_rational is True:
        m, n = sp.fraction(t1)
        return sp.Matrix([n, alpha * m]), True

    if t2.is_rational is True:
        r, s = sp.fraction(t2)
        return sp.Matrix([-r, alpha * s]), True

    if trivial is False and t1.is_rational is False and t2.is_rational is False:
        return None, False

    return None, None

def _compute_irrational_rectangle(
        theta,
        alpha,
        L,
        max_denominator = 1000,
    ):
    a, periodic = _assess_irrational_rectangle(
        theta,
        alpha,
    )
    error = 0 if periodic else None
    if not periodic:
        theta = float(theta)
        alpha = float(alpha)
        
        t_target = np.tan(theta / 2) / alpha

        m, n, error = approximate_rational(
            t_target,
            max_denominator,
        )
        
        a = np.array([n, alpha*m])
    
    if periodic:
        print("Irrational Periodic:", periodic)
    elif not periodic:
        print("Irrational Aperiodic:", periodic)
    
    return a * L, np.abs(error), periodic


def _compute_rational_rectangle(
    theta,
    alpha,
    L,
    max_denominator = 1000,
):
    a, periodic = _assess_rational_rectangle(
            theta,
            alpha,
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
        
        P, Q, error = approximate_rational(
            alpha2,
            max_denominator,
        )
        
        a1 = np.array([n, alpha*m])
        a2 = np.array([-P*m, Q*alpha*n])
        
        a = np.concatenate(
            [
                a1[np.newaxis, :],
                a2[np.newaxis, :],
            ],
            axis = 0,
        )
    
    if periodic:
        print("Irrational Periodic:", periodic)
    elif not periodic:
        print("Irrational Aperiodic:", periodic)
    
    return a * L, np.abs(error), periodic
    
    
def _rectangular_lattice_vectors(
    moire_config,
    regime,
    max_denominator,
):
    theta = moire_config["theta"]
    alpha = moire_config["alpha"]
    L = moire_config["a"]
    print("L", L)
    if (regime=="irrational"):
        a, error, periodic = _compute_irrational_rectangle(
            theta = theta,
            alpha = alpha,
            L = L,
            max_denominator = max_denominator,
        )
    elif (regime=="rational"):
        a, error, periodic = _compute_rational_rectangle(
                    theta = theta,
                    alpha = alpha,
                    L = L,
                    max_denominator = max_denominator,
                )
    return a, error, periodic