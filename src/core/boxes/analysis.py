from ..dimensionless.facade import DimensionlessMethods

default_inheritances = (
    DimensionlessMethods,
    )

class AnalysisBoxMethods(*default_inheritances):
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs,)
        self.init()
    
    def init(self,):        
        self.init_model()

        self.init_workbench()