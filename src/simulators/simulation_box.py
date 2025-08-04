from dataclasses import dataclass

@dataclass
class DataClass:
    structure_config: dict
    modulation_config: dict
    medium_config: dict
    beam_config: dict
    simulation_config: dict
    storage_config: dict
    precision_config: dict
    
class SimulationBox(DataClass):
    def super_init(init_func):
        def wrapper(self, *args, **kwargs):
            super(type(self), self).__init__(*args, **kwargs)
            return init_func(self, *args, **kwargs)
        return wrapper
    @super_init
    def __init__(
        self,
        structure_config,
        modulation_config,
        medium_config,
        beam_config,
        simulation_config,
        storage_config = None,
        precision_config = None,
        ):
        
        self.initialize()
        
    def initialize(self,):
        # % TODO: Change the objects such that they deal with the config dictionaries internally
        if self.storage_config is not None:
            self.storage = self.storage_config["object"](storage_config=self.storage_config,)
            
        self.precision = self.precision_config["object"](precision_config=self.precision_config,)
            
        self.medium_parameters = self.medium_config["object"](medium_config=self.medium_config)
        
        self.beam_parameters = self.beam_config["object"](beam_config=self.beam_config)
            
        self.modulation_properties = self.modulation_config["object"](
            modulation_config = self.modulation_config
            )
        
        ### Define Simulation Box
        ## Dimensionalisation
        self.adim_method = self.simulation_config["adim_method"](
            self.beam_parameters,
            self.medium_parameters,
            self.precision,
            )
        ## Grid
        self.mesh = self.simulation_config["mesh_method"](
            self.simulation_config,
            self.adim_method,
            )
        ## Initial Conditions
        self.input_fields = self.simulation_config["fields"](
            modulation_config=self.modulation_properties,
            precision_control=self.precision,
            store_config=self.storage,
            )
        self.input_fields.gen_fields(
            self.mesh,
            self.simulation_config["noise"],
            )
        
        ### Define Solver
        ## Eq. coefficients
        self.coefs = self.simulation_config["coefs_object"](
            self.medium_parameters,
            self.beam_parameters,
            self.adim_method,
            self.storage,
            # invert_energy_scale=True,
            )
        ## engine
        self.solver = self.simulation_config["solver"](
            mesh=self.mesh,
            coefs=self.coefs,
            solver_method=self.simulation_config["solver_engine"],
            precision_control=self.precision,
            device = self.simulation_config["device"],
            gpu_backend = self.simulation_config["backend"],
            )
                
    def solve(self,):
        self.solver.solver(
            self.input_fields,
            store_config=self.storage,
            )