from ....core.mesh import Mesh2D
from ..coefs import PhotorefractiveCrystalCoefs

class CoupledSimulationBox:
    def __init__(self,
                 medium_parameters,
                 beam1_parameters,
                 beam2_parameters,
                 adim_method,
                 solver_method,
                 N=(256,256,10)):
        l = (medium_parameters["lx"], medium_parameters["ly"], medium_parameters["lz"])
        self.N = N
        
        self.adim_method = adim_method
        
        self.mesh = Mesh2D(medium_parameters, N)        
        self.mesh_adim = Mesh2D(medium_parameters, N, adim_method=adim_method)
        
        self.solver_method = solver_method
        
        self.eq1_coefs = PhotorefractiveCrystalCoefs(medium_parameters, beam1_parameters, adim_method)
        self.eq2_coefs = PhotorefractiveCrystalCoefs(medium_parameters, beam2_parameters, adim_method)