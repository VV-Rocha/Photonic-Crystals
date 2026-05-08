from .decorators import checkpoint


@checkpoint
def dimensionalize_length(
    length,
    model,
):
    """Dimensionalize length.

    Args:
        length (float | ndarray): Adimensional length to be dimensionalized.
        model (str): The model through which the length is being dimensionalized.

    Returns:
        float | ndarray: Dimensional length.
    """
    return length * model.transversal_adim_factor

@checkpoint
def dimensionalize_time(
    time,
    model,
):
    """Dimensionalize time.

    Args:
        time (float | ndarray): Adimensional time to be dimensionalized.
        model (str): The model through which the time is being dimensionalized.

    Returns:
        float | ndarray: Dimensional time.
    """
    return time * model.longitudinal_adim_factor