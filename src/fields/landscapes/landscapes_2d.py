from .lattices.single_lattices.two_dimensional import planewave_lattice
from .lattices.moire_lattices.double_lattices import lattice_sum

class LatticeConfig:
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

    def adimensionalize_landscape(self,):
        """ Adimensionalize lattice parameters."""
        self.a = (self.adimensionalize_length(self.a[0]), self.adimensionalize_length(self.a[1]))


class MoireLattice(LatticeConfig):
    def __init__(
        self,
        landscape_config: dict | None = None,
        *args,
        **kwargs,
        ):
        """ Initialize moire lattice landscape.

        Args:
            landscape_config (None, optional): Configuration dictionary for the moire lattice. Defaults to None.
        """
        super().__init__(
            *args,
            **kwargs,
        )

    def landscape_function(self,):
        """ Generate the constant moire lattice landscape function."""
        return 1.
    
    def landscape_function1(self,):
        """ Generate the moire lattice landscape function."""
        return self.double_lattice()
        
    def double_lattice(self,):
        """ Generate the moire lattice by summing two rotated lattices."""
        xx_rot0, yy_rot0 = self.rotate_mesh(self.angle[0])
        xx_rot1, yy_rot1 = self.rotate_mesh(self.angle[1])
        return lattice_sum(xx_rot0, yy_rot0, xx_rot1, yy_rot1, self.a, self.p, planewave_lattice)