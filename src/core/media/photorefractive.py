import h5py

# % TODO: Add a function to store variables for the PhotorefractiveCrystal class.

# % TODO: Change the classes to use the @dataclass method to ease readability and @classmethod to initiate delta_n_max.

class PhotorefractiveCrystal:
    """A class representing a photorefractive crystal parameters with a single incident beam."""
    def __init__(
        self,
        medium_config,
        ):
        """Initialize the photorefractive crystal when a single beam is being used.

        Args:
            medium_config (dict): Dictionary with all the physical parameters required to initiate the object.
        """
        self.n = medium_config["n"]
        self.electro_optic_coef = medium_config["electro_optic_coef"]
        self.tension = medium_config["tension"]
        self.Isat = medium_config["Isat"]
        self.alpha = medium_config["alpha"]
        
        self.Lx = medium_config["Lx"]
        self.Ly = medium_config["Ly"]
        self.Lz = medium_config["Lz"]
        
        # Computes and initializes the delta_n_max variable.
        self.delta_n_max = .5 * self.n**3 * self.electro_optic_coef * self.tension / self.Lx

class TwoBeamPhotorefractiveCrystal(PhotorefractiveCrystal):
    """A class representing a photorefractive crystal parameteres for two incident beams."""
    def __init__(
        self,
        medium_config,
        ):
        """Initialize the photorefractive crystal when using two light beams.

        Args:
            medium_config (dict): Dictionary with all the physical parameters required to initiate the object.
        """
        super().__init__(medium_config)
        
        self.n1 = medium_config["n1"]
        self.electro_optic_coef1 = medium_config["electro_optic_coef1"]
        self.alpha1 = medium_config["alpha1"]
        
        # Computes and initializes the delta_n_max for the second beam.
        self.delta_n_max1 = .5 * self.n1**3 * self.electro_optic_coef1 * self.tension / self.Lx