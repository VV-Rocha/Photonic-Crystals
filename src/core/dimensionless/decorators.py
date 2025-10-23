def checkpoint(func):
    """ Applies transformation only if adimensionalization is not the identity."""
    def wrapper(self, quantity):
        if hasattr(self, "adimensional_flag"):
            if self.adimensional_flag:
                return func(self, quantity)
            else:
                return quantity
        else:
            return quantity
    return wrapper