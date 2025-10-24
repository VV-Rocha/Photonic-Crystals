def delta_n_max(n, electro_optic_coef, tension, Lx):
    return .5 * n**3 * electro_optic_coef * tension / Lx

def second_value(string, crystal_config):
    if string in crystal_config.keys():
        param = crystal_config[string]
    else:
        param = crystal_config[string[:-1]]
    return param

class PhotorefractiveCrystalParameters:
    """A class representing a photorefractive crystal parameters with a single incident beam."""
    def __init__(
        self,
        crystal_config,
        *args,
        **kwargs,
        ):
        """Initialize the photorefractive crystal when a single beam is being used.

        Args:
            crystal_config (dict): Dictionary with all the physical parameters required to initiate the object.
        """
        self.n = crystal_config["n"]
        self.electro_optic_coef = crystal_config["electro_optic_coef"]
        self.tension = crystal_config["tension"]
        self.Isat = crystal_config["Isat"]
        self.alpha = crystal_config["alpha"]
        
        self.Lx = crystal_config["Lx"]
        self.Ly = crystal_config["Ly"]
        self.Lz = crystal_config["Lz"]
        
        self.Isat = crystal_config["Isat"]
        
        # Computes and initializes the delta_n_max variable.
        self.delta_n_max = delta_n_max(self.n, self.electro_optic_coef, self.tension, self.Lx)
                        
        super().__init__(
            *args,
            **kwargs,
            )

class CoupledPhotorefractiveCrystalParameters(PhotorefractiveCrystalParameters):
    """A class representing a photorefractive crystal parameteres for two incident beams."""
    def __init__(
        self,
        crystal_config,
        *args,
        **kwargs,
        ):
        """Initialize the photorefractive crystal when using two light beams.

        Args:
            crystal_config (dict): Dictionary with all the physical parameters required to initiate the object.
        """
        self.n1 = second_value("n1", crystal_config)
        self.electro_optic_coef1 = second_value("electro_optic_coef1", crystal_config)
        self.alpha1 = second_value("alpha1", crystal_config)
        
        super().__init__(
            crystal_config = crystal_config,
            *args,
            **kwargs,
            )
        
        # Computes and initializes the delta_n_max for the second beam.
        self.delta_n_max1 = delta_n_max(self.n1, self.electro_optic_coef1, self.tension, self.Lx)