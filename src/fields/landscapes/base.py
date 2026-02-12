class Uniform:
    def __init__(
        self,
        landscape_config,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
    
    def landscape_function(self,):
        return 1.
    
    def adimensionalize_landscape(self,):
        pass