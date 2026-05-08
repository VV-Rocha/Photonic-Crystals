import numpy as np


def ShiqiXia_ssh_modulation(
    xx,
    a,
    c,
    intra_cell,
    dimerization = .8,
):
    """
    Function plotting SSH according to the paper "Nontrivial coupling of light into a defect: the interplay of nonlinearity and topology" by Shiqi Xia, et al.

    Args:
        xx (_type_): xx meshgrid
        a (_type_): lattice parameter
        c (_type_): reference center
        intra_cell (_type_): distance between sites A and B, in units of lattice parameters
        dimerization (float, optional): ratio between intensities. Defaults to .8.
    """
    return np.sqrt(dimerization * np.cos((np.pi*(xx-c)/(a)))**2 + np.cos(np.pi*(xx-c-intra_cell*a)/(a/2))**2)
    
def site_by_site_ssh(
    xx,
    a,
    c,
    intra_cell=0.25,
    dimerization=0.5,
    sigma=0.08,
    amp_A=1.0, 
):
    """
    a: unit-cell period
    c: reference center
    intra_cell: position of B site as fraction of a
    sigma: site width as fraction of a
    amp_A, amp_B: relative site heights
    """
    mod = np.zeros_like(xx)

    n_min = int(np.floor(xx.min() / a)) - 1
    n_max = int(np.ceil(xx.max() / a)) + 1

    for n in range(n_min, n_max + 1):
        xA = n * a
        xB = n * a + intra_cell * a

        mod += amp_A * np.exp(-(xx - xA - c)**2 / (2 * (sigma*a)**2))
        mod += dimerization * np.exp(-(xx - xB - c)**2 / (2 * (sigma*a)**2))

    return mod