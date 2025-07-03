# % TODO: Add a function to initialize the objects by reading of a hdf5 file. As input this method should receive a StoreConfig and automatically read the necessary files.

from functools import wraps

from numpy import ndarray

from numpy import abs, angle, array, ones, copy, conjugate

from .noise import introduce_2d_noise

import h5py

def default_precision(func):
    @wraps(func)
    def wrapper(self, config, precision_control, *args, **kwargs):
        # % TODO: Later change the if condition to verify isinstance(precision, PrecisionControl)
        if precision_control is None:
            from numpy import complex128
            return func(self, config, complex128)
        return func(self, config, precision_control.np_complex)
    return wrapper

class StoreField:
    """Class to store and load fields in hdf5 format."""
    def __init__(self,
                 store_config=None,
                 **kwargs,
                 ):
        super().__init__(**kwargs)
        self.store_config = store_config

    def store_field(self, field: ndarray=None, filename: str = ""):
        """Store the field in hdf5 format. The field is stored in the dataset "field" and the extent in the dataset "extent".

        Args:
            filename (str): Directory of the file to store the field. Defaults to None.
            field (ndarray, optional): Stores field, if field is None stores self.field. Defaults to None.
        """
        with h5py.File(filename, "w") as f:
            f.create_dataset("field", data=field)
            f.create_dataset("extent", data=self.extent)
        f.close()
        
    def load_field(self, filename: str):
        """Load the field from hdf5 format.

        Args:
            filename (str): Directory of the file to load the field.
        """
        with h5py.File(filename, "r") as f:
            self.field = f["field"][:]
            self.extent = f["extent"][:]
        f.close()

class Field2D(StoreField,):
    """(Numpy) 2D field class."""
    def __init__(self,
                 simulation_config,
                 precision_control=None,
                 store_config=None,
                 ):
        """Initializes the field array and the metadata of the field. The field is stored in a numpy array. The metadata is stored in the extent attribute.
        The extent attribute is a numpy array with the following format: [x_min, x_max, y_min, y_max].

        Args:
            simulation_config (SimulationConfig): Simulation box configuration. The parameters required are:
                - Nx: Number of points in the x direction.
                - Ny: Number of points in the y direction.
                - lx: Length of the box in the x direction.
                - ly: Length of the box in the y direction.
            precision_control (PrecisionControl, optional): PrecisionControl object containing the numpy numerical precision dtypes used. Defaults to None.
            store_config (StorageConfig, optional): StorageConfig object containing the structure and directories of the storage folder. Defaults to None.
        """
        super().__init__(store_config = store_config,)
        
        self.init_field(simulation_config, precision_control)

        self.nfields = "single"

        self.npfloat = precision_control.np_float
        
    def get_intensity(self,):
        return ((self.field) * conjugate(self.field)).astype(self.npfloat)

    def get_total_intensity(self,):
        return self.get_intensity()

    def get_angle(self,):
        return angle(self.field)

    def init_mesh_metadata(func):
        """Decorator initializing the mesh metadata of the field. The metadata is stored in the extent attribute."""
        @wraps(func)
        def wrapper(self, config, *args, **kwargs):
            if not hasattr(self, "x_min"):
                x_min = -config["lx"]/2
            if not hasattr(self, "x_max"):
                x_max = config["lx"]/2
            if not hasattr(self, "y_min"):
                y_min = -config["ly"]/2
            if not hasattr(self, "y_max"):
                y_max = config["ly"]/2
            if not hasattr(self, "extent"):
                self.extent = array([x_min, x_max, y_min, y_max])
            return func(self, config, *args, **kwargs)
        return wrapper

    @default_precision
    @init_mesh_metadata
    def init_field(self, simulation_config, precision_control,):
        """Initialize the field array and the metadata of the field.

        Args:
            simulation_config (SimulationConfig): Simulation box configuration. The parameters required are:
                - Nx: Number of points in the x direction.
                - Ny: Number of points in the y direction.
                - lx: Length of the box in the x direction.
                - ly: Length of the box in the y direction.
            precision_control (PrecisionControl): PrecisionControl object containing the numpy numerical precision dtypes used.
        """
        shape = (simulation_config["Nx"], simulation_config["Ny"])
        self.field = ones(shape, precision_control)

    def check_field(func):
        """Decorator to check if the given field is None. If it is, the function uses the field attribute of the class. This is used to avoid having to pass the field as an argument every time.
        """
        @wraps(func)
        def wrapper(self, field=None, *args, **kwargs):
            if field is None:
                return func(self, self.field, *args, **kwargs)
            return func(self, field, *args, **kwargs)
        return wrapper

    def copy_input_field(self,):
        self.input_field = copy(self.field)

    @check_field
    def store_field(self, field=None, filename:str = ""):
        """Store the field in hdf5 format. The field is stored in the dataset "field" and the extent in the dataset "extent".

        Args:
            filename (str): Directory of the file to store the field.
            field (ndarray, optional): Field to be stored. Defaults to self.field.
        """
        super().store_field(field, filename)
        
        
class LandscapedField2D(Field2D):
    """2D field class with landscape. The field is stored in a numpy array. The metadata is stored in the extent attribute."""
    def __init__(self,
                 simulation_config,
                 modulation_config,
                 precision_control=None,
                 store_config=None,
                 ):
        super().__init__(simulation_config = simulation_config,
                         precision_control = precision_control,
                         store_config = store_config,
                         )

        self.modulation_config = modulation_config
        
    def gen_landscape(self, mesh):
        """Generates the field using the landscape and the modulation function. 

        Args:
            mesh (Mesh2D object): Mesh of the domain of the landscape function.
        """
        self.landscape = self.modulation_config.landscape(mesh)
    
    def gen_field(self,
                  mesh,
                  noise: bool | float = False,
                  ):
        self.gen_landscape(mesh)
        self.field = self.landscape
        if type(noise) is float:
            introduce_2d_noise(self.field, noise)
        
class ModulatedField2D(LandscapedField2D):
    def __init__(self,
                 simulation_config,
                 modulation_config,
                 precision_control=None,
                 store_config=None,
                 ):
        super().__init__(simulation_config = simulation_config,
                         modulation_config = modulation_config,
                         precision_control = precision_control,
                         store_config = store_config,
                         )
        
    def gen_envelope(self, mesh):
        self.envelope = self.modulation_config.modulation_function(mesh)
        
    def gen_field(self,
                  mesh,
                  noise: bool | float = False,
                  ):
        super().gen_field(mesh,
                          noise=False)
        
        self.gen_envelope(mesh)
        if type(self.landscape) is float:
            self.field *= self.envelope
        else:
            self.field[:, :] *= self.envelope
            
        if type(noise) is float:
            introduce_2d_noise(self.field, noise)
    
class CoupledModulatedFields2D(ModulatedField2D):
    def __init__(self,
                 simulation_config,
                 modulation_config,
                 precision_control=None,
                 store_config=None,
                 ):
        super().__init__(simulation_config = simulation_config,
                     modulation_config = modulation_config.beam,
                     precision_control = precision_control,
                     )
        self.store_config = store_config
    
        self._field1 = ModulatedField2D(simulation_config = simulation_config,
                                    modulation_config = modulation_config.beam1,
                                    precision_control = precision_control,
                                    )
    
        self.nfields = "coupled"
    
    def copy_input_fields(self,):
        self.copy_input_field()
        self._field1.copy_input_field()
    
    @wraps(ModulatedField2D.gen_field)
    def gen_field1(self,
                   mesh, 
                   noise):
        self._field1.gen_field(mesh,
                               noise)
    
    def gen_fields(self,
                   mesh,
                   noise: bool | float = False,
                   ):
        self.gen_field(mesh, noise)
        self.gen_field1(mesh, noise)
    
    @wraps(ModulatedField2D.gen_landscape)
    def gen_landscape1(self, mesh):
        self._field1.gen_landscape(mesh)
    
    @wraps(ModulatedField2D.gen_envelope)
    def gen_envelope1(self, mesh):
        self._field1.gen_envelope(mesh)
    
    def get_intensity1(self,):
        return self._field1.get_intensity()
    
    def get_angle1(self,):
        return self._field1.get_angle()
    
    def get_total_intensity(self,):
        return self.get_intensity() + self.get_intensity1()
    
    def default_fields(func):
        @wraps(func)
        def wrapper(self,
                    field = None,
                    field1 = None,
                    *args,
                    **kwargs,
                    ):
            if (field is None) and (field1 is None):
                return func(self, self.field, self.field1, *args, **kwargs)
            elif (field is None) and (field1 is not None):
                return func(self, self.field, field1, *args, **kwargs)
            elif (field is not None) and (field1 is None):
                return func(self, field, self.field1, *args, **kwargs)
            else:
                return func(self, field, field1, *args, **kwargs)
        return wrapper
    
    @default_fields
    def store_fields(self, field=None, field1=None, index: str = ""):
        self.store_field(field,
                         self.store_config.get_field_dir(index))
        self._field1.store_field(field1,
                                 self.store_config.get_field1_dir(index),
                                 )
    
    @property
    def input_field1(self,):
        return self._field1.input_field
    
    @input_field1.setter
    def input_field1(self, new_field):
        self._field1.input_field = new_field
    
    @property
    def field1(self,):
        return self._field1.field
    
    @field1.setter
    def field1(self, new_field):
        self._field1.field[:, :] = new_field
        
    @property
    def extent1(self,):
        return self._field1.extent
    
    @extent1.setter
    def extent1(self, new_extent):
        self._field1.extent[:] = new_extent