import h5py
import numpy as np


class LoadField:
    """ Class to load simulation fields from storage."""
    def load_field(
        self,
        index: str | int | None = None,
        ):
        """ Load the field from storage.

        Args:
            index (str | int | None, optional): Index of the field to load. Can be "last" or an integer index. Defaults to None.
        """
        with h5py.File(self.get_field_directory(index), "r") as f:
            self.field = f["field"][:]
        f.close()
        
class LoadSimulation(LoadField):
    """ Class to load entire simulation fields from storage."""
    def init_fields_zeros(self,):
        """ Initialize the fields array with zeros based on storage mode."""
        if self.store.lower() == "last":
            self.fields = np.zeros((2, *self.field_shape), dtype=np.complex128)
        else:
            self.fields = np.zeros((self.Nsteps, *self.field_shape), dtype=np.complex128)
    
    def load_last_field(self,):
        """ Load the last stored field into the fields array."""
        self.fields[1] = self.load_field()
    
    def mount_field(self, index = None):
        """ Load a specific field and mount it into the fields array."""
        self.load_field(index)
        self.fields[index] = self.field
    
    def load_simulation(self,):
        """ Load the entire simulation fields from storage."""
        self.init_fields_zeros()

        self.mount_field(index=0) # load initial state
        
        if self.store.lower() == "last":
            self.load_last_field()
        else:
            for i in range(1, self.Nsteps):
                self.mount_field(index = i)
                
class CoupledLoadField:
    """ Class to load coupled simulation fields from storage."""
    def load_field(
        self,
        directory,
        ):
        """ Load the first field from storage."""
        with h5py.File(directory, "r") as f:
            self.field = f["field"][:]
        f.close()
        
    def load_field1(
        self,
        directory,
        ):
        """ Load the second field from storage."""
        with h5py.File(directory, "r") as f:
            self.field1 = f["field"][:]
        f.close()

class LoadCoupledSimulation(CoupledLoadField):
    """ Class to load entire coupled simulation fields from storage."""
    def init_fields_zeros(self, field_number=0):
        """ Initialize the coupled fields arrays with zeros based on storage mode."""
        if field_number is None:        
            if self.store.lower() == "last":
                self.fields = np.zeros((2, *self.field_shape), dtype=np.complex128)
                self.fields1 = np.zeros((2, *self.field_shape), dtype=np.complex128)
            else:
                self.fields = np.zeros((self.Nsteps, *self.field_shape), dtype=np.complex128)
                self.fields1 = np.zeros((self.Nsteps, *self.field_shape), dtype=np.complex128)
        elif field_number is 0:
            if self.store.lower() == "last":
                self.fields = np.zeros((2, *self.field_shape), dtype=np.complex128)
            else:
                self.fields = np.zeros((self.Nsteps, *self.field_shape), dtype=np.complex128)
        elif field_number is 1:
            if self.store.lower() == "last":
                self.fields1 = np.zeros((2, *self.field_shape), dtype=np.complex128)
            else:
                self.fields1 = np.zeros((self.Nsteps, *self.field_shape), dtype=np.complex128)

    def load_last_field(self,):
        """ Load the last stored coupled fields into the fields arrays."""
        directory = self.get_field_directory("last")
        self.load_field(directory[0])
        self.fields[1] = self.field

    def load_simulation(self, field_number=0):
        """ Load the entire coupled simulation fields from storage.

        Args:
            field_number (int, optional): field number to load (0, 1 or None for both). Defaults to 0.
        """
        self.init_fields_zeros(field_number)
        
        if field_number is 0:
            # load initial state
            directory = self.get_field_directory(0)
            self.load_field(directory[0])
            self.fields[0] = self.field
        
            if self.store.lower() == "last":
                self.load_last_field()
            else:
                for i in range(1, self.Nsteps):
                    directory = self.get_field_directory(i)
                    self.load_field(directory[0])
                    self.fields[i] = self.field