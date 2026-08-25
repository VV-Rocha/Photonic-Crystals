from pathlib import Path

import h5py
import numpy as np


def _decode_h5_value(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")

    if isinstance(value, np.generic):
        return value.item()

    return value


def _read_dataset(dataset):
    value = dataset[()]

    if isinstance(value, bytes):
        return value.decode("utf-8")

    if isinstance(value, np.ndarray):
        if value.shape == ():
            return value.item()

        return value

    if isinstance(value, np.generic):
        return value.item()

    return value


def _read_group(group):
    result = {}

    for key, value in group.attrs.items():
        value = _decode_h5_value(value)

        if value == "None":
            result[key] = None
        else:
            result[key] = value

    for key, item in group.items():

        if isinstance(item, h5py.Dataset):
            result[key] = _read_dataset(item)

        elif isinstance(item, h5py.Group):
            result[key] = _read_group(item)

    # Reconstruct heterogeneous lists
    if result and all(key.startswith("item_") for key in result):
        try:
            items = sorted(
                (int(key.split("_", 1)[1]), value)
                for key, value in result.items()
            )

            if [i for i, _ in items] == list(range(len(items))):
                return [value for _, value in items]

        except (ValueError, IndexError):
            pass

    return result


def _load_h5_file(filepath):
    with h5py.File(filepath, "r") as h5file:
        return _read_group(h5file)


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

    for filepath in configs_directory.glob("*.h5"):
        configs[filepath.stem] = _load_h5_file(filepath)

    for subdirectory in configs_directory.iterdir():
        if subdirectory.is_dir():
            configs[subdirectory.name] = _load_config_dict(subdirectory)

    return configs


def _add_config_aliases(configs):
    configs = dict(configs)

    if "media_config" in configs:
        configs["crystal_config"] = configs["media_config"]

    if "model_config" in configs:
        model = configs["model_config"]

        if "lattice_config" in model:
            configs["lattice_config"] = model["lattice_config"]

    if "beams_config" in configs:
        beams = configs["beams_config"]

        if "beam_1" in beams:
            configs["state_modulation_config"] = (
                beams["beam_1"]["envelope_config"]
            )

            configs["state_structure_config"] = (
                beams["beam_1"]["landscape_config"]
            )

        if "beam_2" in beams:
            configs["lattice_modulation_config"] = (
                beams["beam_2"]["envelope_config"]
            )

    return configs


def _load_stored_config(data_directory):
    configs_directory = Path(data_directory) / "configs"

    configs = _load_config_dict(configs_directory)
    configs = _add_config_aliases(configs)

    return configs