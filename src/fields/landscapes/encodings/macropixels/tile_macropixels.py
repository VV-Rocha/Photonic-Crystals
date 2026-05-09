import numpy as np


def _tile_macropixels(macropixels, mask_shape):
    """
    Tile encoded macropixels into the center of a larger mask.

    Parameters
    ----------
    macropixels : dict
        Dictionary whose values are 2D arrays with identical shape.
    mask_shape : tuple
        Shape of the final mask as (Ny, Nx).

    Returns
    -------
    mask : ndarray
        Final mask with the macropixels tiled at the center.
    """

    n_features = len(macropixels)

    if n_features < 1:
        raise ValueError("macropixels must contain at least one element.")

    Ny, Nx = mask_shape

    cols = int(np.ceil(np.sqrt(n_features)))
    rows = int(np.ceil(n_features / cols))

    first_macro = next(iter(macropixels.values()))
    macro_Ny, macro_Nx = first_macro.shape

    tiled_Ny = rows * macro_Ny
    tiled_Nx = cols * macro_Nx

    if tiled_Ny > Ny or tiled_Nx > Nx:
        raise ValueError(
            "The tiled macropixel region is larger than the final mask. "
            f"Tiled region shape is {(tiled_Ny, tiled_Nx)}, "
            f"but mask shape is {mask_shape}."
        )

    mask = np.zeros(mask_shape, dtype=first_macro.dtype)
    mask += 1.

    y0 = (Ny - tiled_Ny) // 2
    x0 = (Nx - tiled_Nx) // 2

    for idx, (name, macro) in enumerate(macropixels.items()):
        if macro.shape != (macro_Ny, macro_Nx):
            raise ValueError(
                f"Macropixel '{name}' has shape {macro.shape}, "
                f"but expected {(macro_Ny, macro_Nx)}."
            )

        row = idx // cols
        col = idx % cols

        y_start = y0 + row * macro_Ny
        y_end = y_start + macro_Ny

        x_start = x0 + col * macro_Nx
        x_end = x_start + macro_Nx

        mask[y_start:y_end, x_start:x_end] = macro

    return mask