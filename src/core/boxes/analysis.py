from .load_config.load_config import _load_stored_config


class AnalysisBox:
    def __init__(
        self,
        mesh: object,
        beams: dict,
        media: object,
        model: object,
        storage: object,
        *args,
        **kwargs,
    ):
        self.mesh = mesh
        self.beams = beams
        self.media = media
        self.model = model
        self.storage = storage
        
        super().__init__(*args, **kwargs,)
    
    def init(self, data_directory=None):
        """
        Initialize objects from loaded configs.

        Usage:
            analysis_box.load_config(data_folder)
            analysis_box.init()

        or:
            analysis_box.init(data_folder)
        """
        if data_directory is not None:
            self.load_config(data_directory)

        if self.configs is None:
            raise RuntimeError(
                "No configs loaded. Call load_config(data_directory) before init(), "
                "or call init(data_directory)."
            )

        self._init_objects_from_configs(self.configs)
        
    def init_beams(self,):
        for beam in self.beams.values():
            beam.init(self)
        
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

        self.mesh = self.mesh(self.configs.simulation_config)
        self.beams = self._init_beams(self.beams, self.configs.beams_config)
        self.media = self.media(self.configs.media_config)
        self.model = self.model(self.configs.model_config)
        self.storage = self.storage(self.configs.storage_config)

    def _init_beams(self, beam_templates, beams_config):
        initialized_beams = {}

        for beam_name, beam_cls in beam_templates.items():
            
            beam_config = beams_config[beam_name]
            
            initialized_beams[beam_name] = beam_cls(**beam_config)

        return initialized_beams