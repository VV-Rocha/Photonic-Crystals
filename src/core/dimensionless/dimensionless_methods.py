from numpy import pi, sqrt

class WavevectorScale():
    def __init__(self,
                 beam_parameters,
                 crystal_parameters,
                 E0=1.,):
        w = beam_parameters["lambda"]
        n = crystal_parameters["n"]
        bias_field = crystal_parameters["tension"] / crystal_parameters["lx"]
        electro_optic_coef = crystal_parameters["electro_optic_coef"]
        
        delta_n_max = .5 * n**3 * electro_optic_coef * bias_field
        k = 2*pi/w
        
        self.init_transformation_factors(k, n, delta_n_max, E0)
        
    def init_transformation_factors(self, k, n, delta_n_max, E0):
        self.transversal_adim_factor = sqrt(E0) / (k * sqrt(n * delta_n_max))
        self.longitudinal_adim_factor = E0 / (k * delta_n_max)
        
    def adimensionalize_length(self, x):
        return x / self.transversal_adim_factor
    
    def dimensionalize_length(self, x):
        return x * self.transversal_adim_factor
        
    def adimensionalize_time(self, t):
        return t / self.longitudinal_adim_factor
    
    def dimensionalize_time(self, t):
        return t * self.longitudinal_adim_factor