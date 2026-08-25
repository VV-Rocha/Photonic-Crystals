from numpy import conjugate, angle, zeros, complex128, float64

from .modulate import Modulation


class Field(Modulation):
    """ Base Field Class."""
    def get_intensity(self,):
        """ Get the intensity of the field."""
        return ((self.field) * conjugate(self.field)).astype(float64)

    def get_total_intensity(self,):
        """ Get the total intensity of the field."""
        return self.get_intensity()

    def get_angle(self,):
        """ Get the phase angle of the field."""
        return angle(self.field)

    def init_field(self, box):
        """ Initialize the field array."""
        self.field = zeros(box.field_shape, dtype=complex128)