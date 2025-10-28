from numpy import conjugate, angle, zeros, complex128, float64

from .decorators import reset_field


class Field:
    """ Base Field Class."""
    def __init__(self, *args, **kwargs):
        """ Initialize Field attributes."""
        super().__init__(*args, **kwargs)
        
        self.init_field()  ## allocates a place in memory
                
    @property
    def nfields(self,):
        return "single"
    
    def get_intensity(self,):
        """ Get the intensity of the field."""
        return ((self.field) * conjugate(self.field)).astype(float64)

    def get_total_intensity(self,):
        """ Get the total intensity of the field."""
        return self.get_intensity()

    def get_angle(self,):
        """ Get the phase angle of the field."""
        return angle(self.field)

    def init_field(self,):
        """ Initialize the field array."""
        self.field = zeros(self.field_shape, dtype=complex128)
        
class CoupledFields:
    """ Base Coupled Fields Class."""
    def __init__(self, *args, **kwargs):
        """ Initialize Coupled Field attributes."""
        super().__init__(*args, **kwargs)
        
        self.init_field()
        
    @property
    def nfields(self,):
        return "two"
        
    def init_field(self,):
        """ Initialize the coupled field arrays."""
        self.field = zeros(self.field_shape, dtype=complex128)
        self.field1 = zeros(self.field_shape, dtype=complex128)
        
    def get_intensity(self,):
        """ Get the intensity of the first field."""
        return ((self.field) * conjugate(self.field)).astype(float64)
    
    def get_intensity1(self,):
        """ Get the intensity of the second field."""
        return ((self.field1) * conjugate(self.field1)).astype(float64)
    
    def get_total_intensity(self,):
        """ Get the total intensity of both fields."""
        return self.get_intensity() + self.get_intensity1()
    
    def get_angle(self,):
        """ Get the phase angle of the first field."""
        return angle(self.field)
    
    def get_angle1(self,):
        """ Get the phase angle of the second field."""
        return angle(self.field1)
    
class Modulation:
    """ Base Modulation Class."""
    @reset_field
    def modulate_field(self,):
        """ Modulate the field with envelope and landscape functions."""
        self.field += self.envelope_function()
        self.field *= self.landscape_function()
        
    def adimensionalize_field(self,):
        """ Adimensionalize both envelope and landscape functions."""
        self.adimensionalize_envelope()
        self.adimensionalize_landscape()
        
class CoupledModulation(Modulation):
    """ Base Coupled Modulation Class."""
    @reset_field
    def modulate_field(self,):
        """ Modulate both fields with their respective envelope and landscape functions."""
        super().modulate_field()
        self.modulate_field1()
        
    def modulate_field1(self,):
        """ Modulate the second field with its envelope and landscape functions."""
        self.field1 += self.envelope_function1()
        self.field1 *= self.landscape_function1()