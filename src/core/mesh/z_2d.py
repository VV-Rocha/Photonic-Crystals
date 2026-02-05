from typing import Tuple

from numpy import meshgrid, pi, cos, sin, ndarray, arange, array, linspace
from numpy.fft import fftfreq, fftshift

class Box2D:
    """Class to store the simulation box configuration."""
    def __init__(
        self,
        simulation_config,
        *args,
        **kwargs,
        ):
        """Initialize the box variables."""
        self.Nx = simulation_config["Nx"]
        self.Ny = simulation_config["Ny"]
        self.Nz = simulation_config["Nz"]
        self.lx = simulation_config["lx"]
        self.ly = simulation_config["ly"]
        self.lz = simulation_config["lz"]
        
        self.field_shape = (self.Nx, self.Ny)
        
        if "noise" in simulation_config.keys():
            self.noise = simulation_config["noise"]
        
        self.init_metadata()
        
        super().__init__(
            *args,
            **kwargs,
        )
        
    def init_metadata(self,):
        """ Initialize metadata for the box."""
        if not hasattr(self, "x_min"):
            x_min = -self.lx/2
        if not hasattr(self, "x_max"):
            x_max = self.lx/2
        if not hasattr(self, "y_min"):
            y_min = -self.ly/2
        if not hasattr(self, "y_max"):
            y_max = self.ly/2
        if not hasattr(self, "extent"):
            self.extent = array([x_min, x_max, y_min, y_max])

class Mesh2D(Box2D):
    """Class to create a 2D mesh for the position representation of functions."""
    def init_mesh(self,):
        self.init_grid()
        self.init_steps()
        
    def init_steps(self,):
        """Initialize the steps in the mesh."""
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
        self.dz = self.z[1] - self.z[0]
        
    def grid(self,):
        """Initialize the mesh grid for the 2D box."""
        self.x = arange(-int(self.Nx/2), int(self.Nx/2)) * self.lx/self.Nx
        self.y = arange(-int(self.Ny/2), int(self.Ny/2)) * self.ly/self.Ny
        
        self.z = linspace(0, self.lz, self.Nz + 1)
        self.xx, self.yy = meshgrid(self.x, self.y)
        
    def adim_grid(self,):
        self.x = arange(-int(self.Nx/2), int(self.Nx/2)) * self.adimensionalize_length(self.lx)/self.Nx
        self.y = arange(-int(self.Ny/2), int(self.Ny/2)) * self.adimensionalize_length(self.ly)/self.Ny
        
        self.z = linspace(0, self.adimensionalize_time(self.lz), self.Nz + 1)

        self.xx, self.yy = meshgrid(self.x, self.y)
        
    def init_grid(self,):
        if hasattr(self, "adimensionalize_length") and hasattr(self, "adimensionalize_time"):
            self.adim_grid()
        else:
            self.grid()
        
    def rotate_mesh(self, angle: float,) -> Tuple[ndarray, ndarray]:
        """Returns the mesh rotated by the given angle in radians.

        Args:
            angle (float): Rotation angle in radians.

        Returns:
            Tuple[ndarray, ndarray]: Rotated X and Y mesh grids.
        """
        return self.xx*cos(angle) - self.yy*sin(angle), self.xx*sin(angle) + self.yy*cos(angle)
        
    def init_k_grid(self,):
        """Initialize the k-space mesh."""
        self.kx = 2*pi*(fftfreq(self.Nx, self.dx))
        self.ky = 2*pi*(fftfreq(self.Ny, self.dy))
        
        self.dkx = self.kx[1] - self.kx[0]
        self.dky = self.ky[1] - self.ky[0]
        
        self.kz = 2*pi*(fftfreq(self.Nz, self.dz))
        
        self.kxx, self.kyy = meshgrid(self.kx, self.ky)