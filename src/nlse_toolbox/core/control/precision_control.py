import h5py

class PrecisionControl:
    """Holds predefined precision values for the simulation and data storage and analysis.
    The precision values are stored in a file and can be loaded or saved as needed."""
    def __init__(
        self,
        precision_config,
        ):
        """Initialize the PrecisionControl object with the desired precision.

        Args:
            precision (str, optional): Precision parameter "double" for double precision or "single" for single precision. Defaults to None.
        """
        self.precision = precision_config["precision"].lower()
        
        self.init_numpy_dtypes()
        
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
    def __init__(
        self,
        precision_config,
        ):
        """Initialize the PrecisionControl object with the desired precision.

        Args:
            precision (str, optional): Precision parameter "double" for double precision or "single" for single precision. Defaults to None.
        """
        super().__init__(
            precision_config = precision_config,
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