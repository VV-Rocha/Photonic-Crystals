class UniformLandscape:
    def __init__(
        self,
        landscape_config,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
    
    def landscape_function(self, *args, **kwargs,):
        return 1.
    
    def adimensionalize_landscape(self, *args, **kwargs,):
        pass