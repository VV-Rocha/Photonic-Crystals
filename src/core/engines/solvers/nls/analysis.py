from ....storage.directories import StorageConfig

class AnalysisBoxStepSolver(StorageConfig):
    def __init__(
        self,
        device_config,
        modulation_config,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)