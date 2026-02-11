class UnpackModulationConfig:
    def __init__(
        self,
        modulation_config: dict,
        *args,
        **kwargs,
    ):
        super().__init__(
            landscape_config = modulation_config["landscape_config"],
            envelope_config = modulation_config["envelope_config"],
            *args,
            **kwargs,
        )

class CoupledUnpackModulationConfig(UnpackModulationConfig):
    def __init__(
        self,
        modulation_config: dict,
        *args,
        **kwargs,
    ):
        super().__init__(
            landscape1_config = modulation_config["landscape1_config"],
            envelope1_config = modulation_config["envelope1_config"],
            modulation_config = modulation_config,
            *args,
            **kwargs,
            )