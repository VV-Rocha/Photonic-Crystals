import h5py
from pathlib import Path


from .write import _write_object_contents
from .utils import _object_has_dict_attributes

import h5py
from pathlib import Path


def _store_config(directory, object_dict):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    for key, value in object_dict.items():
        key = str(key)

        if isinstance(value, dict):
            subdirectory = directory / key
            _store_config(subdirectory, value)

        elif _object_has_dict_attributes(value):
            subdirectory = directory / key
            subdirectory.mkdir(parents=True, exist_ok=True)

            _store_config(subdirectory, vars(value))

        else:
            filepath = directory / f"{key}.h5"

            with h5py.File(filepath, "w") as h5file:
                _write_object_contents(h5file, value)