from .store_config.store import store_config
from .detection.noise import Detection


class AnalogousTime2DSimulationBox(Detection):
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
        self._store_config(config_module)
        
        self.mesh.init()
        self.model.init(self, *args, **kwargs)
        self.init_beams(
            encoding_noise = self.solver.encoding_noise,
        )
        self.solver.init(self)
    
    def init_beams(
        self,
        encoding_noise=0.,
    ):
        for beam in self.beams.values():
            beam.init(
                self,
                encoding_noise = encoding_noise,
            )
            self.random_phase(
                beam = beam,
            )
        
    def random_phase(
        self,
        beam,
    ):
        if hasattr(beam, "random_phase"):
            if beam.random_phase:
                if ((not beam.fixed_phase_mask) or (not hasattr(beam, "random_phase_mask"))):
                    print("Generating Speckle")
                    beam.gen_random_phase_mask(self, beam.speckle_size)
                beam.add_random_phase()

    def solve(self,):
        self.storage.store_step(
                box = self,
                index = 0,
            )
        self.solver.solve(self)
        
    def _store_config(self, config_module):
        store_config(self.storage.config, config_module)