from .base import introduce_noise

class WhitenoiseField:
    """ Method class to add white noise to a field."""
    def add_noise(
        self,
        noise,
    ):
        """ Add white noise to the field."""
        introduce_noise(self.field, noise)