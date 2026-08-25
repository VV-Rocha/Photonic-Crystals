from .....arrayfire_utils.np_af_interface import from_arrayfire_to_numpy
from .....arrayfire_utils.np_af_interface import  from_numpy_to_arrayfire


def fields_af_to_np(box):
    # convert fields to numpy
    for beam_key, beam_value in box.beams.items():
        beam_value.field = from_arrayfire_to_numpy(beam_value.field)
    
def fields_np_to_af(box):
    # convert fields to arrayfire
    for beam_key, beam_value in box.beams.items():
        beam_value.field = from_numpy_to_arrayfire(beam_value.field)

class AfNpInterface:
    @property
    def arrayfire_flag(self,):
        return True
    
    def init_af(self, box):
        fields_np_to_af(box)

        self.mesh.kxx = from_numpy_to_arrayfire(self.mesh.kxx)
        self.mesh.kyy = from_numpy_to_arrayfire(self.mesh.kyy)
        
    def end_af(self, box):
        fields_af_to_np(box)
        
        self.mesh.kxx = from_arrayfire_to_numpy(self.mesh.kxx)
        self.mesh.kyy = from_arrayfire_to_numpy(self.mesh.kyy)