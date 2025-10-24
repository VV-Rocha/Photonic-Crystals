from ......mesh.z_1d import Mesh1D

class SplitStepMesh(Mesh1D):
    """ Methods to convert between numpy and arrayfire array types. """
    def __init__(
        self,
        *args,
        **kwargs,
        ):
        super().__init__(
            *args,
            **kwargs,
        )

    def init_af(self,):
        """ Initialize arrayfire arrays for field and k-grid."""
        self.field = self.np_to_af(self.field)
        
        self.init_k_grid()
        self.kx = self.np_to_af(self.kx)
        
    def end_af(self,):
        """ Convert arrayfire arrays back to numpy arrays."""
        self.field = self.af_to_np(self.field)
        
        self.kx = self.af_to_np(self.kx)