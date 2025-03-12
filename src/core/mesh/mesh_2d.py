from numpy import linspace, meshgrid

class Mesh2D:
    def __init__(self,
                 medium_properties,  # crystal dimensions in meters
                 N = (256,256,10), # number of points in each dimension
                 adim_method=None,
                 ):
        self.lx, self.ly, self.lz = medium_properties["lx"], medium_properties["ly"], medium_properties["lz"]
        self.Nx, self.Ny, self.Nz = N
        
        if adim_method is not None:
            self.lx = adim_method.adimensionalize_length(self.lx)
            self.ly = adim_method.adimensionalize_length(self.ly)
            self.lz = adim_method.adimensionalize_time(self.lz)
            
        self.init_mesh()
        
    def init_mesh(self,):
        self.x = linspace(-self.lx/2, self.lx/2, self.Nx)
        self.y = linspace(-self.ly/2, self.ly/2, self.Ny)
        self.z = linspace(0, self.lz, self.Nz)
                
        self.XX, self.YY = meshgrid(self.x, self.y)