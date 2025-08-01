# % TODO: Add mechanisms to assess missing configuration files and print a warning.
import os

from functools import wraps

import inspect

default_storage_config = {"store": "last",
                          "home": "./Data/",
                          "extension": ".h5",
                          "stride": 1,
                          }

def validate_directory(func):
    """Decorator to check if the directory exists."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        self = bound_args.arguments["self"]
        directory = bound_args.arguments["directory"]
        if hasattr(self, "home"):
            directory = self.home + directory
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        return func(*args, **kwargs)
    return wrapper

def validate_workspace(func):
    """Decorator to verify if the home directory ends with dash and exists and correct these if needed."""
    @wraps(func)
    def wrapper(self, storage_config):
        if not storage_config["home"].endswith("/"):
            storage_config["home"] = storage_config["home"] + "/"
            
        if not os.path.exists(storage_config["home"]):
            os.makedirs(storage_config["home"])
        
        return func(self, storage_config)
    return wrapper

def endswith_dash(func):
    """Guarantee the directory endswith '/'."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        if bound_args.arguments["directory"] != "":
            if not bound_args.arguments["directory"].endswith("/"):
                bound_args.arguments["directory"] = bound_args.arguments["directory"] + "/" 
        return func(*bound_args.args, **bound_args.kwargs)
    return wrapper

class BaseConfig:
    """Base class for storage configurations."""
    @validate_workspace
    def __init__(self, storage_config=default_storage_config):
        """Initialize the base class for returning directories.

        Args:
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
        """
        self.home = storage_config["home"]
        self.extension = storage_config["extension"]        
    
    @validate_directory
    @endswith_dash
    def get_directory(self,
                      filename: str = "",
                      directory: str = "",
                      ) -> str:
        """Returns the directory for the given filename and relative directory. The directory is constructed by concatenating the home directory, the relative directory, the filename, and the extension.

        Args:
            filename (str, optional): Name of the data file (without extension). Defaults to "".
            directory (str, optional): Relative directory starting from home. Defaults to "".

        Returns:
            str: The directory for the given filename.
        """
        return self.home + directory + filename + self.extension

class FundamentalStorage(BaseConfig):
    """Base class for fundamental storage configurations."""
    def __init__(self, storage_config=default_storage_config):
        """Initializes the base class for returning the directories for the precision, medium_parameters, beam_config, and box_config.

        Args:
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
        """
        super().__init__(storage_config=storage_config)
        
    def get_precision_dir(self,):
        """Returns the directory for the precision configuration file."""
        return self.get_directory(filename = "precision",)
    
    def get_medium_dir(self,):
        """Returns the directory for the medium parameters configuration file."""
        return self.get_directory(filename = "medium_parameters",)

    def get_beam_dir(self,):
        """Returns the directory for the beam configuration file."""
        return self.get_directory(filename = "beam_config",)
    
    def get_box_dir(self,):
        """Returns the directory for the box configuration file."""
        return self.get_directory(filename = "box_config",)
    
class FieldStorage(FundamentalStorage):
    """ Base class for field storage configurations."""
    def __init__(self, storage_config=default_storage_config):
        """Initializes the base class for returning the directories for the field. The field is stored in the directory "Field/". Inherits from the FundamentalStorage class.

        Args:
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
        """
        super().__init__(storage_config=storage_config)

    def get_field_dir(self,
                      index: str = "",
                      ) -> str:
        """Returns the directory for the field configuration file. The field is stored in the directory "Field/".
        
        Args:
            index (str, optional): Index to be appended to the filename 'field_{index}'. Defaults to "".

        Returns:
            str: Directory for the field configuration file.
        """
        if index == "":
            filename = "field"
        else:
            filename = "field_" + index
        return self.get_directory(filename = filename,
                                  directory = "Field/",
                                  )
        
    def get_input_dir(self,):
        """Returns the directory for the input configuration file."""
        return self.get_directory(filename = "input_config",)
    
class CoupledFieldStorage(FieldStorage):
    """ Base class for two coupled field storage configurations."""
    def __init__(self, storage_config=default_storage_config):
        """Initializes the base class for returning the directories for the field. The field is stored in the directory "Field1/". Inherits from the FieldStorage class.

        Args:
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
        """
        super().__init__(storage_config=storage_config)
        
    def get_field1_dir(self,
                      index: str = "",
                      ) -> str:
        """Returns the directory for the field1 configuration file. The field is stored in the directory "Field1/".

        Args:
            index (str, optional): Index to be appended to the filename 'field_{index}'. Defaults to "".
            
        Returns:
            str: _description_
        """
        return self.get_directory(filename = "field_" + index,
                                  directory = "Field1/",
                                  )
    
class SimulationStorageConfig:
    """Base class for simulation storage configurations."""
    def __init__(self, storage_config=default_storage_config):
        """Initializes the base class for the simulation storage configuration.

        Args:
            store (str): Store the last simulation step ('last') or in strides ('strides').
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
            stride (int, optional): Number of stride steps to be used if store='strides'. Defaults to 1.
        """
        super().__init__(storage_config=storage_config)
        
        self.store = storage_config["store"]
        if (self.store == "strides"):
            self.stride = storage_config["stride"]
        
    def get_store_type(self,):
        """Returns the store type."""
        return self.store
    
    def get_stride(self,):
        """Returns the stride number."""
        return self.stride
    
    def get_coefs_dir(self,):
        """Returns the directory of the coefficients configuration file used in the simulation."""
        return self.get_directory(filename = "eq_coefs",)

class StorageConfig(SimulationStorageConfig, FieldStorage):
    """Storage configuration class for the simulation of a single field."""
    def __init__(self, storage_config=default_storage_config,):
        """Initializes the storage configuration class for the simulation of a single field. Inherits from the SimulationStorageConfig and FieldStorage classes.

        Args:
            store (str): Store the last simulation step ('last') or in strides ('strides').
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
            stride (int, optional): Number of stride steps to be used if store='strides'. Defaults to 1.
        """
        super().__init__(storage_config=storage_config)
    
class CoupledStorageConfig(SimulationStorageConfig, CoupledFieldStorage):
    """Storage configuration class for the simulation of two coupled fields."""
    def __init__(self, storage_config=default_storage_config,):
        """Initializes the storage configuration class for the simulation of two coupled fields. Inherits from the SimulationStorageConfig and CoupledFieldStorage classes.

        Args:
            store (str): Store the last simulation step ('last') or in strides ('strides').
            home (str, optional): Home directory for storing data. Defaults to "./Data/".
            extension (str, optional): Extension used for the storing files. Defaults to ".h5".
            stride (int, optional): Number of stride steps to be used if store='strides'. Defaults to 1.
        """
        super().__init__(storage_config=storage_config)