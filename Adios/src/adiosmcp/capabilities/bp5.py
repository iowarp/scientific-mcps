# bp5.py
import numpy as np
import adios2

def bp5(filename: str) -> dict:
    """
    Read a BP5 file (any shape/dtype) via adios2.Stream.  
    Returns a nested dict of the form:
        {
          step_index: {
            "variables": {
                var_name: <scalar OR flattened list>,
                ...
            },
            "metadata": {
                var_name: {"shape": <string>, "dtype": <string>}, 
                ...
            },
            "attributes": {
                attribute_name: <value>, 
                ...
            }
          },
          ...
        }
    Raises exceptions up to the caller if the file can't be opened or if any step fails.
    """
    result = {}

    # Open in “read” mode using the high‐level Stream API
    with adios2.Stream(filename, "r") as s:
        # Loop over every step in the BP5 file
        for _ in s.steps():
            step = s.current_step()
            result[step] = {"variables": {}, "metadata": {}, "attributes": {}}

            # 1) Read all variables at this step
            avail_vars = s.available_variables()  # dict: var_name -> {"Shape": str, "Type": str, ...}
            for var_name, info in avail_vars.items():
                # Read raw data (NumPy scalar or array)
                arr = s.read(var_name)

                # Convert to plain Python types:
                if isinstance(arr, np.generic) or (hasattr(arr, "shape") and arr.shape == ()):
                    # Scalar → .item()
                    val = np.array(arr).item()
                else:
                    # Array → flatten & convert to list
                    val = np.array(arr).flatten().tolist()

                # Store the data under “variables”
                result[step]["variables"][var_name] = val

                # Store shape & dtype under “metadata”
                shape_str = info.get("Shape", "")
                dtype_str = info.get("Type", "")
                result[step]["metadata"][var_name] = {
                    "shape": shape_str,
                    "dtype": dtype_str
                }

            # 2) Read all attributes (if any exist) at this step
            avail_attrs = s.available_attributes()  # dict: attr_name -> {"Type": str, ...}
            for attr_name in avail_attrs:
                # adios2.Stream.read_attribute(...) returns a NumPy type or array if it is array‐typed.
                a = s.read_attribute(attr_name)
                # Convert to plain Python:
                if isinstance(a, np.generic) or (hasattr(a, "shape") and a.shape == ()):
                    a_val = np.array(a).item()
                else:
                    a_val = np.array(a).flatten().tolist()
                result[step]["attributes"][attr_name] = a_val

    return result
