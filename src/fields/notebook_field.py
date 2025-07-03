from .field import ModulatedField2D
from .field import CoupledModulatedFields2D

from .field_plotting import CoupledPlotting
from .field_plotting import FieldPlotting

class NotebookCoupledFields(CoupledPlotting, CoupledModulatedFields2D):
    """Joins the AfCoupled2D and CoupledPlotting classes to explore simuation in a notebook."""
    def __init__(self,
                 simulation_config,
                 modulation_config,
                 store_config=None,
                 precision_control=None,
                 ):
        super().__init__(simulation_config = simulation_config,
                         modulation_config = modulation_config,
                         store_config = store_config,
                         precision_control = precision_control,
                         )
        
class NotebookField(FieldPlotting, ModulatedField2D):
    def __init__(self,
                 simulation_config,
                 modulation_config,
                 store_config=None,
                 precision_control=None,
                 ):
        super().__init__(simulation_config = simulation_config,
                         modulation_config = modulation_config,
                         store_config = store_config,
                         precision_control = precision_control,
                         )