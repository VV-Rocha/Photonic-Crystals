from ...core.mesh import Mesh2D

class GaussianFields():
    from .distributions import landscaped_gaussian
    def __init__(self, mesh, beam1_parameters, beam2_parameters=None):
        self.beam1_parameters = beam1_parameters["w"]
        self.mesh = mesh
        
        if (field2 is True) and (beam2_parameters is not None):
            self.beam2_fields = beam2_parameters
            
    def add_field1(self, landscape=1.):
        wx, wy = self.beam1_parameters["w"]
        
        try:
            I = self.beam1_parameters["I"]
        except KeyError:
            I = 1.
        try:
            power = self.beam1_parameters["power"]
        except KeyError:
            power = 1
        try:
            normed = self.beam1_parameters["normed"]
        except KeyError:
            normed = "max"

        self.field1 = landscaped_gaussian(wx, wy, I=I, landscape=landscape, power=power, normed=normed)
        
    def add_field2(self, landscape=1.):
        wx, wy = self.beam2_parameters["w"]
        
        try:
            I = self.beam2_parameters["I"]
        except KeyError:
            I = 1.
        try:
            power = self.beam2_parameters["power"]
        except KeyError:
            power = 1
        try:
            normed = self.beam2_parameters["normed"]
        except KeyError:
            normed = "max"

        self.field2 = landscaped_gaussian(wx, wy, I=I, landscape=landscape, power=power, normed=normed)
        