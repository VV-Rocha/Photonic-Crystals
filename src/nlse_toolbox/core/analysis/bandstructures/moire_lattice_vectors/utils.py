import sympy as sp
from fractions import Fraction


def approximate_rational(
    t_target,
    max_denominator=1000,
):
    ratio = Fraction(t_target).limit_denominator(max_denominator)
    m, n = ratio.numerator, ratio.denominator
    error = abs(t_target - m / n)
    return m, n, error

def _exact_inputs(theta, alpha):
    theta, alpha = sp.sympify(theta), sp.sympify(alpha)
    if theta.has(sp.Float) or alpha.has(sp.Float):
        raise ValueError("Use exact SymPy expressions, not floating-point inputs.")
    return theta, alpha

def _simplify(expr):
    return sp.simplify(sp.trigsimp(sp.expand_trig(expr)))

def _all_rational(expressions):
    checks = [expr.is_rational for expr in expressions]
    if any(check is False for check in checks):
        return False
    if all(check is True for check in checks):
        return True
    return None