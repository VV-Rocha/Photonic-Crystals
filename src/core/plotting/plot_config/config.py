class PlottingConfig:
    def __init__(
        self,
        plot_config,
        *args,
        **kwargs,
    ):
        self.units = plot_config["units"]
        self.units_factor = plot_config["units_factor"]
                
        super().__init__(*args, **kwargs)