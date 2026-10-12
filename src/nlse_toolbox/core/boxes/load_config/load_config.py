from pathlib import Path

import h5py
import numpy as np


def _decode_h5_value(value):
    if isinstance(value, (bytes, np.bytes_)):
        return value.decode("utf-8")

    if isinstance(value, np.generic):
        return value.item()

    return value


def _read_dataset(dataset):
    # Decode UTF-8 strings, including arrays of strings.
    if h5py.check_string_dtype(dataset.dtype) is not None:
        return dataset.asstr()[()]

    return _decode_h5_value(dataset[()])


def _read_group(group, reconstruct_list=True):
    result = {}

    for key, value in group.attrs.items():
        value = _decode_h5_value(value)
        result[key] = (
            None if isinstance(value, str) and value == "None" else value
        )

    for key, item in group.items():
        if isinstance(item, h5py.Dataset):
            result[key] = _read_dataset(item)
        else:
            result[key] = _read_group(item)

    # Your writer stores heterogeneous sequences as item_0, item_1, ...
    if reconstruct_list and result:
        expected_keys = {f"item_{i}" for i in range(len(result))}

        if set(result) == expected_keys:
            return [result[f"item_{i}"] for i in range(len(result))]

    return result


def _load_h5_file(filepath):
    with h5py.File(filepath, "r") as h5file:
        # The root represents the configuration dictionary.
        return _read_group(h5file, reconstruct_list=False)


def _load_config_dict(configs_directory):
    configs_directory = Path(configs_directory)

    if not configs_directory.exists():
        raise FileNotFoundError(
            f"Config directory does not exist: {configs_directory}"
        )

    if not configs_directory.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {configs_directory}"
        )

    configs = {}

    for filepath in sorted(configs_directory.glob("*.h5")):
        configs[filepath.stem] = _load_h5_file(filepath)

    return configs


def _load_stored_config(directory):
    return _load_config_dict(Path(directory) / "configs")