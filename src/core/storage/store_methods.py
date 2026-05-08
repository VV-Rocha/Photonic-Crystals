import h5py
import pickle

from .directories import FieldDirectories


class StoreConfig:
    def store_configs(
        self,
        **kwargs,
    ):
        """ Store the simulation configuration dictionaries to storage.

        Args:
            **kwargs: running at the beggining, all input dictionary with configs are stored.
        """
        with open(self.get_directory("config_dicts.pickle"), "wb") as fpkl:
            pickle.dump(kwargs, fpkl, protocol=pickle.HIGHEST_PROTOCOL)
        fpkl.close()

class StorageField(FieldDirectories, StoreConfig):
    """ Class to store simulation fields to storage."""
    def store_step(
        self,
        box,
        index=None,
    ):
        """ Store the field at a given step based on storage mode.

        Args:
            index (_type_, optional): step index to store. Defaults to None.
        """
        if (self.store.lower() == "last"):
            if (index == self.Nsteps):
                self.store_field(
                    box,
                    index="last",
                )
        elif (self.store.lower() == "stride"):
            self.store_field(
                box,
                index=index,
            )
    
    def store_field(
        self,
        box,
        index=None,
    ):
        """
        Store the field to storage.
        
        Args:
            index (_type_, optional): step index to store. Defaults to None.
        """
        file_dir = self.get_field_directory(index)
        
        with h5py.File(file_dir, "w") as hf:
            for beam_key, beam_value in box.beams.items():
                hf.create_dataset(beam_key, data=beam_value.field)
        hf.close()