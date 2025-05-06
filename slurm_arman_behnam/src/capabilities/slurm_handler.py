import random

async def submit_job(params):
    """Simulate Slurm job submission."""
    script_path = params.get("script_path", "")
    cores = params.get("cores", 1)
    
    if not script_path:
        return {
            "error": {
                "code": 400,
                "message": "Missing required parameter: script_path"
            }
        }
    
    try:
        cmd = f"sbatch --ntasks={cores} {script_path}"
        print(f"Would execute: {cmd}")
        
        job_id = random.randint(10000, 99999)
        
        return {
            "tool": "slurm",
            "job_id": job_id,
            "status": "submitted",
            "metadata": {
                "script": script_path,
                "cores": cores,
                "queue": "compute"
            }
        }
    except Exception as e:
        return {
            "error": {
                "code": 500,
                "message": f"Job submission failed: {str(e)}"
            }
        }