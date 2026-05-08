from .store_config.store import _store_config


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
    
    def init(self, *args, **kwargs):
        self.store_config()
        
        self.mesh.init()
        self.model.init(self, *args, **kwargs)
        self.init_beams()
        self.solver.init(self)
    
    def init_beams(self,):
        for beam in self.beams.values():
            beam.init(self)
    
    def solve(self,):
        self.solver.solve(self)
        
    def store_config(self,):
        _store_config(self.storage.config, vars(self))