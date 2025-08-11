from dataclasses import dataclass
from typing import Optional

@dataclass
class DataClass:
    structure_config: dict
    modulation_config: dict
    medium_config: dict
    beam_config: dict
    simulation_config: dict
    storage_config: Optional[dict] = None
    precision_config: Optional[dict] = None

class SimulationBox(DataClass):
    def __init__(
        self,
        structure_config,
        modulation_config,
        medium_config,
        beam_config,
        simulation_config,
        storage_config=None,
        precision_config=None,
        *args,
        **kwargs,
    ):
        # call parent dataclass __init__
        super().__init__(
            structure_config,
            modulation_config,
            medium_config,
            beam_config,
            simulation_config,
            storage_config,
            precision_config,
            *args,
            **kwargs,
        )
        
        self.initialize_parameters()
        
    def initialize(self,):
        if self.storage_config is not None:
            self.storage = self.storage_config["object"](storage_config=self.storage_config,)
            
        self.precision = self.precision_config["object"](precision_config=self.precision_config,)
            
        self.medium_parameters = self.medium_config["object"](medium_config=self.medium_config)
        
        self.beam_parameters = self.beam_config["object"](beam_config=self.beam_config)
            
        self.modulation_properties = self.modulation_config["object"](
            modulation_config = self.modulation_config
            )
        
        ### Define strategies  # % TODO: Strategies are fluxes of information without defining parameters so they should later be defined as inherited classes
        self.adim_method = self.simulation_config["adim_method"](
            self.beam_parameters,
            self.medium_parameters,
            self.precision,
            )
        self.solver = self.simulation_config["solver"](
            mesh=self.mesh,
            coefs=self.coefs,
            solver_method=self.simulation_config["solver_engine"],
            precision_control=self.precision,
            device = self.simulation_config["device"],
            gpu_backend = self.simulation_config["backend"],
            )

        
        ### Define parameters
        self.mesh = self.simulation_config["mesh_method"](
            self.simulation_config,
            self.adim_method,
            )

        self.input_fields = self.simulation_config["fields"](
            modulation_config=self.modulation_properties,
            precision_control=self.precision,
            store_config=self.storage,
            )
        self.input_fields.gen_fields(
            self.mesh,
            self.simulation_config["noise"],
            )
        
        self.model = self.simulation_config["model"](
            self.medium_parameters,
            self.beam_parameters,
            )
                
    def solve(self,):
        self.solver.solver(
            self.input_fields,
            store_config=self.storage,
            )