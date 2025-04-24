import scipy.sparse as sps

import numpy as np

from scipy.sparse.linalg import eigsh

class SE_SpatialDecomposition:
    def __init__(self,
                 mesh,
                 coefs,
                 precision_control,
                 ):
        self.mesh = mesh
        self.coefs = coefs
        
        self.np_float = precision_control.np_float
        
        # init laplacian matrix
        self.gen_laplacian()
        
    def gen_laplacian(self,):
        I = sps.eye(self.mesh.Nx)
        
        D = sps.csr_matrix((-2 * sps.eye(self.mesh.Nx) + sps.eye(self.mesh.Nx, k=1) + sps.eye(self.mesh.Nx, k=-1)))
        
        self.K = (self.coefs.kinetic*(sps.kron(D, I)/self.mesh.dx**2 + sps.kron(I,D)/self.mesh.dy**2)).astype(self.np_float)
        
    def gen_potential(self, fields):
        self.V = -self.coefs.potential_function(fields)  ## the minus sign makes it so if c=-1 the potential field is attractive.
        
        self.V = (sps.diags(self.V.flatten() - np.abs(self.V.flatten()).max())).astype(self.np_float)
        
    def get_eig(self,
                n_eigenvectors: int | None = 50,
                return_eigenvectors: bool = False,
                ):
        return eigsh(self.K + self.V,
                     k = n_eigenvectors,
                     return_eigenvectors = return_eigenvectors,
                     sigma=None,
                     which="LA",
                     tol=1e-8,
                     maxiter=5000,
                     v0=None,
                     ncv=None,
                     )