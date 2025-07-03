from numpy.random import normal

def whitenoise_2d_field(A, shape):
    new_field = normal(0,
                       scale=A,
                       size=shape,
                       )
    return new_field

def introduce_2d_noise(field, A):
    field[:,:] = field * (1. + whitenoise_2d_field(A, field.shape))