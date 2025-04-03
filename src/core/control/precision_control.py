import h5py

class PrecisionControl:
    """Holds predefined precision values for the simulation and data storage and analysis.
    The precision values are stored in a file and can be loaded or saved as needed."""
    def __init__(self,
                 precision: str=None,
                 store_config=None,
                 ):
        """Initialize the PrecisionControl object with the desired precision.

        Args:
            precision (str, optional): Precision parameter "double" for double precision or "single" for single precision. Defaults to None.
            store_config (StorageObject, optional): Uses storage objects defined in storage_config.py to store the precision configuration. Defaults to None.
        """
        if (precision is None) and (store_config is not None):
            self.load_precision(store_config)
            
        self.precision = precision.lower()
        
        self.init_numpy_dtypes()
        
        if store_config is not None:
            self.store_precision(store_config)
        
    @classmethod
    def load_precision(cls,
                       store_config,
                       ):
        """Initialize PrecisionControl object from a stored configuration.

        Args:
            store_config (StorageObject): StorageObject containing the directory with the precision configuration.
        """
        filename = store_config.get_precision_dir()
        with h5py.File(filename, "r") as f:
            precision = f["precision"][()]
        f.close()
        if isinstance(precision, bytes,):
            precision = precision.decode("utf-8")
        return cls(precision=precision)
        
    def store_precision(self, store_config,):
        filename = store_config.get_precision_dir()
        with h5py.File(filename, "w") as f:
            f.create_dataset("precision", data=self.precision)
        f.close()
        
    def init_numpy_dtypes(self,):
        if self.precision == "double":
            from numpy import float64, complex128
            self.np_float = float64
            self.np_complex = complex128
        elif self.precision == "single":
            from numpy import float32, complex64
            self.np_float = float32
            self.np_complex = complex64


class AfPrecisionControl(PrecisionControl):
    """Holds predefined precision values for the simulation and data storage and analysis.
    The precision values are stored in a file and can be loaded or saved as needed."""
    def __init__(self,
                 precision: str = None,
                 store_config = None,
                 ):
        """Initialize the PrecisionControl object with the desired precision.

        Args:
            precision (str, optional): Precision parameter "double" for double precision or "single" for single precision. Defaults to None.
            store_config (StorageObject, optional): Uses storage objects defined in storage_config.py to store the precision configuration. Defaults to None.
        """
        super().__init__(precision = precision,
                         store_config = store_config,
                         )
        
        self.init_af_dtypes()
        
    def init_af_dtypes(self):
        """Initializes the arrayfire numerical types based on the required precision."""
        import arrayfire as af
        if self.precision == "double":
            self.af_float = af.Dtype.f64
            self.af_complex = af.Dtype.c64
        elif self.precision == "single":
            self.af_float = af.Dtype.f32
            self.af_complex = af.Dtype.c32
            
    @classmethod
    def load_precision(cls,
                       store_config,
                       ):
        """Initialize PrecisionControl object from a stored configuration.

        Args:
            store_config (StorageObject): StorageObject containing the directory with the precision configuration.
        """
        filename = store_config.get_precision_dir()
        with h5py.File(filename, "r") as f:
            precision = f["precision"][()]
        f.close()
        if isinstance(precision, bytes,):
            precision = precision.decode("utf-8")
        return cls(precision=precision)