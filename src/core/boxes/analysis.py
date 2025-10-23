from ..dimensionless.facade import DimensionlessMethods

default_inheritances = (
    DimensionlessMethods,
    )

class AnalysisBoxMethods(*default_inheritances):
    def init(self,):        
        self.init_model()

        self.init_workbench()