from ..base import Uniform

class LatticeConfig(Uniform):
    """ 2D Lattice landscape configuration class."""
    def __init__(
        self,
        landscape1_config: dict,
        *args,
        **kwargs,
    ):
        """Initialize lattice parameters from configuration dictionary.

        Args:
            landscape1_config (dict): Configuration dictionary containing lattice parameters. keys:
                - "angle": Angle of the first lattice.
                - "angle1": Angle of the second lattice.
                - "a": Lattice constant of the first lattice.
                - "a1": Lattice constant of the second lattice.
                - "p": Weight of the first lattice.
        """
        self.angle = (landscape1_config["angle"], landscape1_config["angle1"])
        self.a = (landscape1_config["a"], landscape1_config["a1"])
        self.p = (landscape1_config["p"], landscape1_config["p1"])
        
        super().__init__(*args, **kwargs)

    def adimensionalize_landscape1(self,):
        """ Adimensionalize lattice parameters."""
        self.a = (self.adimensionalize_length(self.a[0]), self.adimensionalize_length(self.a[1]))