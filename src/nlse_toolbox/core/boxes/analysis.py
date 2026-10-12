from .load_config.load_config import _load_stored_config


class AnalysisBox:
    def __init__(
        self,
        mesh,
        beams,
        media,
        model,
        storage,
        *args,
        **kwargs,
    ):
        self.mesh = mesh
        self.beams = beams
        self.media = media
        self.model = model
        self.storage = storage
        
        self.load_config(self.storage.home)
        
    def init_beams(self,):
        self.beams = self._init_beams(
                    self.beams,
                    self.configs["beams_config"],
                )
        
    def load_config(self, directory):
        """
        Loads the configurations in the given directory.

        Args:
            directory (str): directory to the configuration folder

        Returns:
            dict: Returns the dictionary with the configurations required to initialize the objects. 
        """
        self.configs = _load_stored_config(directory)
    
    def load_simulation(self,):
        self.storage._load_simulation(self)
        
    def init(self, data_directory=None):
        if data_directory is not None:
            self.load_config(data_directory)

        if self.configs is None:
            raise RuntimeError(
                "No config loaded. Call load_config(data_directory) first, "
                "or call init(data_directory)."
            )

        self.mesh = self.mesh(self.configs["simulation_config"])
        self.init_beams()
        self.media = self.media(self.configs["crystal_config"])
        self.model = self.model()

    def _init_beams(self, beam_templates, beams_config):
        initialized_beams = {}

        for beam_name, beam_cls in beam_templates.items():
            
            beam_config = beams_config[beam_name]
            
            initialized_beams[beam_name] = beam_cls(**beam_config)
            
            initialized_beams[beam_name].init(
                self,
                encoding_noise = 0.,
            )

        return initialized_beams