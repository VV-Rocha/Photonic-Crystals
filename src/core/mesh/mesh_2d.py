from typing import Tuple

from numpy import linspace, meshgrid, pi, cos, sin, ndarray
from numpy.fft import fftfreq, fftshift

import arrayfire as af

class Box:
    """Class to store the simulation box configuration."""
    def __init__(self, simulation_config):
        """Initialize the box variables."""
        self.Nx = simulation_config["Nx"]
        self.Ny = simulation_config["Ny"]
        self.Nz = simulation_config["Nz"]
        self.lx = simulation_config["lx"]
        self.ly = simulation_config["ly"]
        self.lz = simulation_config["lz"]

class AdimensionalBox(Box):
    """Takes care of adimensionalization (if defined)."""
    def __init__(self, adim_method, **kwargs):
        """Initializes the adimensional box variables.

        Args:
            adim_method (Adimensionalization Object, optional): Uses an adimensionalization object defined in this repository to adimensionalize the simulation box. Defaults to None.

        Raises:
            print: If adim_method is None, it prints a message indicating that the adimensional method is not defined.
            AttributeError: If adim_method is defined but fails to adimensionalize the simulation box, it raises an AttributeError with a message indicating the failure.
        """
        super().__init__(**kwargs)
        
        self.adim_method = adim_method
        try:
            self.lx = adim_method.adimensionalize_length(self.lx)
            self.ly = adim_method.adimensionalize_length(self.ly)
            self.lz = adim_method.adimensionalize_time(self.lz)
            self.dim_flag = "dimensional"
        except AttributeError as e:
            self.dim_flag = "adimensional"
            if adim_method is None:
                print("Adimensional method not defined. Currently working with dimensional box.")
            else:
                raise AttributeError("Adimensional method is defined but failed to adimensionalize simulation box. Currently working with dimensional box.")

class Mesh2D(AdimensionalBox):
    """Class to create a 2D mesh for the position representation of functions."""
    def __init__(self,
                 simulation_config: dict,
                 adim_method = None,
                 ):
        """Initialize the mesh object.

        Args:
            simulation_config (dict): Dictionary containing the simulation configuration. The parameters required are:
                - Nx: Number of points in the x direction.
                - Ny: Number of points in the y direction.
                - Nz: Number of points in the z direction.
                - lx: Length of the box in the x direction.
                - ly: Length of the box in the y direction.
                - lz: Length of the box in the z direction.
            adim_method (Adimensionalization Object, optional): Uses an adimensionalization object defined in this repository to adimensionalize the simulation box. Defaults to None.
        """
        super().__init__(simulation_config = simulation_config,
                         adim_method = adim_method,
                         )
        
        self.init_mesh()
        self.init_steps()
        
    def init_steps(self,):
        """Initialize the steps in the mesh."""
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
        self.dz = self.z[1] - self.z[0]
        
    def init_mesh(self,):
        """Initialize the mesh grid for the 2D box."""
        self.x = linspace(-self.lx/2, self.lx/2, self.Nx)
        self.y = linspace(-self.ly/2, self.ly/2, self.Ny)
        self.z = linspace(0., self.lz, self.Nz)
                
        self.XX, self.YY = meshgrid(self.x, self.y)
        
    def rotate_mesh(self, angle: float,) -> Tuple[ndarray, ndarray]:
        """Returns the mesh rotated by the given angle in radians.

        Args:
            angle (float): Rotation angle in radians.

        Returns:
            Tuple[ndarray, ndarray]: Rotated X and Y mesh grids.
        """
        return self.XX*cos(angle) - self.YY*sin(angle), self.XX*sin(angle) + self.YY*cos(angle)
        
    def init_k_mesh(self,):
        """Initialize the k-space mesh."""
        self.kx = 2*pi*(fftfreq(self.Nx, self.dx))
        self.ky = 2*pi*(fftfreq(self.Ny, self.dy))
        
        self.kz = 2*pi*(fftfreq(self.Nz, self.dz))
        
        self.kXX, self.kYY = meshgrid(self.kx, self.ky)