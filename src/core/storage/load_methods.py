import numpy as np
import h5py

from .directories import FieldDirectories


def init_array(box):
    return np.empty(
        (
            box.mesh.Nz+1,
            box.mesh.Nx,
            box.mesh.Ny,
        ),
        dtype = np.complex128,    
    )
    

def _load_file(
    idx,
    folder_dir,
    box,
    beams,
):
    directory = folder_dir + f"field_{idx}.h5"
    with h5py.File(directory, "r") as f:
        for beam in f.keys():
            if (idx==0):
                beams[beam].field = init_array(box)
            beams[beam].field[idx] = f[beam][:]
    return beams


class LoadSimulation(FieldDirectories):
    def _load_simulation(self, box):        
        for i in range(box.mesh.Nz+1):
            box.beams = _load_file(
                i,
                box.storage.get_directory("Field/"),
                box,
                box.beams,
            )