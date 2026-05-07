from .lattice_config import MoireLatticeConfig

from .single_lattices.two_dimensional import planewave_lattice
from .double_lattices.double_lattices import lattice_sum


class MoireLatticeLandscape(MoireLatticeConfig):
    def landscape_function(self, mesh):
        """ Generate the moire lattice landscape function."""
        return self._double_lattice(mesh)
    
    def _double_lattice(self, mesh):
        """ Generate the moire lattice by summing two rotated lattices."""
        xx_rot0, yy_rot0 = mesh.rotate_mesh(self.angle[0])
        xx_rot1, yy_rot1 = mesh.rotate_mesh(self.angle[1])
        return lattice_sum(xx_rot0, yy_rot0, xx_rot1, yy_rot1, self.a, self.p, planewave_lattice)