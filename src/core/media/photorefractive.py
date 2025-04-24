import h5py

# % TODO: Add a function to store variables for the PhotorefractiveCrystal class.

# % TODO: Change the classes to use the @dataclass method to ease readability and @classmethod to initiate delta_n_max.

class PhotorefractiveCrystal:
    """A class representing a photorefractive crystal parameters with a single incident beam."""
    def __init__(self,
                 n: float,
                 electro_optic_coef: float,
                 tension: float,
                 Isat: float,
                 alpha: float,
                 Lx: float,
                 Ly: float,
                 Lz: float,
                 store_config = None,
                 ):
        """Initialize the photorefractive crystal when a single beam is being used.

        Args:
            n (float): Extraordinary refractive index.
            electro_optic_coef (float): Electro-optic coefficient of the photorefractive crystal.
            tension (float): Voltage applied accross the horizontal direction of the crystal
            Isat (float): Saturation intensity.
            alpha (float): Absorption coefficient.
            Lx (float): Horizontal length of the crystal.
            Ly (float): Vertical length of the crystal.
            Lz (float): Longitudinal length of the crystal.
        """
        self.n = n
        self.electro_optic_coef = electro_optic_coef
        self.tension = tension
        self.Isat = Isat
        self.alpha = alpha
        
        self.Lx = Lx
        self.Ly = Ly
        self.Lz = Lz
        
        # Computes and initializes the delta_n_max variable.
        self.delta_n_max = .5 * self.n**3 * self.electro_optic_coef * self.tension / self.Lx

class TwoBeamPhotorefractiveCrystal(PhotorefractiveCrystal):
    """A class representing a photorefractive crystal parameteres for two incident beams."""
    def __init__(self,
                 n: float,
                 n1: float,
                 electro_optic_coef: float,
                 electro_optic_coef1: float,
                 tension: float,
                 Isat: float,
                 alpha: float,
                 alpha1: float,
                 Lx: float,
                 Ly: float,
                 Lz: float,
                 store_config=None,
                 ):
        """Initialize the photorefractive crystal when using two light beams.

        Args:
            n (float): Extraordinary refractive index (first beam).
            n1 (float): Extraordinary refractive index (second beam).
            electro_optic_coef (float): Electro-optic coefficient of the photorefractive crystal (first beam).
            electro_optic_coef1 (float): Electro-optic coefficient of the photorefractive crystal (second beam).
            tension (float): Voltage applied accross the horizontal direction of the crystal.
            Isat (float): Saturation intensity.
            alpha (float): Absorption coefficient (first beam).
            alpha1 (float): Absorption coefficient (second beam).
            Lx (float): Horizontal length of the crystal.
            Ly (float): Vertical length of the crystal.
            Lz (float): Longitudinal length of the crystal.
            store_config (StoreConfig object, optional): StoreConfig object defined in core.control. Defaults to None.
        """
        super().__init__(n = n,
                         electro_optic_coef = electro_optic_coef,
                         tension = tension,
                         Isat = Isat,
                         alpha = alpha,
                         Lx = Lx,
                         Ly = Ly,
                         Lz = Lz,
                         )
        
        self.n1 = n1
        self.electro_optic_coef1 = electro_optic_coef1
        self.alpha1 = alpha1
        
        # Computes and initializes the delta_n_max for the second beam.
        self.delta_n_max1 = .5 * self.n1**3 * self.electro_optic_coef1 * self.tension / self.Lx
        
        if store_config is not None:
            self.store_parameters(store_config)        
        
    def store_parameters(self, store_config):
        """Stores the crystal parameters for both beams.

        Args:
            store_config (StoreConfig object): StoreConfig object defined in core.control.
        """
        filename = store_config.get_medium_dir()
        with h5py.File(filename, "w") as f:
            f.create_dataset("n", data = self.n)
            f.create_dataset("electro_optic_coef", data = self.electro_optic_coef)
            f.create_dataset("tension", data = self.tension)
            f.create_dataset("Isat", data=self.Isat)
            f.create_dataset("alpha", data=self.alpha)
            f.create_dataset("Lx", data = self.Lx)
            f.create_dataset("Ly", data = self.Ly)
            f.create_dataset("Lz", data = self.Lz)
        
            f.create_dataset("n1", data = self.n1)
            f.create_dataset("electro_optic_coef1", data = self.electro_optic_coef1)
            f.create_dataset("alpha1", data=self.alpha1)
            
            f.create_dataset("delta_n_max", data=self.delta_n_max)
            f.create_dataset("delta_n_max1", data=self.delta_n_max1)
        f.close()