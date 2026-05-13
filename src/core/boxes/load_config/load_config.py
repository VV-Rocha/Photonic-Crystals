# load_stored_config.py

from pathlib import Path
from types import SimpleNamespace

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

    if set(result.keys()) == {"value"}:
        return result["value"]

    return result


def _load_h5_file(filepath):
    with h5py.File(filepath, "r") as h5file:
        return _read_group(h5file)


def _to_namespace(value):
    if isinstance(value, dict):
        return SimpleNamespace(
            **{
                key: _to_namespace(sub_value)
                for key, sub_value in value.items()
            }
        )

    return value


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
    """
    Add names that match the original config module.

    Stored names:
        media_config
        model_config
        beams_config

    Useful aliases:
        crystal_config
        lattice_config
        state_structure_config
        state_modulation_config
        lattice_modulation_config
    """
    configs = dict(configs)

    if "media_config" in configs:
        configs["crystal_config"] = configs["media_config"]

    if "model_config" in configs:
        model_config = configs["model_config"]

        if isinstance(model_config, dict):
            if "crystal_config" in model_config:
                configs["crystal_config"] = model_config["crystal_config"]

            if "lattice_config" in model_config:
                configs["lattice_config"] = model_config["lattice_config"]

    if "beams_config" in configs:
        beams_config = configs["beams_config"]

        if isinstance(beams_config, dict):
            for beam_name, beam_entry in beams_config.items():
                if not isinstance(beam_entry, dict):
                    continue

                beam_config = beam_entry.get("config", beam_entry)

                if not isinstance(beam_config, dict):
                    continue

                for key, value in beam_config.items():
                    if key.endswith("_config"):
                        configs[key] = value

    return configs

def _load_stored_config(data_directory):
    data_directory = Path(data_directory)
    configs_directory = data_directory / "configs"

    configs = _load_config_dict(configs_directory)
    configs = _add_config_aliases(configs)

    return SimpleNamespace(**configs)