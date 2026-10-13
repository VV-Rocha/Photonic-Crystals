import numpy as np

from ..iterators.solver import AfTimeSpaceAnalogIterator
from .step_methods.step_methods import StepMethods
from .solver_init import SolverInit


class SplitStepSolver(
    SolverInit,
    StepMethods,
    AfTimeSpaceAnalogIterator,
):
    pass

        
class MetadataSplitStepSolver(
    SplitStepSolver,
):
    def init(
        self,
        box,
    ):
        super().init(box=box)
        if hasattr(self, "metadata"):
            self.init_metadata_storage()
    
    def init_metadata_storage(
        self,
    ):
        self.metadata_history = {}
        for beam in self.metadata.keys():
            self.metadata_history[beam] = {}
            for metadata in self.metadata[beam].keys():
                self.metadata_history[beam][metadata] = np.empty(self.Nsteps+1)
                
    def compute_metadata(
        self,
        i,
        box,
    ):
        for beam in self.metadata.keys():
            for metadata in self.metadata[beam].keys():
                self.metadata_history[beam][metadata][i] = self.metadata[beam][metadata](
                    beam = beam,
                    box = box,
                )