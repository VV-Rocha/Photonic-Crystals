import copy

from .....mesh.z_2d import Mesh2D
from .....dimensionless.adimensionalization import adimensionalize_length
from .....dimensionless.adimensionalization import adimensionalize_time


def make_simulation_config(box):
    simulation_config = {
        "Nx": box.mesh.Nx,
        "Ny": box.mesh.Ny,
        "Nz": box.mesh.Nz,
        "lx": adimensionalize_length(box.mesh.lx, box.model),
        "ly": adimensionalize_length(box.mesh.ly, box.model),
        "lz": adimensionalize_time(box.mesh.lz, box.model),
        "noise": 0.,
    }
    return simulation_config

class SolverMeshGrid(Mesh2D):
    def __init__(self, box):
        if not box.model.adimensional_flag:
            self.mesh = copy.deepcopy(box.mesh)
        elif box.model.adimensional_flag:
            super().__init__(
                simulation_config = make_simulation_config(box),
            )