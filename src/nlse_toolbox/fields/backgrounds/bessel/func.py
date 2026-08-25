from scipy.special import j0


def _bessel0(
    r,
    kr,
):
    return j0(kr * r)