import arrayfire as af

from .step_functions import _linear_step, _nonlinear_step, _absorption_step
from .utils import exp_coefficient
    
class StepMethods:
    def step_solver(self, box):
        """Inplace single step evolution of the 2D NLSE using the split-step Fourier method.
        """
        # half linear step
        self.linear_step(box)
        
        # nonlinear step
        self.nonlinear_step(box)
        
        # absorption step
        self.absorption_step(box)
        
        # half linear step
        self.linear_step(box)
        
    def linear_step(self, box):
        for beam_key, beam_value in box.beams.items():
            if beam_value.dynamics:
                _linear_step(
                    beam_value.field,
                    box.model.beam_coefs[beam_key].kinetic,
                    self.mesh.kxx,
                    self.mesh.kyy,
                    self.mesh.dz,
                )
    
    def af_get_intensity(self, box):
        first = True
        for beam_value in box.beams.values():
            if first:
                total_field_intensity = (beam_value.field)*af.conjg(beam_value.field)
                first = False
            else:
                total_field_intensity += (beam_value.field)*af.conjg(beam_value.field)
        return total_field_intensity
    
    def _potential(
        self,
        potential,
        total_intensity_field,
        Isat,
    ):
        return potential * (total_intensity_field / (Isat + total_intensity_field))
    
    def nonlinear_step(
        self,
        box,
    ):
        total_intensity_field = self.af_get_intensity(box)
        
        for beam_key, beam_value in box.beams.items():
            if beam_value.dynamics:
                potential_field = self._potential(
                    box.model.beam_coefs[beam_key].potential,
                    total_intensity_field,
                    box.media.shared_properties.Isat,
                )
                _nonlinear_step(
                    beam_value.field,
                    potential_field,
                    self.mesh.dz,
                )
            
    def absorption_step(self, box):
        for beam_key, beam_value in box.beams.items():
            if beam_value.dynamics:
                _absorption_step(
                    beam_value.field,
                    exp_coefficient(
                        box.model.beam_coefs[beam_key].absorption,
                        self.mesh.dz
                    )
                )