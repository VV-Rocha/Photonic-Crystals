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
    def __init__(self,
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
            
        self.precision = self.precision_config["object"](precision=self.precision_config["precision"],
                                       store_config=self.storage,
                                       )
            
        self.medium_parameters = self.medium_config["object"](n = self.medium_config["n"],
                                                                    n1 = self.medium_config["n"],
                                                                    electro_optic_coef = self.medium_config["electro_optic_coef"],
                                                                    electro_optic_coef1 = self.medium_config["electro_optic_coef1"],
                                                                    tension = self.medium_config["tension"],
                                                                    Isat = self.medium_config["Isat"],
                                                                    alpha = self.medium_config["alpha"],
                                                                    alpha1 = self.medium_config["alpha1"],
                                                                    Lx = self.medium_config["Lx"],
                                                                    Ly = self.medium_config["Ly"],
                                                                    Lz = self.medium_config["Lz"],
                                                                    store_config=self.storage,
                                                                    )
        self.beam_parameters = self.beam_config["object"](wavelengths = (self.beam_config["wavelength"], self.beam_config["wavelength1"]),
                                                              cs = (self.beam_config["sign"] * 1., self.beam_config["sign"] * .1),
                                                              store_config = self.storage,
                                                              )
        self.adim_method = self.simulation_config["adim_method"](self.beam_parameters,
                                                                     self.medium_parameters,
                                                                     self.precision,
                                                                     )
            
        self.modulation_properties = self.modulation_config["object"](lattice_parameter = None,
                                                                          lattice1_parameter = (self.structure_config["a"], self.structure_config["a"]),
                                                p = self.structure_config["p"],
                                                p1 = self.structure_config["p1"],
                                                rotation = None,
                                                rotation1 = (self.structure_config["eta"], self.structure_config["angle"] + self.structure_config["eta"]),
                                                width = self.modulation_config["waist"],
                                                width1 = self.modulation_config["waist1"],
                                                center = self.modulation_config["center"],
                                                I = self.modulation_config["I"],
                                                I1 = self.modulation_config["I1"],
                                                power = self.modulation_config["exponent"],
                                                power1 = self.modulation_config["exponent1"],
                                                store_config=self.storage,
                                                lattice_method=self.structure_config["lattice_method"],
                                                lattice1_method=self.structure_config["lattice1_method"],
                                                )
    
        self.coefs = self.simulation_config["coefs_object"](self.medium_parameters,
                                                            self.beam_parameters,
                                                            self.adim_method,
                                                            self.storage,
                                                            # invert_energy_scale=True,
                                                            )
        
        self.mesh = self.simulation_config["mesh_method"](self.simulation_config,
                                                          self.adim_method)
        
        self.solver = self.simulation_config["solver"](mesh=self.mesh,
                              coefs=self.coefs,
                              solver_method=self.simulation_config["solver_engine"],
                              precision_control=self.precision,
                              device = self.simulation_config["device"],
                              gpu_backend = self.simulation_config["backend"],
                              )
        
        self.input_fields = self.simulation_config["fields"](self.simulation_config,
                                                             modulation_config=self.modulation_properties,
                                                             precision_control=self.precision,
                                                             store_config=self.storage,
                                                             )
        self.input_fields.gen_fields(self.mesh, self.simulation_config["noise"])
                
    def solve(self,):
        self.solver.solver(self.input_fields, store_config=self.storage)