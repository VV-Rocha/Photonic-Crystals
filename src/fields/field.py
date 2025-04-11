# % TODO: Rewrite input class to handle noise addition and plotting. Have it inherit landscape functions to plot the fields.

# % TODO: Add a function to initialize the objects by reading of a hdf5 file. As input this method should receive a StoreConfig and automatically read the necessary files.

from functools import wraps

from numpy import ndarray

def default_precision(func):
    @wraps(func)
    def wrapper(self, config, precision_control, *args, **kwargs):
        # % TODO: Later change the if condition to verify isinstance(precision, PrecisionControl)
        if precision_control is None:
            from numpy import complex128
            return func(self, config, complex128)
        return func(self, config, precision_control.np_complex)
    return wrapper

def cache_import_StoreField(init_func):
    @wraps(init_func)
    def wrapper(*args, **kwargs):
        if not hasattr(StoreField, "_File"):
            from h5py import File
            StoreField._File = File
        return init_func(*args, **kwargs)
    return wrapper

class StoreField:
    """Class to store and load fields in hdf5 format."""
    @cache_import_StoreField
    def __init__(self,
                 storage_config=None,
                 **kwargs,
                 ):
        super().__init__(**kwargs)
        self.storage_config = storage_config

    def store_field(self, field: ndarray=None, filename: str = ""):
        """Store the field in hdf5 format. The field is stored in the dataset "field" and the extent in the dataset "extent".

        Args:
            filename (str): Directory of the file to store the field. Defaults to None.
            field (ndarray, optional): Stores field, if field is None stores self.field. Defaults to None.
        """
        with self.__class__._File(filename, "w") as f:
            f.create_dataset("field", data=field)
            f.create_dataset("extent", data=self.extent)
        f.close()
        
    def load_field(self, filename: str):
        """Load the field from hdf5 format.

        Args:
            filename (str): Directory of the file to load the field.
        """
        with self.__class__._File(filename, "r") as f:
            self.field = f["field"][:]
            self.extent = f["extent"][:]
        f.close()

def cache_import_Field2D(init_func):
    @wraps(init_func)
    def wrapper(*args, **kwargs):
        if not hasattr(Field2D, "_zeros"):
            from numpy import zeros
            Field2D._zeros = zeros
        if not hasattr(Field2D, "_array"):
            from numpy import array
            Field2D._array = array
        if not hasattr(Field2D, "_copy"):
            from numpy import copy
            Field2D._copy = copy
        return init_func(*args, **kwargs)
    return wrapper

class Field2D(StoreField, ):
    """(Numpy) 2D field class."""
    @cache_import_Field2D
    def __init__(self,
                 simulation_config,
                 precision_control=None,
                 storage_config=None,
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
            storage_config (StorageConfig, optional): StorageConfig object containing the structure and directories of the storage folder. Defaults to None.
        """
        super().__init__(storage_config = storage_config,
                         )
        self.init_field(simulation_config, precision_control)
    
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
                self.extent = self.__class__._array([x_min, x_max, y_min, y_max])
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
        self.field = self.__class__._zeros(shape, precision_control)

    def check_field(func):
        """Decorator to check if the given field is None. If it is, the function uses the field attribute of the class. This is used to avoid having to pass the field as an argument every time.
        """
        @wraps(func)
        def wrapper(self, field=None, *args, **kwargs):
            if field is None:
                return func(self, self.field, *args, **kwargs)
            return func(self, field, *args, **kwargs)
        return wrapper

    @check_field
    def copy_input_field(self,
                         field: ndarray | None = None,
                         ):
        self.input_field = self.__class__._copy(field)

    @check_field
    def store_field(self, field=None, filename:str = ""):
        """Store the field in hdf5 format. The field is stored in the dataset "field" and the extent in the dataset "extent".

        Args:
            filename (str): Directory of the file to store the field.
            field (ndarray, optional): Field to be stored. Defaults to self.field.
        """
        super().store_field(field, filename)

def cache_import_AfField2D(init_func):
    @wraps(init_func)
    def wrapper(*args, **kwargs):
        if not hasattr(AfField2D, "_Array"):
            from arrayfire import Array
            AfField2D._Array = Array
        if not hasattr(AfField2D, "_from_ndarray"):
            from arrayfire.interop import from_ndarray
            AfField2D._from_ndarray = from_ndarray
        return init_func(*args, **kwargs)        
    return wrapper

class AfField2D(Field2D):
    """(Arrayfire) 2D field class. Features conversion functions to convert between ndarray and Arrayfire Array.
    The field is stored in an Arrayfire array. The metadata is stored in the extent attribute."""
    @cache_import_AfField2D
    def __init__(self,
                 simulation_config,
                 precision_control=None,
                 storage_config=None,
                 ):
        """Initializes the field array and the metadata of the field.

        Args:
            simulation_config (SimulationConfig object): Simulation box configuration. The parameters required are:
                - Nx: Number of points in the x direction.
                - Ny: Number of points in the y direction.
                - lx: Length of the box in the x direction.
                - ly: Length of the box in the y direction.
            precision_control (PrecisionControl object, optional): PrecisionControl object containing the numpy and arrayfire numerical precision dtypes used. Defaults to None.
            storage_config (StorageConfig object, optional): StorageConfig object containing the structure and directories of the storage folder. Defaults to None.
        """
        super().__init__(simulation_config = simulation_config,
                         precision_control = precision_control,
                         storage_config = storage_config,
                         )
    
    def convert_to_afarray(self,):
        """Converts the field to an Arrayfire Array. If the field is already an Arrayfire array, it does nothing."""
        self.field = self.return_afarray()
        
    def convert_to_ndarray(self,):
        """Converts the field to a numpy array. If the field is already a numpy array, it does nothing."""
        self.field = self.return_ndarray()
        
    def return_afarray(self,):
        """Returns the field as an Arrayfire Array."""
        if not isinstance(self.field, self.__class__._Array):
            return self.__class__._from_ndarray(self.field)
        return self.field
        
    def return_ndarray(self,):
        """Returns the field as a numpy ndarray."""
        if isinstance(self.field, self.__class__._Array):
            return self.field.to_ndarray()
        return self.field

    def check_field(func):
        @wraps(func)
        def wrapper(self, field=None, *args, **kwargs):
            if field is None:
                return func(self, self.field, *args, **kwargs)
            return func(self, field, *args, **kwargs)
        return wrapper

    @check_field
    def store_field(self, field=None, filename: str = ""):
        """Store the field in hdf5 format. The field is stored in the dataset "field" and the extent in the dataset "extent".
        The field and extent are stored as numpy ndarrays.

        Args:
            filename (str): Directory of the file to store the field. Defaults to None.
            field (ndarray, optional): Stores field, if field is None stores self.field. Defaults to None.
        """
        super().store_field(self.return_ndarray(), filename,)

class AfLandscapedField2D(AfField2D):
    """(Arrayfire) 2D field class with landscape. The field is stored in an Arrayfire array. The metadata is stored in the extent attribute."""
    def __init__(self,
                 simulation_config,
                 beam_config,
                 precision_control=None,
                 storage_config=None,
                 ):
        super().__init__(simulation_config = simulation_config,
                         precision_control = precision_control,
                         storage_config = storage_config,
                         )
        
        self.init_canvas(simulation_config,
                         precision_control,
                         )
        self.beam_config = beam_config

    @default_precision
    def init_canvas(self, config, precision_control,):
        """Initializes the beam profile and the landscape modulation. The profile and landscape are stored in a numpy array.

        Args:
            config (_type_): SimulationConfig object containing the simulation box configuration. The parameters required are:
                - Nx: Number of points in the x direction.
                - Ny: Number of points in the y direction.
            precision_control (_type_): PrecisionControl object containing the numpy numerical precision of the numpy and arrayfire dtypes used.
        """
        shape = (config["Nx"], config["Ny"])
        self.profile = self.__class__._zeros(shape, precision_control)
        self.landscape = self.__class__._zeros(shape, precision_control)
    
    def check_array_type(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(self.field, self.__class__._Array):
                self.convert_to_ndarray()
                func(self, *args, **kwargs)
                self.convert_to_afarray()
                return None
            func(self, *args, **kwargs)
            return None
        return wrapper
    
    @check_array_type
    def gen_field(self, mesh,):
        """Generates the field using the landscape and the modulation function. 

        Args:
            mesh (Mesh2D object): Mesh of the domain of the landscape function.
        """
        self.field[:,:] = self.beam_config.landscape(mesh) * self.beam_config.modulation_function(mesh)
        
class AfCoupled2D(AfLandscapedField2D):
    "Extends the single field objects to two fields."
    # % TODO: Change the class to first expose the method of _field1 and then define the functions on top.
    def __init__(self,
                 simulation_config,
                 modulation_config,
                 store_config=None,
                 precision_control=None,
                 ):
        """Initializes the two fields. The fields are stored in a numpy array. The metadata is stored in the extent attribute.

        Args:
            simulation_config (SimulationConfig object): SimulationConfig object containing the simulation box configuration.
            modulation_config (ModulationConfig object): ModulationConfig object containing the modulation configuration.
            store_config (StoreConfig object, optional): StoreConfig object containing the structure and directories of the storage folder. Defaults to None.
            precision_control (PrecisionControl object, optional): PrecisionControl object containing the numpy and arrayfire numerical precision dtypes used. Defaults to None.
        """
        super().__init__(simulation_config = simulation_config,
                         beam_config = modulation_config.beam,
                         precision_control = precision_control,
                         )
        self.store_config = store_config
        
        self._field1 = AfLandscapedField2D(simulation_config = simulation_config,
                                         beam_config = modulation_config.beam1,
                                         precision_control = precision_control,
                                         )
        
    def gen_fields(self,
                   mesh,
                   ):
        """Calls the field generation function of the two fields. The fields are generated using the landscape and the modulation function. The field generation function is defined in the modulation_config object.

        Args:
            mesh (Mesh2D object): Mesh of the domain of the landscape functions.
        """
        self.gen_field(mesh)
        self._field1.gen_field(mesh)

    def convert_fields_to_ndarray(self,):
        """Converts the fields to numpy ndarrays. If the fields are already numpy ndarrays, it does nothing."""
        self.convert_to_ndarray()
        self._field1.convert_to_ndarray()
        
    def convert_fields_to_afarray(self,):
        """Converts the fields to Arrayfire Array. If the fields are already Arrayfire Array, it does nothing."""
        self.convert_to_afarray()
        self._field1.convert_to_afarray()
    
    def store_fields(self,
                     index: str,
                     ):
        """Stores the fields in hdf5 format. The fields are stored in the dataset "field" and the extent in the dataset "extent". The fields are placed in a 'Field/' and 'Field1/' folder respectively. The extent is stored in the dataset "extent" and the field in the dataset "field". The field and extent are stored as numpy ndarrays.

        Args:
            index (str): Index to add to the 'field_{index}' base filename.
        """
        self.store_field(self.field, self.store_config.get_field_dir(index))
        self._field1.store_field(self.field1, self.store_config.get_field1_dir(index),)
        # % TODO: Add method to automatically convert index to str and remove conversion in previous lines

    def copy_input_fields(self,):
        self.copy_input_field()
        self._field1.copy_input_field()
    
    @property
    def input_field1(self,):
        return self._field1.input_field

    @property
    def field1(self,):
        return self._field1.field
    
    @field1.setter
    def field1(self, new_field):
        self._field1.field = new_field
    
    @property
    def extent1(self,):
        return self._field1.extent