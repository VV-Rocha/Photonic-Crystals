from functools import wraps

def default_potential(func):
    @wraps(func)
    def wrapper(self, field, potential):
        if potential is None:
            potential = self.potential
        return func(self, field, potential)
    return wrapper

def default_potential1(func):
    @wraps(func)
    def wrapper(self, potential):
        if potential is None:
            potential = self.potential1
        return func(self, potential)
    return wrapper