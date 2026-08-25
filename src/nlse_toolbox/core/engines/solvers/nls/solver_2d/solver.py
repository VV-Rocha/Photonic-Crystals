from .....arrayfire_utils.device import set_device

from ..iterators.solver import AfTimeSpaceAnalogIterator
from .step_methods import StepMethods
from .solver_grid import SolverMeshGrid


class SplitStepSolver(
    StepMethods,
    AfTimeSpaceAnalogIterator,
):
    def __init__(
        self,
        solver_config,
        *args,
        **kwargs,
    ):
        if ("device" in solver_config.keys()):
            self.device = solver_config["device"]
        if ("backend" in solver_config.keys()):
            self.backend = solver_config["backend"]
        
        super().__init__(*args, **kwargs,)
    
    def init(self, box):
        set_device(self.device)
        
        self.mesh = SolverMeshGrid(box)
        self.mesh.init()