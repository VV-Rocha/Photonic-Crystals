from .....mesh.z_2d import Mesh2D

class SplitStepMesh(Mesh2D):
    def init_af(self,):
        self.field = self.np_to_af(self.field)

        self.init_k_grid()
        self.kxx = self.np_to_af(self.kxx)
        self.kyy = self.np_to_af(self.kyy)
        
    def end_af(self,):
        self.field = self.af_to_np(self.field)
        
        self.kxx = self.af_to_np(self.kxx)
        self.kyy = self.af_to_np(self.kyy)


class CoupledSplitStepMesh(SplitStepMesh):
    def init_af(self,):
        super().init_af()
        self.field1 = self.np_to_af(self.field1)
        
    def end_af(self,):
        super().end_af()
        self.field1 = self.af_to_np(self.field1)