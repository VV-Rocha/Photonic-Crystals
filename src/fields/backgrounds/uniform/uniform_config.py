class UniformConfig:
    def __init__(
        self,
        envelope_config,
        *args,
        **kwargs
    ):
        self.I = envelope_config["I"]
        super().__init__(*args, **kwargs)
    
    def adimensionalize_envelope(self, *args, **kwargs,):
        pass