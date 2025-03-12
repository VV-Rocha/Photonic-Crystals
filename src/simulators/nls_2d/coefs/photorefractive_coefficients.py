from numpy import pi

class PhotorefractiveCrystalCoefs():
    def __init__(self, crystal_parameters, beam_parameters, adim_method, secondary_beam=None):
        k = 2*pi/beam_parameters["lambda"]
        c = beam_parameters["c"]
        
        if secondary_beam is None:
            n = crystal_parameters["n"]
            alpha = crystal_parameters["alpha"]
            delta_n_max = crystal_parameters["delta_n_max"]
        elif secondary_beam is not None:
            n = crystal_parameters["n"+secondary_beam]
            alpha = crystal_parameters["alpha"+secondary_beam]
            delta_n_max = crystal_parameters["delta_n_max"+secondary_beam]
            
        self.kinetic = .5 * (1/(k * n)) * adim_method.longitudinal_adim_factor / (adim_method.transversal_adim_factor**2)
        self.potential = c * k * adim_method.longitudinal_adim_factor * delta_n_max
        self.absorption = alpha * adim_method.longitudinal_adim_factor