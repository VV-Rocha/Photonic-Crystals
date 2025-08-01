from functools import wraps

from .lattice import LatticeConfig, GaussianBeamConfig

from ..landscapes.lattices.moire_lattices import double_lattice

def try_init(init_func):
    @wraps(init_func)
    def wrapper(self, *args, **kwargs):
        try:
            return init_func(self, *args, **kwargs)
        except ((KeyError, AttributeError)) as e:
            self.landscape = lambda mesh: 1.
            print(f"Warning: config incomplete ({e}), disabling its lattice.")
    return wrapper

class MoireLattice(LatticeConfig):
    @try_init
    def __init__(self,
                 structure_config,
                 *args,
                 **kwargs):
        super().__init__(structure_config=structure_config,
                         *args,
                         *kwargs)

        self.lattice1_parameter = structure_config["a1"]
        self.p1 = structure_config["p1"]
        self.rotation1 = structure_config["angle1"]
        
        if (structure_config["lattice_method"] is None) and (structure_config["lattice1_method"] is None):
            self.landscape = lambda mesh: 1.
        else:
            self.landscape = lambda mesh: double_lattice(
                mesh,
                self.get_lattice_parameters(),
                self.get_ps(),
                self.get_angles(),
                (structure_config["lattice_method"], structure_config["lattice1_method"]),
                )
            
    def get_lattice_parameters(self,):
        return (self.lattice_parameter, self.lattice1_parameter)
    
    def get_ps(self,):
        return (self.p, self.p1)
    
    def get_angles(self,):
        return (self.rotation, self.rotation1)
    
class MoireLatticeGaussianBeamConfig(GaussianBeamConfig, MoireLattice):
    def __init__(
        self,
        structure_config,
        modulation_config,
        ):
        super().__init__(
            structure_config = structure_config,
            modulation_config = modulation_config,
            )

class MoireLatticeGaussianCoupledBeamConfig(MoireLatticeGaussianBeamConfig):
    def __init__(
        self,
        modulation_config,
        ):
        super().__init__(
            structure_config = modulation_config["structure"],
            modulation_config = modulation_config["modulation"],
            )
        
        self.beam1 = MoireLatticeGaussianBeamConfig(
            structure_config = modulation_config["structure1"],
            modulation_config = modulation_config["modulation1"],
        )