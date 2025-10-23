from ..dimensionless.facade import DimensionlessMethods

default_inheritances = (
    DimensionlessMethods,
    )

class SimulationBoxMethods(*default_inheritances):
    def init(self,):
        self.init_model()
        self.init_solver()        

        self.adimensionalize_field()

        self.modulate_field()
        self.add_noise()
        self.store_field(index="0")  # store initial state
        if hasattr(self, "plot_flag"):
            if self.plot_flag:
                self.init_plot()