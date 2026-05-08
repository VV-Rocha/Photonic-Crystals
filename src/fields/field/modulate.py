from functools import wraps


def reset_field(func):
    @wraps(func)
    def wrapper(self, box):
        self.init_field(box)
        return func(self, box)
    return wrapper

class Modulation:
    """ Base Modulation Class."""
    def init(self, box):
        """Initialize Field"""
        self.modulate(box.mesh)
    
    @reset_field
    def modulate(self, box):
        """ Modulate the field with envelope and landscape functions."""
        self.field += self.envelope_function(box)
        self.field *= self.landscape_function(box)