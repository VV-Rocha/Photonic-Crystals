class MoireLatticeConfig:
    """ 2D Lattice landscape configuration class."""
    def __init__(
        self,
        landscape_config: dict,
        *args,
        **kwargs,
    ):
        """Initialize lattice parameters from configuration dictionary.

        Args:
            landscape_config (dict): Configuration dictionary containing lattice parameters. keys:
                - "angle": Angle of the first lattice.
                - "angle1": Angle of the second lattice.
                - "a": Lattice constant of the first lattice.
                - "a1": Lattice constant of the second lattice.
                - "p": Weight of the first lattice.
        """
        self.angle = (landscape_config["angle"], landscape_config["angle1"])
        self.a = (landscape_config["a"], landscape_config["a1"])
        self.p = (landscape_config["p"], landscape_config["p1"])
        
        super().__init__(*args, **kwargs)