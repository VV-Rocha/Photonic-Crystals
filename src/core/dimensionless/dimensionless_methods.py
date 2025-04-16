from numpy import pi, sqrt

from numpy import ndarray

class DimensionlessMethods:
    """ Dimensionalization transformation functions."""
    def __init__(self,):
        pass
    
    def adimensionalize_length(self, length: float | ndarray) -> float | ndarray:
        """Adimensionalize lenght.

        Args:
            length (float | ndarray): Dimensional length to be adimensionalized.

        Returns:
            float | ndarray: Adimensional length.
        """
        return length / self.transversal_adim_factor
    
    def dimensionalize_length(self, length: float | ndarray) -> float | ndarray:
        """Dimensionalize length.

        Args:
            length (float | ndarray): Adimensional length to be dimensionalized.

        Returns:
            float | ndarray: Dimensional length.
        """
        return length * self.transversal_adim_factor
        
    def adimensionalize_time(self, time: float | ndarray) -> float | ndarray:
        """Adimensionalize time.

        Args:
            time (float | ndarray): Dimensional time to be adimensionalized.

        Returns:
            float | ndarray: Adimensional time.
        """
        return time / self.longitudinal_adim_factor
    
    def dimensionalize_time(self, time: float | ndarray) -> float | ndarray:
        """Dimensionalize time.

        Args:
            time (float | ndarray): Adimensional time to be dimensionalized.

        Returns:
            float | ndarray: Dimensional time.
        """
        return time * self.longitudinal_adim_factor

class Dimensional(DimensionlessMethods):
    def __init__(self,):
        self.transversal_adim_factor = 1.
        self.longitudinal_adim_factor = 1.
        
        super().__init__()

class WavevectorScale(DimensionlessMethods):
    """Adimensionalization to the wavelength scale in photorefractive crystals."""
    def __init__(self,
                 beam_parameters,
                 crystal_parameters,
                 precision_control, E0=1.,):
        """Initialize the scaling factors used for adimensionalization to the wavevector scale in a photorefractive crystal.

        Args:
            beam_parameters (Beam object): Class object defined for carrying the fundamental light beam properties.
            crystal_parameters (_type_): Class object carrying the photorefractive crystal properties.
            precision_control (_type_): Class object with the numerical precision used throughout the algorithms.
            E0 (_type_, optional): Variable scaling parameters. Defaults to 1..
        """
        w = beam_parameters.wavelength
        n = crystal_parameters.n
        
        delta_n_max = crystal_parameters.delta_n_max
        k = 2*pi/w
                
        ## init scaling factors
        self.transversal_adim_factor = precision_control.np_float(sqrt(E0) / (k * sqrt(n * delta_n_max)))
        self.longitudinal_adim_factor = precision_control.np_float(E0 / (k * delta_n_max))
        
        super().__init__()