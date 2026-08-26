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
        
        if ("encoding_noise" in solver_config.keys()):
            self.encoding_noise = solver_config["encoding_noise"]
        else:
            self.encoding_noise = 0.
            
        if ("detection_noise" in solver_config.keys()):
            self.detection_noise = solver_config["detection_noise"]
        else:
            self.detection_noise = 0.
        
        super().__init__(*args, **kwargs,)
    
    def init(self, box):
        set_device(self.device)
        
        self.mesh = SolverMeshGrid(box)
        self.mesh.init()