from pathlib import Path
import h5py
import numpy as np


def _write_value(h5group, name, value):
    if isinstance(value, (int, float, bool, complex, np.number)):
        h5group.create_dataset(name, data=value)
        return

    if isinstance(value, str):
        dt = h5py.string_dtype(encoding="utf-8")
        h5group.create_dataset(name, data=value, dtype=dt)
        return

    if value is None:
        h5group.attrs[name] = "None"
        return

    if isinstance(value, np.ndarray):
        h5group.create_dataset(name, data=value)
        return

    if isinstance(value, (list, tuple)):
        try:
            h5group.create_dataset(name, data=np.array(value))
        except Exception:
            subgroup = h5group.create_group(name)
            for i, item in enumerate(value):
                _write_value(subgroup, f"item_{i}", item)
        return

    if isinstance(value, dict):
        subgroup = h5group.create_group(name)

        for key, item in value.items():
            _write_value(subgroup, str(key), item)

        return

    h5group.attrs[name] = repr(value)


def _write_config_file(filepath, config):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with h5py.File(filepath, "w") as h5file:
        if isinstance(config, dict):
            for key, value in config.items():
                _write_value(h5file, str(key), value)
        else:
            _write_value(h5file, "value", config)    


def store_config(directory, configs, overwrite=True):
    directory = Path(directory)

    if directory.exists() and not overwrite:
        raise FileExistsError(f"Config directory already exists: {directory}")

    directory.mkdir(parents=True, exist_ok=True)

    for config_name, config_value in configs.items():
        filepath = directory / f"{config_name}.h5"
        _write_config_file(filepath, config_value)