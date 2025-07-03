import arrayfire as af

from functools import wraps

from numpy import ndarray

import numpy as np

def return_afarray(field):
    """Returns the field as an Arrayfire Array."""
    if not isinstance(field, af.Array):
        return af.from_ndarray(field)
    return field
    
def return_ndarray(field):
    """Returns the field as a numpy ndarray."""
    if isinstance(field, af.Array):
        return field.to_ndarray()
    return field

class ConversionMethods:
    def convert_to_afarray(self,):
        """Converts the field to an Arrayfire Array. If the field is already an Arrayfire array, it does nothing."""
        self.field = return_afarray(self.field)
    
    def convert_to_ndarray(self,):
        """Converts the field to a numpy array. If the field is already a numpy array, it does nothing."""
        self.field = return_ndarray(self.field)

class CoupledConversionMethods(ConversionMethods):
    def convert_to_afarray(self,):
        super().convert_to_afarray()
        self.field1 = return_afarray(self.field1)
    
    def convert_to_ndarray(self,):
        super().convert_to_ndarray()
        self.field1 = return_ndarray(self.field1)


class AfField2D(ConversionMethods):
    """(Arrayfire) 2D field class. Features conversion functions to convert between ndarray and Arrayfire Array. The field is stored in an Arrayfire array. The metadata is stored in the extent attribute."""
    def __init__(self,
                 field,
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
        self._Field = field
        
        self.init_field()

    def get_intensity(self,):
        return af.abs(self.field) * af.abs(self.field)

    def get_total_intensity(self,):
        return self.get_intensity()

    def check_field(func):
        """If field is None default to self.field."""
        @wraps(func)
        def wrapper(self, field=None, *args, **kwargs):
            if field is None:
                return func(self, self.field, *args, **kwargs)
            return func(self, field, *args, **kwargs)
        return wrapper

    @check_field
    def store_field(self, field=None, index: str = ""):
        """Store the field in hdf5 format. The field is stored in the dataset "field" and the extent in the dataset "extent".
        The field and extent are stored as numpy ndarrays.

        Args:
            filename (str): Directory of the file to store the field. Defaults to None.
            field (ndarray, optional): Stores field, if field is None stores self.field. Defaults to None.
        """
        self._Field.store_field(return_ndarray(field), index)

    def update_Field(self,):
        self._Field.field[:, :] = return_ndarray(self.field)

    def init_field(self,):
        self.field = return_afarray(self._Field.field)

    @property
    def nfields(self,):
        return self._Field.nfields
    
from .field import CoupledModulatedFields2D
class AfCoupledFields2D(CoupledConversionMethods):
    "Extends the single field objects to two fields."
    def __init__(self,
                 fields: CoupledModulatedFields2D,
                 ):
        """Initializes the two fields. The fields are stored in a numpy array. The metadata is stored in the extent attribute.

        Args:
            simulation_config (SimulationConfig object): SimulationConfig object containing the simulation box configuration.
            modulation_config (ModulationConfig object): ModulationConfig object containing the modulation configuration.
            store_config (StoreConfig object, optional): StoreConfig object containing the structure and directories of the storage folder. Defaults to None.
            precision_control (PrecisionControl object, optional): PrecisionControl object containing the numpy and arrayfire numerical precision dtypes used. Defaults to None.
        """
        self._Fields = fields
        
        self.init_fields()
        
    def init_fields(self,):
        self.field = return_afarray(self._Fields.field)
        self.field1 = return_afarray(self._Fields.field1)
        
    def get_intensity(self,):
        return af.abs(self.field)*af.abs(self.field)
    
    def get_intensity1(self,):
        return af.abs(self.field1)*af.abs(self.field1)
    
    def get_total_intensity(self,):
        coherence = 0. # we are considering two incoherent fields only.
        i = self.get_intensity() + self.get_intensity1() # + coherence * np.sqrt(self.get_intensity()) * np.sqrt(self.get_intensity1())
        return i

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
    def store_fields(self,
                     field = None,
                     field1 = None,
                     index: str = "",
                     ):
        """Stores the fields in hdf5 format. The fields are stored in the dataset "field" and the extent in the dataset "extent". The fields are placed in a 'Field/' and 'Field1/' folder respectively. The extent is stored in the dataset "extent" and the field in the dataset "field". The field and extent are stored as numpy ndarrays.

        Args:
            index (str): Index to add to the 'field_{index}' base filename.
        """
        self._Fields.store_fields(return_ndarray(field),
                                  return_ndarray(field1),
                                  index,
                                  )
        # % TODO: Add method to automatically convert index to str and remove conversion in previous lines
        
    def update_Fields(self,):
        self._Fields.field[:, :] = return_ndarray(self.field)
        self._Fields.field1[:, :] = return_ndarray(self.field1)
        
    @property
    def nfields(self,):
        return self._Fields.nfields