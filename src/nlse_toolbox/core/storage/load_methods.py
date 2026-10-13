import numpy as np
import h5py

from .directories import FieldDirectories


def init_array(box):
    if box.storage.store.lower() == "last":
        return np.empty(
            (
                2,
                box.mesh.Nx,
                box.mesh.Ny,
            ),
            dtype = np.complex128,    
        )
    elif box.storage.store.lower() == "stride":
        return np.empty(
            (
                int(1 + box.mesh.Nz // box.storage.stride),
                box.mesh.Nx,
                box.mesh.Ny,
            ),
            dtype = np.complex128,    
        )


def _load_file(
    i,
    idx,
    folder_dir,
    box,
):
    directory = folder_dir + f"field_{"last" if (i==-1) else i}.h5"
    with h5py.File(directory, "r") as f:
        for beam in f.keys():
            if (idx==0):
                box.beams[beam].field = init_array(box)
            box.beams[beam].field[idx] = f[beam][:]
    return box.beams


class LoadSimulation(FieldDirectories):
    def _load_simulation(self, box):
        if (box.storage.store.lower() == "last"):
            search_range = [0, -1]
        elif (box.storage.store.lower() == "stride"):
            search_range = range(0, box.mesh.Nz+1, box.storage.stride)
            idx = 0
        for i in search_range:
            box.beams = _load_file(
                i,
                idx,
                box.storage.get_directory("Field/"),
                box,
            )
            if (box.storage.store.lower() == "stride"):
                idx += 1