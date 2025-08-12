def delta_n_max(n, electro_optic_coef, tension, Lx):
    return .5 * n**3 * electro_optic_coef * tension / Lx

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

class SecondBeamPhotorefractiveCrystalParameters(PhotorefractiveCrystalParameters):
    """A class representing a photorefractive crystal parameteres for two incident beams."""
    def __init__(
        self,
        crystal_config,
        ):
        """Initialize the photorefractive crystal when using two light beams.

        Args:
            crystal_config (dict): Dictionary with all the physical parameters required to initiate the object.
        """
        super().__init__(crystal_config)
        
        self.n1 = crystal_config["n1"]
        self.electro_optic_coef1 = crystal_config["electro_optic_coef1"]
        self.alpha1 = crystal_config["alpha1"]
        
        # Computes and initializes the delta_n_max for the second beam.
        self.delta_n_max1 = delta_n_max(.5 * self.n1**3 * self.electro_optic_coef1 * self.tension / self.Lx)