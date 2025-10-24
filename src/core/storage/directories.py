import os

class StorageConfig:
    """ Class to handle storage configuration."""
    def __init__(
        self,
        storage_config: dict,
        *args,
        **kwargs,
        ):
        """ Initialize storage configuration.

        Args:
            storage_config (dict): Dictionary containing storage configuration parameters. With the following keys:
                - home (str): Base directory for storage.
                - store (str, optional): Storage mode, either "last" or "stride". Defaults to "last".
                - stride (int, optional): Stride value for "stride" storage mode. Required if store is "stride".
        """
        self.home = storage_config["home"]
        
        if "store" in storage_config.keys():
            self.store = storage_config["store"]
        else:
            self.store = "last"
        
        if hasattr(self, "stride"):
            if self.store.lower() == "stride":
                self.stride = storage_config["stride"]
            else:
                self.stride = None
        else:
            self.stride = None
        
        self.endswith_dash()
        
        super().__init__(
            *args,
            **kwargs,
            )
        
    def endswith_dash(self,):
        """ Ensure the home directory ends with a slash."""
        if not self.home.endswith("/"):
            self.home += "/"
        
class FolderMethods(StorageConfig):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """ Initialize folder methods and ensure home folder exists."""
        super().__init__(
            *args,
            **kwargs,
        )
        
        self.home_folder()
        
    def home_folder(self,):
        """ Ensure the home folder exists."""
        if not os.path.exists(self.home):
            os.makedirs(self.home)
    
    def make_folder(self, relative_directory,):
        """ Create a folder at the specified relative directory if it does not exist."""
        self.home_folder()
        if not os.path.exists(self.home + relative_directory):
            os.makedirs(self.home + relative_directory)
            
    def get_directory(self, relative_directory=""):
        """ Get the full directory path for a given relative directory, creating it if necessary."""
        if "." in relative_directory:
            return self.home + relative_directory
        self.make_folder(relative_directory = relative_directory)
        return self.home + relative_directory
            
class FieldDirectories(FolderMethods):
    """ Class to handle field directories."""
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """ Initialize field directories and ensure field folder exists."""
        super().__init__(
            *args,
            **kwargs,
            )
        self.make_folder(relative_directory = self.field_rel_directory)
        
    @property
    def field_rel_directory(self,):
        return "Field/"
        
    def automatic_stride(self,):
        """ Automatically manage stride count for field storage."""
        if hasattr(self, "stride_count"):
            self.stride_count += 1
        else:
            self.stride_count = 1
        
    def field_filename(self, index=None):
        """ Get the filename for the field based on the storage mode and index."""
        if self.store.lower() == "last":
            dir_ = "field_last.h5"
        elif self.store.lower() == "stride":
            if (index == None) or (index == ""):
                index = self.stride_count
            dir_ = "field_" + str(index) + ".h5"
        return dir_
    
    def get_field_directory(self, index=None):
        """ Get the full directory path for the field based on the storage mode and index."""
        self.automatic_stride()
        return self.get_directory(self.field_rel_directory) + self.field_filename(index)
    
class CoupledFieldDirectories(FieldDirectories):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """ Initialize coupled field directories and ensure both field folders exist."""
        super().__init__(
            *args,
            **kwargs,
        )
        self.make_folder(self.field_rel_directory1)
        
    @property
    def field_rel_directory1(self,):
        return "Field1/"
        
    def get_field_directory(self, index=None):
        """ Get the full directory paths for both coupled fields based on the storage mode and index."""
        field_directory = super().get_field_directory(index)
        field1_directory = self.get_directory(self.field_rel_directory1) + self.field_filename(index)
        return field_directory, field1_directory