from numpy import ndarray, array, arange, pi, linspace
from numpy.fft import fftshift, fftfreq

class Box1D:
    """ Class to store the simulation box configuration."""
    def __init__(
        self,
        simulation_config,
        *args,
        **kwargs,
        ):
        """ Initialize the box variables."""
        self.Nx = simulation_config["Nx"]
        self.Nz = simulation_config["Nz"]
        self.lx = simulation_config["lx"]
        self.lz = simulation_config["lz"]
        
        self.field_shape = (self.Nx,)

        if "noise" in simulation_config.keys():
            self.noise = simulation_config["noise"]

        self.init_metadata()
                
        super().__init__(
            *args,
            **kwargs,
            )
        
    def init_metadata(self):
        """ Initialize metadata for the box."""
        if not hasattr(self, "x_min"):
            x_min = -self.lx/2.
        if not hasattr(self, "x_max"):
            x_max = self.lx/2.
        if not hasattr(self, "extent"):
            self.extent = array([x_min, x_max])
            
class Mesh1D(Box1D):
    """ Class to create a 1D mesh for the position representation of functions."""
    def init_mesh(self,):
        """ Initialize the mesh grid and steps."""
        self.init_grid()
        self.init_steps()
        
    def init_steps(self,):
        """ Initialize the steps in the mesh."""
        self.dx = self.x[1] - self.x[0]
        self.dz = self.z[1] - self.z[0]
        
    def grid(self,):
        """ Initialize the mesh grid for the 1D box."""
        self.x = arange(-int(self.Nx/2), int(self.Nx/2)) * self.lx/self.Nx
        self.z = linspace(0, self.lz, self.Nz + 1)
        
    def adim_grid(self,):
        """ Initialize the adimensionalized mesh grid for the 1D box."""
        self.x = arange(-int(self.Nx/2), int(self.Nx/2)) * self.adimensionalize_length(self.lx)/self.Nx

        self.z = linspace(0, self.adimensionalize_time(self.lz), self.Nz + 1)
        
    def init_grid(self,):
        """ Initialize the mesh grid based on adimensionalization settings."""
        if hasattr(self, "adimensionalize_length") and hasattr(self, "adimensionalize_time"):
            self.adim_grid()
        else:
            self.grid()
            
    def init_k_grid(self,):
        """ Initialize the momentum space grid."""
        self.kx = 2 * pi * fftfreq(self.Nx, self.dx)
        
        self.dkx = self.kx[1] - self.kx[0]
        
        self.kz = 2 * pi * fftfreq(self.Nz, self.dz)
        
        self.dkz = self.kz[1] - self.kz[0]