def checkpoint(func):
    """ Applies transformation only if adimensionalization is not the identity."""
    def wrapper(quantity, model):
        if hasattr(model, "adimensional_flag"):
            if model.adimensional_flag:
                return func(quantity, model)
            else:
                return quantity
        else:
            return quantity
    return wrapper