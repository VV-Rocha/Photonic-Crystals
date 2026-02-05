import h5py
import numpy as np

from .directories import FieldDirectories
from .directories import CoupledFieldDirectories

class LoadField(FieldDirectories):
    """ Class to load simulation fields from storage."""
    def get_field(
        self,
        directory: str,
        ):
        """ Get the field from directory.

        Args:
            directory (str): Directory of the field .h5 file.
        """
        with h5py.File(directory, "r") as f:
            field = f["field"][:]
        f.close()
        return field

class LoadSimulation(LoadField):
    """ Class to load entire simulation fields from storage."""
    def get_last_field(self,):
        """ Load the last stored field into the fields array."""
        return self.get_field(self.get_field_directory("last"))
    
    def get_input_field(self,):
        return self.get_field(self.get_field_directory(0))
    
    def mount_field(self, index = None):
        """ Load a specific field and mount it into the fields array."""
        self.fields[index] = self.get_field(self.get_field_directory(index))
    
    def load_field(self,):
        """ Load the entire simulation fields from storage."""
        if self.store.lower() == "last":
            self.fields = np.zeros((2, *self.field_shape), dtype=np.complex128)
            self.fields[0] = self.get_input_field()
            self.fields[1] = self.get_last_field()
        else:
            self.fields = np.zeros((self.Nsteps+1, *self.field_shape), dtype=np.complex128)
            for i in range(self.Nsteps + 1):
                self.mount_field(index = i)
                
class LoadCoupledSimulation(CoupledFieldDirectories, LoadSimulation):
    """ Class to load entire coupled simulation fields from storage."""
    def get_last_field(self,):
        """ Load the last stored field into the fields array."""
        return self.get_field(self.get_field_directory("last")[0])
    
    def get_input_field(self,):
        return self.get_field(self.get_field_directory(0)[0])
    
    def mount_field(self, index = None):
        """ Load a specific field and mount it into the fields array."""
        self.fields[index] = self.get_field(self.get_field_directory(index)[0])
    
    def mount_field1(self, index = None):
        """ Load a specific field and mount it into the fields array."""
        self.fields1[index] = self.get_field(self.get_field_directory(index)[1])
    
    def mount_fields(self, index = None):
        """ Mount fields."""
        self.fields[index] = self.get_field(self.get_field_directory(index)[0])
        self.fields1[index] = self.get_field(self.get_field_directory(index)[1])
    
    def get_input_field1(self,):
        return self.get_field(self.get_field_directory(0)[1])
    
    def get_last_field1(self,):
        """ Load the last stored field into the fields array."""
        return self.get_field(self.get_field_directory("last")[1])

    def load_field(self,):
        """ Load the entire simulation fields from storage."""
        if self.store.lower() == "last":
            self.fields = np.zeros((2, *self.field_shape), dtype=np.complex128)
            self.fields[0] = self.get_input_field()
            self.fields[1] = self.get_last_field()
        else:
            self.fields = np.zeros((self.Nsteps+1, *self.field_shape), dtype=np.complex128)
            for i in range(self.Nsteps + 1):
                self.mount_field(index = i)
    
    def load_field1(self,):
        """ Load the entire simulation fields from storage."""
        if self.store.lower() == "last":
            self.fields1 = np.zeros((2, *self.field_shape), dtype=np.complex128)
            self.fields1[0] = self.get_input_field1()
            self.fields1[1] = self.get_last_field1()
        else:
            self.fields1 = np.zeros((self.Nsteps+1, *self.field_shape), dtype=np.complex128)
            for i in range(self.Nsteps + 1):
                self.mount_field1(index = i)
        
    def load_fields(
        self,
        field_number = None,
    ):
        if field_number == 0:
            self.load_field()
        elif field_number == 1:
            self.load_field1()
        else:
            if self.store.lower() == "last":
                self.load_field()
                self.load_field1()
            elif self.store.lower() == "stride":
                self.fields = np.zeros((self.Nsteps+1, *self.field_shape), dtype=np.complex128)
                self.fields1 = np.zeros((self.Nsteps+1, *self.field_shape), dtype=np.complex128)
                for i in range(self.Nsteps + 1):
                    self.mount_fields(index = i)