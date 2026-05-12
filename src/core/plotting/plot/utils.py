import numpy as np


def xx_yy_in_extent(xx, yy, extent):
    mask = (
        (xx >= extent[0]) &
        (xx <= extent[1]) &
        (yy >= extent[2]) &
        (yy <= extent[3])
    )

    rows, cols = np.where(mask)

    r0, r1 = rows.min(), rows.max() + 1
    c0, c1 = cols.min(), cols.max() + 1

    return xx[r0:r1, c0:c1], yy[r0:r1, c0:c1], (slice(r0, r1), slice(c0, c1))

def get_extent_region(
    xx,
    yy,
    z,
    extent,
):
    if (extent==None):
        return xx, yy, z
    
    xx, yy, idxs = xx_yy_in_extent(
        xx,
        yy,
        extent,
    )
    
    z = z[*idxs]
    
    return xx, yy, z