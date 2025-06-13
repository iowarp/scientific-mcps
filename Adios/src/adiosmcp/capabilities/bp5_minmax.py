import adios2
import numpy as np
from typing import Optional, Dict, Any

def get_min_max(
    filename: str,
    variable_name: str,
    step: Optional[int] = None
) -> Dict[str, Any]:
    """
    Return the min and max of a variable in a BP5 file.

    Args:
      filename: Path to the BP5 directory (e.g. "run.bp")
      variable_name: Name of the variable to inspect
      step: If provided, only consider that timestep; otherwise consider all steps

    Returns:
      If step is given:
        {"step": step, "min": <float>, "max": <float>}
      Else:
        {"min": <float>, "max": <float>}
    
    Raises:
      ValueError if the requested step or variable is not found,
      or if the variable has no data.
    """
    global_min = None
    global_max = None

    with adios2.Stream(filename, "r") as s:
        for _ in s.steps():
            current = s.current_step()
            if step is not None and current != step:
                continue
            # make sure the var exists at this step
            if variable_name not in s.available_variables():
                raise ValueError(f"'{variable_name}' not found in step {current}")
            arr = s.read(variable_name)
            data = np.asarray(arr).flatten()
            if data.size == 0:
                continue
            step_min = data.min()
            step_max = data.max()
            if step is not None:
                # immediately return for a single step
                return {"step": step, "min": step_min.item(), "max": step_max.item()}
            # accumulate global
            if global_min is None:
                global_min, global_max = step_min, step_max
            else:
                global_min = min(global_min, step_min)
                global_max = max(global_max, step_max)

    if global_min is None:
        raise ValueError(f"Incorrect Variable name or No data found for variable '{variable_name}'")
    if step is not None:
        raise ValueError(f"Step {step} not found in file '{filename}'")
    return {"min": global_min.item(), "max": global_max.item()}
