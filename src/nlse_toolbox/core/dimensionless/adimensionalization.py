from .decorators import checkpoint


@checkpoint
def adimensionalize_length(
    length,
    model,
):
    """Adimensionalize length.

    Args:
        length (float | ndarray): Dimensional length to be adimensionalized.
        model (str): The model through which the length is being dimensionalized.

    Returns:
        float | ndarray: Adimensional length.
    """
    return length / model.transversal_adim_factor

@checkpoint
def adimensionalize_time(
    time,
    model,
):
    """Adimensionalize time.

    Args:
        time (float | ndarray): Dimensional time to be adimensionalized.
        model (str): The model through which the time is being dimensionalized.

    Returns:
        float | ndarray: Adimensional time.
    """
    return time / model.longitudinal_adim_factor