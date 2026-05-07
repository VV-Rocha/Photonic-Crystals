import numpy as np
import h5py

def _write_value(h5group, name, value, visited=None):
    """
    Recursively write a value to an HDF5 group.

    - Basic values become datasets.
    - Lists/tuples/arrays become datasets if possible.
    - Dicts become groups.
    - Objects become groups containing their attributes.
    """

    if visited is None:
        visited = set()

    # Avoid infinite recursion if objects reference each other
    value_id = id(value)
    if value_id in visited:
        h5group.attrs[f"{name}_skipped"] = "Circular reference detected"
        return

    # Basic scalar values
    if isinstance(value, (int, float, bool, complex, np.number)):
        h5group.create_dataset(name, data=value)
        return

    # Strings
    if isinstance(value, str):
        dt = h5py.string_dtype(encoding="utf-8")
        h5group.create_dataset(name, data=value, dtype=dt)
        return

    # None
    if value is None:
        h5group.attrs[name] = "None"
        return

    # NumPy arrays
    if isinstance(value, np.ndarray):
        h5group.create_dataset(name, data=value)
        return

    # Lists or tuples
    if isinstance(value, (list, tuple)):
        try:
            h5group.create_dataset(name, data=np.array(value))
        except Exception:
            subgroup = h5group.create_group(name)
            for i, item in enumerate(value):
                _write_value(subgroup, f"item_{i}", item, visited)
        return

    # Dictionaries
    if isinstance(value, dict):
        subgroup = h5group.create_group(name)

        for key, item in value.items():
            key = str(key)
            _write_value(subgroup, key, item, visited)

        return

    # Objects with attributes
    if hasattr(value, "__dict__"):
        visited.add(value_id)

        subgroup = h5group.create_group(name)

        # Store class information
        subgroup.attrs["class"] = value.__class__.__name__
        subgroup.attrs["module"] = value.__class__.__module__

        for attr_name, attr_value in vars(value).items():

            # Optional: skip private/internal attributes
            if attr_name.startswith("_"):
                continue

            # Optional: skip functions/methods
            if callable(attr_value):
                continue

            _write_value(subgroup, attr_name, attr_value, visited)

        visited.remove(value_id)
        return

    # Fallback for unsupported types
    h5group.attrs[name] = repr(value)
    
    
def _write_object_contents(h5file, obj):
    """
    Write an object's attributes directly into the root of the HDF5 file.
    This avoids creating an extra root group named after the object.
    """

    if hasattr(obj, "__dict__"):
        h5file.attrs["class"] = obj.__class__.__name__
        h5file.attrs["module"] = obj.__class__.__module__

        visited = set()

        for attr_name, attr_value in vars(obj).items():
            if attr_name.startswith("_"):
                continue

            if callable(attr_value):
                continue

            _write_value(h5file, attr_name, attr_value, visited)

    else:
        _write_value(h5file, "value", obj, visited=set())