import adios2
import numpy as np
from typing import Optional, Any

def add_variables(
    filename: str,
    var1: str,
    var2: str,
    step1: Optional[int] = None,
    step2: Optional[int] = None
) -> Any:
    """
    Sum two variables in a BP5 file, either at specific steps or across all steps.

    Args:
      filename: Path to the BP5 directory
      var1: First variable name
      var2: Second variable name
      step1: If given, read var1 only at this step; otherwise sum var1 over all steps
      step2: If given, read var2 only at this step; otherwise sum var2 over all steps

    Returns:
      If the result is scalar: a Python float/int
      If an array: a flattened Python list of numbers

    Raises:
      ValueError if a requested step or variable is missing, or if the final shapes mismatch.
    """
    def fetch_sum(var: str, step: Optional[int]) -> np.ndarray:
        total = None
        with adios2.Stream(filename, "r") as s:
            for _ in s.steps():
                curr = s.current_step()
                if step is not None and curr != step:
                    continue
                if var not in s.available_variables():
                    raise ValueError(f"'{var}' not found in step {curr}")
                arr = s.read(var)
                data = np.asarray(arr)
                if total is None:
                    total = np.zeros_like(data)
                total += data
                if step is not None:
                    # done after one match
                    break
        if total is None:
            if step is not None:
                raise ValueError(f"Variable {var} or Step {step} not found for '{var}'")
            else:
                raise ValueError(f"No data found for variable '{var}'")
        return total

    sum1 = fetch_sum(var1, step1)
    sum2 = fetch_sum(var2, step2)

    if sum1.shape != sum2.shape:
        raise ValueError(
            f"Shape mismatch: {var1}{sum1.shape} vs {var2}{sum2.shape}"
        )
    result = sum1 + sum2

    # convert to Python types
    if result.ndim == 0:
        return result.item()
    return result.flatten().tolist()
