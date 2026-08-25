import arrayfire as af


def set_device(
    device = 0,
):
    """
    Set the arrayfire device to be used for computations.

    Args:
        device (int, optional): device ID to be used for arrayfire computations. Defaults to 0.
    """
    # af.set_backend(backend)
    af.set_device(device)
    print("Backend:", af.get_active_backend())
    print(af.info()) 