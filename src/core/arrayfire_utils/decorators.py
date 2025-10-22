from numpy import array, float32, float64

def scalar_to_list(func):
    def wrapper(self, quantity):
        if type(quantity) in [float, int, float32, float64]:
            quantity = array([quantity])
        return func(self, quantity)
    return wrapper