from .lattices.base import LatticeConfig

from .lattices.single_lattices.two_dimensional import planewave_lattice
from .lattices.moire_lattices.double_lattices import lattice_sum

from .dark_soliton.base import DarkSolitonConfig

class MoireLattice(LatticeConfig):
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