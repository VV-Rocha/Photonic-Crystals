import h5py
import pickle

from .directories import FieldDirectories, CoupledFieldDirectories


class StoreConfig:
    def store_configs(
        self,
        crystal_config: dict,
        beam_config: dict,
        simulation_config: dict,
        device_config: dict,
        modulation_config: dict,
        storage_config: dict,
    ):
        """ Store the simulation configuration dictionaries to storage.

        Args:
            crystal_config (dict): Crystal configuration dictionary.
            beam_config (dict): Beam configuration dictionary.
            simulation_config (dict): Simulation configuration dictionary.
            device_config (dict): Device configuration dictionary.
            modulation_config (dict): Modulation configuration dictionary.
            storage_config (dict): Storage configuration dictionary.
        """
        config_dict = {
            "medium_config": crystal_config,
            "beam_config": beam_config,
            "simulation_config": simulation_config,
            "device_config": device_config,
            "modulation_config": modulation_config,
            "storage_config": storage_config,   
        }

        with open(self.get_directory("config_dicts.pickle"), "wb") as fpkl:
            pickle.dump(config_dict, fpkl, protocol=pickle.HIGHEST_PROTOCOL)
        fpkl.close()

class StorageField(FieldDirectories, StoreConfig):
    """ Class to store simulation fields to storage."""
    def store_step(self, index=None):
        """ Store the field at a given step based on storage mode.

        Args:
            index (_type_, optional): step index to store. Defaults to None.
        """
        if self.store.lower() == "last":
            if index == self.Nsteps:
                self.store_field(index="last")
        elif self.store.lower() == "stride":
            self.store_field(index=index)
    
    def store_field(self, index = None):
        """ Store the field to storage.

        Args:
            index (_type_, optional): step index to store. Defaults to None.
        """
        file_dir = self.get_field_directory(index)
        with h5py.File(file_dir, "w") as hf:
            hf.create_dataset("field", data=self.field)
        hf.close()


class CoupledStorageField(CoupledFieldDirectories, StoreConfig):
    """ Class to handle storage of coupled simulation fields."""
    def store_step(self, index =None):
        """ Store the coupled fields at a given step based on storage mode.

        Args:
            index (str | int, optional): step index to store. Defaults to None.
        """
        if self.store.lower() == "last":
            if index == self.Nsteps:
                self.store_field(index="last")
        elif self.store.lower() == "stride":
            self.store_field(index=index)
            
    def store_field(self, index=None):
        """ Store the coupled fields to storage.

        Args:
            index (str | int, optional): step index to store. Defaults to None.
        """
        file_directories = self.get_field_directory(index)
        with h5py.File(file_directories[0], "w") as hf:
            hf.create_dataset("field", data=self.field)
        hf.close()
        with h5py.File(file_directories[1], "w") as hf:
            hf.create_dataset("field", data=self.field1)
        hf.close()