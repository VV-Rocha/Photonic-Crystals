from functools import wraps

def reset_field(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.init_field()
        return func(self, *args, **kwargs)
    return wrapper