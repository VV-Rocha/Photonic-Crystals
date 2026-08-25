import arrayfire as af

def exp_coefficient(absorption, dz):
    return af.exp(af.constant(-absorption*dz, 1, 1, dtype=af.Dtype.c64))