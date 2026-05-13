from .store_config.store import store_config_from_module


class AnalogousTime2DSimulationBox:
    def __init__(
        self,
        beams: dict,
        media: object,
        model: object,
        mesh: object,
        solver: object,
        storage: object,
    ):
        self.mesh = mesh
        self.beams = beams
        self.media = media
        self.model = model
        self.solver = solver
        self.storage = storage
    
    def init(self, config_module, *args, **kwargs):
        self.store_config(config_module)
        
        self.mesh.init()
        self.model.init(self, *args, **kwargs)
        self.init_beams()
        self.solver.init(self)
    
    def init_beams(self,):
        for beam in self.beams.values():
            beam.init(self)
    
    def solve(self,):
        self.storage.store_step(
                box = self,
                index = 0,
            )
        self.solver.solve(self)
        
    def store_config(self, config_module):
        store_config_from_module(self.storage.config, config_module)