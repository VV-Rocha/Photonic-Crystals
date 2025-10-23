from ......mesh.z_2d import Mesh2D

class SplitStepMesh(Mesh2D):
    def init_af(self,):
        self.field = self.np_to_af(self.field)
        self.field1 = self.np_to_af(self.field1)
        
        self.init_k_grid()
        self.kxx = self.np_to_af(self.kxx)
        self.kyy = self.np_to_af(self.kyy)
        
    def end_af(self,):
        self.field = self.af_to_np(self.field)
        self.field1 = self.af_to_np(self.field1)
        
        self.kxx = self.af_to_np(self.kxx)
        self.kyy = self.af_to_np(self.kyy)