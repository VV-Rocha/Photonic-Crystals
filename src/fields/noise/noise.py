from .base import introduce_noise

class WhitenoiseField:
    """ Method class to add white noise to a field."""
    def add_noise(self,):
        """ Add white noise to the field."""
        introduce_noise(self.field, self.noise)
        
class WhitenoiseCoupledFields(WhitenoiseField):
    """ Method class to add white noise to coupled fields."""
    def add_noise(self,):
        """ Add white noise to both coupled fields."""
        super().add_noise()
        introduce_noise(self.field1, self.noise)